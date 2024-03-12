
document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', function() {
        // Get the text of the clicked item
        var text = this.textContent;
        // Find the parent dropdown of the clicked item
        var dropdown = this.closest('.dropdown');
        // Set the button text to the selected item's text
        // The button is the first element inside the dropdown div with the 'dropdown-toggle' class
        var button = dropdown.querySelector('.dropdown-toggle');
        button.textContent = text;
        // Optionally, you can append the caret symbol again if it disappears
        button.innerHTML = text + ' <span class="caret"></span>';
    });
});



function submitForm(){
    event.preventDefault();

    var genreVal = document.getElementById("genre").value;
    var tempoVal = document.getElementById("tempo").value;
    var lengthVal = document.getElementById("length").value;

    var data = {
        genre: genreVal, tempo: tempoVal, length: lengthVal
    };



    fetch('/submit_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',

    },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        document.getElementById("results").innerHTML = data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });

}