window.onload = function() {
    // Get clues from the global variable defined in the HTML
    var clues = window.clues || [];
    var cluesDiv = document.getElementById('cluesList');
    if (cluesDiv) {
        var cluesText = '<strong>Clues:</strong><br>';
        
        clues.forEach(function(clue, index) {
            cluesText += '<div class="clue-item" id="clue-' + index + '">' + (index + 1) + '. ' + clue + '</div>';
        });
        
        cluesDiv.innerHTML = cluesText;
    }

    // Extract the last part of the path (the code) and update iframe src
    var pathParts = window.location.pathname.split('/');
    var code = pathParts[pathParts.length - 2]; // Get the second-to-last part (before 'index.html')
    var prefix = code[0];
    var cookieName = 'moodeng_code_' + prefix;
    appendToCookie(cookieName, code);
    displayCookieCodes(cookieName);
    autoShowClues(cookieName);
    
    // Find the iframe and update its src with the code
    var iframe = document.querySelector('iframe');
    if (iframe) {
        iframe.src = iframe.src.replace('REPLACE_CODE_HERE', code);        iframe.src = updatedSrc;
    }

    window.showClues = function(numClues) {
        for (var i = 0; i < clues.length; i++) {
            var clueElement = document.getElementById('clue-' + i);
            if (clueElement) {
                clueElement.style.display = 'none';
            }
        }

        for (var i = 0; i < numClues && i < clues.length; i++) {
            var clueElement = document.getElementById('clue-' + i);
            if (clueElement) {
                clueElement.style.display = 'block';
            }
        }
    };
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

function displayCookieCodes(cookieName) {
    var cookieDiv = document.getElementById('cookieCodes');
    if (!cookieDiv) {
        cookieDiv = document.createElement('div');
        cookieDiv.id = 'cookieCodes';
        cookieDiv.style.cssText = 'position: fixed; top: 10px; right: 10px; background: #f0f0f0; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 12px; z-index: 1000; max-width: 300px;';
        document.body.appendChild(cookieDiv);
    }
    var moodengCode = Cookies.get(cookieName);
    var cookieText = '<strong>Moodengs ' + cookieName + ' Found:</strong><br>';
    if (moodengCode) {
        try {
            var codes = Object.keys(JSON.parse(moodengCode));
            codes.forEach(function(code, index) {
                cookieText += (index + 1) + '. ' + code + '<br>';
            });
        } catch (e) {
            cookieText += 'No Moodengs found';
        }
    } else {
        cookieText += 'No Moodengs found';
    }
    
    cookieDiv.innerHTML = cookieText;
}

// Function to automatically show clues based on number of codes collected
function autoShowClues(cookieName) {
    var numCodes = Object.keys(JSON.parse(Cookies.get(cookieName) || '{}')).length;
    
    var numCluesToShow = Math.min(numCodes, clues.length);
    
    for (var i = 0; i < clues.length; i++) {
        var clueElement = document.getElementById('clue-' + i);
        if (clueElement) {
            clueElement.style.display = 'none';
        }
    }
    
    for (var i = 0; i < numCluesToShow; i++) {
        var clueElement = document.getElementById('clue-' + i);
        if (clueElement) {
            clueElement.style.display = 'block';
        }
    }
} 