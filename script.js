window.onload = function() {
    // Get clues from the global variable defined in the HTML
    var clues = window.clues || [];
    if (!window.clues) {
        alert('Error: clues variable not found');
    }

    // Extract the last part of the path (the code) and update iframe src
    var pathParts = window.location.pathname.split('/');
    var code = pathParts[pathParts.length - 2]; // Get the second-to-last part (before 'index.html')
    
    // Find the iframe and set the URL with the extracted code
    var iframe = document.querySelector('iframe');
    if (iframe) {
        var baseUrl = iframe.getAttribute('data-base-url');
        if (baseUrl) {
            iframe.src = baseUrl + code;
        }
    }


}; 