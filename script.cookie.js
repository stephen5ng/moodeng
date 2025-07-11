const hider_colors = {
    "S": "TURQUOISE",
    "G": "PINK"
};

window.onload = function() {
    if (!window.clues) {
        alert('Error: clues variable not found');
    }

    var urlParams = new URLSearchParams(window.location.search);
    var code = urlParams.get('moo');
    if (!code || !window.clues || !window.codes[code] || !window.clues[code[0]]) {
        window.location.replace('/');
        return;
    }
    var hiderCode = code[0];
    var cookieName = 'moodeng_code_' + hiderCode;
    appendToCookie(cookieName, code);
    displayFoundMoodengs(cookieName);

    var colorSpan = document.getElementById('moodengColor');
    if (colorSpan) {
        colorSpan.innerText = hider_colors[hiderCode] || '';
    }

    window.clues = window.clues[hiderCode];

    autoShowClues(cookieName);
    
    var iframe = document.querySelector('iframe');
    if (iframe) {
        var baseUrl = iframe.getAttribute('data-base-url');
        if (baseUrl) {
            iframe.src = baseUrl + code;
        }
    }
};

function appendToCookie(name, value) {
    var cookieObj;
    try {
        cookieObj = JSON.parse(Cookies.get(name) || '{}');
    } catch (e) {
        cookieObj = {};
    }
    cookieObj[value] = true;
    Cookies.set(name, JSON.stringify(cookieObj));
}

function displayFoundMoodengs(cookieName) {
    var foundDiv = document.getElementById('foundMoodengs');
    if (!foundDiv) {
        alert('Error: foundMoodengs element not found');
        return;
    }
    
    var moodengCode = Cookies.get(cookieName) || '{}';
    try {
        var codes = Object.keys(JSON.parse(moodengCode));
        foundDiv.textContent = codes.join(', ');
    } catch (e) {
        Cookies.remove(cookieName);
        alert('Error parsing cookie');
    }
}

function autoShowClues(cookieName) {
    var cluesDiv = document.getElementById('cluesList');
    if (!cluesDiv) {
        alert('Error: cluesList element not found');
        return;
    }
    
    var numCodes = Object.keys(JSON.parse(Cookies.get(cookieName) || '{}')).length;
    for (var i = 0; i < numCodes; i++) {
        var clueDiv = document.createElement('div');
        clueDiv.className = 'clue-item';
        clueDiv.textContent = (i + 1) + '. ' + window.clues[i];
        cluesDiv.appendChild(clueDiv);
    }
} 