document.addEventListener('DOMContentLoaded', (event) => {
    const textDisplay = document.getElementById('textDisplay');

    if (!!window.EventSource) {
        const source = new EventSource('/get_detected_text');

        source.addEventListener('message', function(e) {
            textDisplay.textContent = e.data; // Utilisez textContent pour définir le texte
        }, false);
    } else {
        console.log("Your browser does not support EventSource.");
    }
});
