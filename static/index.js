let audiosrc;

console.log('Hello from index.js!')

var xhr = null;

function getDate() {
    date = new Date().toString();
    document.getElementById('time-container').textContent
        = date;
}

// an http requet, need to tell it which method to use
getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

// notifies us when the response has been recieved in the backend
function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        getDate();
        dataDiv = document.getElementById('demodiv');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}

function getUsers() {
    console.log("Get users...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "http://localhost:6969/demos", true);
    // Send the request over the network
    xhr.send(null);
}
// server sends response data to our UI
function sendDataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        getDate();
        dataDiv = document.getElementById('demodiv');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}

// code that sends the request
function sendDemos() {
    console.log('send demos function');
    var dataToSend = 'hi';
    // dataToSend = document.getElementById("audioUploadMel").files[0];
    // console.log(dataToSend);
    if (!dataToSend) {
        console.log("No demos to send!:(");
        return;
    }
    console.log("Sening demos...", dataToSend);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/demos", true);

    // set header blessed
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // Send the request over the network
    xhr.send(JSON.stringify({"data": dataToSend}));
}

document.getElementById('audioUploadMel').addEventListener('change', function(event) {
    handleAudioUpload(event, 'audioPlayerMelody', 'audioSrcMelody');
});

document.getElementById('playBtn').addEventListener('click', playAudioMelody);


function playAudioMelody() {
    playAudio('audioPlayerMelody', 'audioSrcMelody');
}


function playAudio(playerID, srcVariable) {
    const player = document.getElementById(playerID);
    if (window[srcVariable]) {
        player.play();
    } else {
        alert("Please upload an audio file first.");
        document.getElementById('playBtn').style.backgroundImage = 'url(/static/NoFilePlay.png)';
    }
}

function setfile(val) {
    document.getElementById('file-name').innerHTML = val;
}

function handleAudioUpload(event, playerID, srcVariable) {
    sendDemos();
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file',file);
    console.log(file);

    // fetch('/upload', {
    //     method: 'POST',
    //     body: formData,
    //     headers: {
    //         'Content-Type': 'multipart/form-data',
    //     },
    // })
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error('Network response was not ok');
    //     }
    //     return response.json(); // Assuming the server returns JSON
    // })

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            window[srcVariable] = e.target.result; // Use window to access the variable by name
            document.getElementById(playerID).src = window[srcVariable];
            document.getElementById('playBtn').style.backgroundImage = 'url(./images/FilePlay.png)';
            document.getElementById('uploadText').textContent = 'Succefully uploaded';
        };
        reader.readAsDataURL(file);
    }
}

var fileName;
var fileSize;

function uploadFile() {
    var fileInput = document.getElementById('audioUploadMel');
    var file = fileInput.files[0]; // Get the first file (assuming single file upload)

    if (file) {
        var formData = new FormData();
        formData.append('file', file);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/input');
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText); // Parse JSON response
                fileName = response.file_name;
                fileSize = response.file_size;

                console.log('File uploaded successfully.');
                console.log('File Name:', fileName);
                console.log('File Size:', fileSize);

                // Set the response to a variable or use it as needed
                // For example, update the UI with the file information
                document.getElementById('fileInfo').innerText = `File Name: ${fileName}, File Size: ${fileSize}`;
            } else {
                console.error('Error uploading file.');
            }
        };
        xhr.send(formData);
    } else {
        console.error('No file selected.');
    }
}

localStorage.setItem('blessed', False);
function startNN() {
    console.log("startNN() function")

    var parameter = fileName;  // Set your parameter here
    var data = { "parameter": parameter };
    console.log('the input file is: ', parameter)

    // load next page
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/gen', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Success: Page content received
                var newPageContent = xhr.responseText;
                document.open();
                document.write(newPageContent);
                document.close();
            } else {
                // Error: Failed to retrieve page content
                console.error('Failed to switch page:', xhr.status);
            }
        }
    };
    xhr.send();

    // start generation
    fetch('/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from Flask backend:', data);
        // Handle the response as needed
        alert('Result from Flask backend: ' + data.result);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    blessed = True;
    localStorage.setItem('blessed', True);


    
}

