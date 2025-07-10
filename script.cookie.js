window.onload = function() {
    // Check if clues variable exists
    if (!window.clues) {
        alert('Error: clues variable not found');
    }

    // Extract the last part of the path (the code) and update iframe src
    var pathParts = window.location.pathname.split('/');
    var code = pathParts[pathParts.length - 2]; // Get the second-to-last part (before 'index.html')
    var prefix = code[0];
    var cookieName = 'moodeng_code_' + prefix;
    appendToCookie(cookieName, code);
    displayFoundMoodengs(cookieName);
    autoShowClues(cookieName);
    
    // Find the iframe and set the URL with the extracted code
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

// Function to automatically show clues based on number of codes collected
function autoShowClues(cookieName) {
    var cluesDiv = document.getElementById('cluesList');
    if (!cluesDiv) {
        alert('Error: cluesList element not found');
        return;
    }
    
    var numCodes = Object.keys(JSON.parse(Cookies.get(cookieName) || '{}')).length;
    var numCluesToShow = Math.min(numCodes, clues.length);
    
    if (numCluesToShow > 0) {
        for (var i = 0; i < numCluesToShow; i++) {
            var clueDiv = document.createElement('div');
            clueDiv.className = 'clue-item';
            clueDiv.id = 'clue-' + i;
            clueDiv.textContent = (i + 1) + '. ' + clues[i];
            cluesDiv.appendChild(clueDiv);
        }
    }
} 