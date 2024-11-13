; (function () {
    document.getElementById("modal_form").addEventListener("keypress", function(event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            return False;
        }
    });
})()