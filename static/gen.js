function startProcessing() {
    document.getElementById('downloadButton').style.display = 'none';
    document.getElementById('playButton').style.display = 'none';
}

// Function to hide the loading screen and show the buttons
function finishProcessing() {
    // if localStorage.getItem('blessed') == True:
    // c
    document.getElementById('loading').style.display = 'none';
    document.getElementById('downloadButton').style.display = 'block';
    document.getElementById('playButton').style.display = 'block';
}

// Example usage
startProcessing()
setTimeout(finishProcessing, 1000);

document.getElementById('downloadButton').addEventListener('click', downloadPrediction);
document.getElementById('playButton').addEventListener('click', playPrediction);

function downloadPrediction() {
    fetch('/process', {
        method: 'POST',
        headers:{
            'Content-Type': 'appliction/json'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.outputFilePath) {
            document.getElementById('downloadButton').href =downloadUrl;
        } else {
            alert('Failed to download prediction.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to download prediction.');
    });
}


// function playPrediction() {
//     const downloadUrl = document.getElementById('playButton').getAttribute('data-url');
//     if (downloadUrl) {
//         const audio = new Audio(downloadUrl);
//         audio.play();
//     } else {
//         alert('Prediction not available for playback.');
//     }
// }

function playPrediction() {
    var audio = new Audio('/result'); // Create an <audio> element

    // Handle audio events
    audio.onloadedmetadata = function() {
        console.log('Audio metadata loaded');
        audio.play(); // Start playing the audio once metadata is loaded
    };

    audio.onerror = function() {
        console.error('Error loading audio');
    };

}


function getFile() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/result');
    xhr.responseType = 'blob'; // Set the response type to blob

    xhr.onload = function() {
        if (xhr.status === 200) {
            var blob = xhr.response;
            var url = window.URL.createObjectURL(blob);

            // Create a link element to trigger the download
            var a = document.createElement('a');
            a.href = url;
            a.download = 'file.txt'; // Set the desired file name
            document.body.appendChild(a);
            a.click();

            // Clean up
            window.URL.revokeObjectURL(url);
        } else {
            console.error('Error fetching file.');
        }
    };

    xhr.send();
}
