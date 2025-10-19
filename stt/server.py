import asyncio
import json
from collections import deque
from typing import Deque

import numpy as np
import websockets
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
WINDOW_SECONDS = 5.0
STEP_SECONDS = 0.4


class RealTimeSTTServer:
    def __init__(self, model_name: str = "large-v3", device: str = "cpu", compute_type: str = "int8") -> None:
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    async def stream_handler(self, ws):
        ring: Deque[int] = deque(maxlen=int(SAMPLE_RATE * WINDOW_SECONDS))
        last_sent = ""

        async def transcribe_loop():
            nonlocal last_sent
            while True:
                await asyncio.sleep(STEP_SECONDS)
                if len(ring) < SAMPLE_RATE:  # wait until >=1s audio buffered
                    continue
                audio = np.array(ring, dtype=np.float32) / 32768.0
                segments, _ = self.model.transcribe(
                    audio=audio,
                    language="ur",
                    task="transcribe",
                    beam_size=1,
                    vad_filter=True,
                    without_timestamps=True,
                    condition_on_previous_text=False,
                )
                text = "".join(s.text for s in segments).strip()
                if text and text != last_sent:
                    try:
                        await ws.send(json.dumps({"type": "partial", "text": text}))
                        last_sent = text
                    except Exception:
                        break

        tx_task = asyncio.create_task(transcribe_loop())
        try:
            async for msg in ws:
                if isinstance(msg, (bytes, bytearray)):
                    pcm = np.frombuffer(msg, dtype=np.int16)
                    ring.extend(pcm.tolist())
                else:
                    try:
                        data = json.loads(msg)
                        if data.get("type") == "reset":
                            ring.clear()
                    except Exception:
                        pass
        finally:
            tx_task.cancel()


async def main():
    import os

    host = os.environ.get("STT_HOST", "0.0.0.0")
    port = int(os.environ.get("STT_PORT", "8000"))
    model_name = os.environ.get("WHISPER_MODEL", "large-v3")
    device = os.environ.get("WHISPER_DEVICE", "cpu")  # "cuda" for GPU
    compute_type = os.environ.get("WHISPER_COMPUTE", "int8")  # e.g. "float16" on GPU

    server = RealTimeSTTServer(model_name, device, compute_type)
    async with websockets.serve(server.stream_handler, host, port, max_size=2**23):
        print(f"STT server running ws://{host}:{port} using {model_name} on {device}/{compute_type}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
