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