window.onload = function() {
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