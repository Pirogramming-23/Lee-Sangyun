const display = document.getElementById('display');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const resetButton = document.getElementById('resetButton');

const stopwatchModeButton = document.getElementById('stopwatchModeButton');
const timerModeButton = document.getElementById('timerModeButton');
const timerSettings = document.querySelector('.timer-settings');
const minutesInput = document.getElementById('minutesInput');
const secondsInput = document.getElementById('secondsInput');

const lapsContainer = document.querySelector('.laps-container');
const lapsList = document.getElementById('laps');
const selectAllCheckbox = document.getElementById('selectAllCheckbox');
const deleteButton = document.getElementById('deleteButton');

let mode = 'stopwatch';
let timer;
let running = false;

let stopwatchStartTime = 0;
let elapsedTime = 0;

let timerDuration = 0;
let remainingTime = 0;

function formatTime(ms) {
    const date = new Date(ms);
    const minutes = String(date.getUTCMinutes()).padStart(2, '0');
    const seconds = String(date.getUTCSeconds()).padStart(2, '0');
    const milliseconds = String(Math.floor(date.getUTCMilliseconds() / 10)).padStart(2, '0');
    return `${minutes}:${seconds}:${milliseconds}`;
}

function resetAll() {
    clearInterval(timer);
    running = false;
    display.textContent = "00:00:00";
    
    stopwatchStartTime = 0;
    elapsedTime = 0;
    
    timerDuration = 0;
    remainingTime = 0;
    minutesInput.value = "0";
    secondsInput.value = "0";
    
    selectAllCheckbox.checked = false;
    updateSelectAllIcon();
}

function switchMode(newMode) {
    if (mode === newMode) return;
    mode = newMode;
    resetAll();

    if (mode === 'stopwatch') {
        stopwatchModeButton.classList.add('active');
        timerModeButton.classList.remove('active');
        timerSettings.style.display = 'none';
        lapsContainer.style.display = 'block';
        stopButton.textContent = 'stop';
    } else {
        timerModeButton.classList.add('active');
        stopwatchModeButton.classList.remove('active');
        timerSettings.style.display = 'flex';
        lapsContainer.style.display = 'none';
        stopButton.textContent = 'pause';
    }
}

stopwatchModeButton.addEventListener('click', () => switchMode('stopwatch'));
timerModeButton.addEventListener('click', () => switchMode('timer'));

function updateStopwatch() {
    const currentRunningTime = elapsedTime + (Date.now() - stopwatchStartTime);
    display.textContent = formatTime(currentRunningTime);
}

function startStopwatch() {
    if (running) return;
    running = true;
    stopwatchStartTime = Date.now() - elapsedTime;
    timer = setInterval(updateStopwatch, 10);
}

function stopStopwatch() {
    if (!running) return;
    running = false;
    clearInterval(timer);
    elapsedTime += Date.now() - stopwatchStartTime;
    display.textContent = formatTime(elapsedTime); 
    addLap(elapsedTime);
}

function updateTimer() {
    remainingTime -= 10;
    if (remainingTime <= 0) {
        clearInterval(timer);
        running = false;
        remainingTime = 0;
        display.textContent = "00:00:00";
        document.body.style.backgroundColor = '#f8d7da';
        setTimeout(() => { document.body.style.backgroundColor = '#f0f2f5'; }, 1000);
    }
    display.textContent = formatTime(remainingTime);
}

function startTimer() {
    if (running) return;
    
    if(remainingTime === 0) {
        const minutes = parseInt(minutesInput.value) || 0;
        const seconds = parseInt(secondsInput.value) || 0;
        timerDuration = (minutes * 60 + seconds) * 1000;
        remainingTime = timerDuration;
    }

    if (remainingTime <= 0) return;

    running = true;
    timer = setInterval(updateTimer, 10);
}

function pauseTimer() {
    if (!running) return;
    running = false;
    clearInterval(timer);
}

startButton.addEventListener('click', () => {
    if (mode === 'stopwatch') {
        startStopwatch();
    } else {
        startTimer();
    }
});

stopButton.addEventListener('click', () => {
    if (mode === 'stopwatch') {
        stopStopwatch();
    } else {
        pauseTimer();
    }
});

resetButton.addEventListener('click', resetAll);

function addLap(lapTime) {
    const lapItem = document.createElement('div');
    lapItem.classList.add('lap-item');
    
    const uniqueId = 'lap-' + Date.now();
    
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.classList.add('lap-checkbox');
    checkbox.id = uniqueId;
    
    const label = document.createElement('label');
    label.htmlFor = uniqueId;
    label.classList.add('checkbox-icon');
    label.innerHTML = '<i class="fa-regular fa-circle"></i><i class="fa-solid fa-check-circle"></i>';

    const timeSpan = document.createElement('span');
    timeSpan.classList.add('lap-time');
    timeSpan.textContent = formatTime(lapTime);

    lapItem.appendChild(checkbox);
    lapItem.appendChild(label);
    lapItem.appendChild(timeSpan);
    lapsList.prepend(lapItem);
}

function deleteSelectedLaps() {
    const laps = lapsList.querySelectorAll('.lap-item');
    laps.forEach(lap => {
        const checkbox = lap.querySelector('.lap-checkbox');
        if (checkbox.checked) {
            lapsList.removeChild(lap);
        }
    });
    selectAllCheckbox.checked = false;
    updateSelectAllIcon();
}

function toggleSelectAll() {
    const checkboxes = lapsList.querySelectorAll('.lap-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
}

function updateSelectAllIcon() {
}

deleteButton.addEventListener('click', deleteSelectedLaps);
selectAllCheckbox.addEventListener('change', () => {
    toggleSelectAll();
    updateSelectAllIcon();
});