window.onload = function() {
    // Get clues from the global variable defined in the HTML
    var clues = window.clues || [];
    var cluesDiv = document.getElementById('cluesList');
    if (cluesDiv) {
        var strongElement = document.createElement('strong');
        strongElement.textContent = 'Clues:';
        cluesDiv.appendChild(strongElement);
        cluesDiv.appendChild(document.createElement('br'));
        
        for (var i = 0; i < clues.length; i++) {
            var clueDiv = document.createElement('div');
            clueDiv.className = 'clue-item';
            clueDiv.id = 'clue-' + i;
            clueDiv.textContent = (i + 1) + '. ' + clues[i];
            cluesDiv.appendChild(clueDiv);
        }
    } else {
        alert('Error: cluesList element not found');
    }

    // Extract the last part of the path (the code) and update iframe src
    var pathParts = window.location.pathname.split('/');
    var code = pathParts[pathParts.length - 2]; // Get the second-to-last part (before 'index.html')
    
    // Find the iframe and update its src with the code
    var iframe = document.querySelector('iframe');
    if (iframe) {
        var currentSrc = iframe.src;
        iframe.src  = currentSrc.replace('REPLACE_CODE_HERE', code);
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