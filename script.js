
let currentPlayer = 'X';
let gameBoard = ['', '', '', '', '', '', '', '', ''];
let gameActive = true;
const cells = document.getElementsByClassName('cell');
const statusDisplay = document.getElementById('status');
const winningCombos = [
    [0, 1, 2], 
    [3, 4, 5], 
    [6, 7, 8], 
    [0, 3, 6], 
    [1, 4, 7], 
    [2, 5, 8], 
    [0, 4, 8], 
    [2, 4, 6]  
];
function makeMove(cellIndex) {
    if (gameBoard[cellIndex] === '' && gameActive) {
        gameBoard[cellIndex] = currentPlayer;
        cells[cellIndex].textContent = currentPlayer;
         if (checkWin()) {
            statusDisplay.textContent = `PLAYER ${currentPlayer} WINS!`;
            gameActive = false;
            return;
        }        
        if (checkDraw()) {
            statusDisplay.textContent = "GAME DRAW!";
            gameActive = false;
            return;
        }
        currentPlayer = currentPlayer === 'X' ? 'Y' : 'X';
        statusDisplay.textContent = `PLAYER ${currentPlayer} TURN`;
    }
}
function checkWin() {
    for (let combo of winningCombos) {
        if (
            gameBoard[combo[0]] !== '' &&
            gameBoard[combo[0]] === gameBoard[combo[1]] &&
            gameBoard[combo[1]] === gameBoard[combo[2]]
        ) {
            combo.forEach(index => cells[index].classList.add('WINNER'));
            return true;
        }
    }
    return false;
}
function checkDraw() {
    return !gameBoard.includes('');
}
function resetGame() {
    currentPlayer = 'X';
    gameBoard = ['', '', '', '', '', '', '', '', ''];
    gameActive = true;
    statusDisplay.textContent = `PLAYER ${currentPlayer} TURN`;
     for (let cell of cells) {
        cell.textContent = '';
        cell.classList.remove('WINNER');
    }
}