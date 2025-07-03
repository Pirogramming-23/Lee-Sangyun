const numberInputs = document.querySelectorAll('.input-field');
const submitButton = document.querySelector('.submit-button');
const resultDisplay = document.getElementById('results');
const attemptsSpan = document.getElementById('attempts');
const resultImage = document.getElementById('game-result-img');

let answer; 
let attempts; 

function startGame() {
    let initialAttemptsInput;
    while (true) {
        initialAttemptsInput = prompt("시도할 횟수를 입력하세요 (1~20 사이)", "10");
        if (initialAttemptsInput === null) {
            attempts = 10; 
            alert("기본 횟수인 10회로 게임을 시작합니다.");
            break;
        }
        const parsedAttempts = parseInt(initialAttemptsInput, 10);
        if (!isNaN(parsedAttempts) && parsedAttempts > 0 && parsedAttempts <= 20) {
            attempts = parsedAttempts;
            break;
        } else {
            alert("1에서 20 사이의 유효한 숫자를 입력해주세요.");
        }
    }
    attemptsSpan.textContent = attempts;

    answer = [];
    while (answer.length < 3) {
        const randomNumber = Math.floor(Math.random() * 10);
        if (!answer.includes(randomNumber)) {
            answer.push(randomNumber);
        }
    }
    console.log("정답:", answer);

    numberInputs.forEach(input => input.value = '');
    resultDisplay.innerHTML = '';

    resultImage.src = '';
    resultImage.style.display = 'none';
    submitButton.disabled = false;
    
    if (numberInputs.length > 0) {
        numberInputs[0].focus();
    }
}


window.check_numbers = function() {
    const userGuess = Array.from(numberInputs).map(input => input.value);

    if (userGuess.some(num => num === '')) {
        console.warn("숫자 3개를 모두 입력해주세요.");
        numberInputs.forEach(input => input.value = '');
        if (numberInputs.length > 0) numberInputs[0].focus();
        return;
    }
    
    const userGuessSet = new Set(userGuess);
    if (userGuessSet.size !== 3) {
        console.warn("중복되지 않는 숫자를 입력해주세요.");
        numberInputs.forEach(input => input.value = '');
        if (numberInputs.length > 0) numberInputs[0].focus();
        return;
    }

    const userNumbers = userGuess.map(num => parseInt(num, 10));
    let strikes = 0;
    let balls = 0;

    for (let i = 0; i < 3; i++) {
        if (userNumbers[i] === answer[i]) {
            strikes++;
        } else if (answer.includes(userNumbers[i])) {
            balls++;
        }
    }

    attempts--;
    attemptsSpan.textContent = attempts;

    const resultLine = document.createElement('div');
    resultLine.className = 'check-result';
    resultLine.style.justifyContent = 'space-between';

    let resultHTML = `
        <div class="left">${userNumbers.join(' ')}</div>
        <div>:</div>
        <div class="right">
    `;

    if (strikes === 0 && balls === 0) {
        resultHTML += `<span class="num-result out">O</span>`; 
    } else {
        resultHTML += `${strikes}<span class="num-result strike">S</span> ${balls}<span class="num-result ball">B</span>`;
    }

    resultHTML += `</div>`;
    resultLine.innerHTML = resultHTML;
    resultDisplay.appendChild(resultLine);
    resultDisplay.scrollTop = resultDisplay.scrollHeight;

    numberInputs.forEach(input => input.value = '');
    if (numberInputs.length > 0) numberInputs[0].focus();

    if (strikes === 3) {
        endGame(true);
    } else if (attempts === 0) {
        endGame(false);
    }
}


function endGame(isWin) {
    submitButton.disabled = true;
    numberInputs.forEach(input => {
        input.disabled = true;
    });
    resultImage.style.display = 'block';

    const finalMessage = document.createElement('div');
    finalMessage.className = 'check-result';
    finalMessage.style.justifyContent = 'center';

    if (isWin) {
        resultImage.src = 'success.png';
        finalMessage.innerHTML = `<div class="final-message" style="color: blue;"> 정답입니다! </div>`;
    } else {
        resultImage.src = 'fail.png';
        finalMessage.innerHTML = `<div class="final-message" style="color: red;">실패! 정답은 ${answer.join('')}</div>`;
    }
    resultDisplay.appendChild(finalMessage);
    resultDisplay.scrollTop = resultDisplay.scrollHeight;
}


numberInputs.forEach((input, index) => {
    input.addEventListener('input', () => {
        if (input.value && index < numberInputs.length - 1) {
            numberInputs[index + 1].focus();
        }
    });
    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            check_numbers();
        }
    });
});

if(submitButton) {
    submitButton.onclick = window.check_numbers;
}

startGame();
