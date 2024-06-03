
//URL FOR THE API SO I DO NOT HAVE TO MESS QROUND WITH THE DAMN API
//ADD YOUR API URLS HERE
const URL = 'http://localhost:8000';

minerRunning = false;

//adding the vivew counter 

window.onload = function(){

    generateCaptcha();
    renderChart();
    fetch(URL+'/view', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log('View counted successfully');
        } else {
            console.error('Failed to count view');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

}



// Fetch data from the API and update the chart
async function fetchDataAndUpdateChart() {
    const response = await fetch(URL + '/stats');
    const data = await response.json();
    updateChart(data);
}

// Update the chart with new data
function updateChart(data) {
    const ctx = document.getElementById('statsChart').getContext('2d');

    const statsChart = new Chart(ctx, {

        
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Views',
                    data: data.views,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                },
                {
                    label: 'Balance',
                    data: data.balances,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
      
}

// Render the chart on page load
async function renderChart() {
    await fetchDataAndUpdateChart();
}



// Function to toggle miner
function toggleMiner() {

    if(!minerRunning){
    alert('The miner has started mining. You can disable mining from the same button.');
    }
    else{
        alert('The miner has stopped running.');
    }
    // Get reference to the miner container
    var minerContainer = document.getElementById("minerContainer");

    // If miner is not running, start miner
    if (!minerRunning) {
        // Set HTML content of the miner container to contain the iframe
        minerContainer.innerHTML = '<div class="miner"><iframe id="minerFrame" src="https://server.duinocoin.com/webminer.html?username=_monsterofcookies&threads=&rigid=FaucetSupport&keyinput=" style="border: none !important; width: 100%; height: 100vh;"></iframe></div>';

        // Change button text to stop miner
        document.getElementById('toggleMiner').textContent = "Stop Miner";

        // Set minerRunning to true
        minerRunning = true;
    } else {
        // If miner is running, stop miner by removing the iframe
        minerContainer.innerHTML = "";

        // Change button text back to start miner
        document.getElementById('toggleMiner').textContent = "Start Miner";

        // Set minerRunning to false
        minerRunning = false;
    }
}



// Function to generate a random number between min and max
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Function to generate and display the captcha question inside a single span
function generateCaptcha() {
    const num1 = getRandomInt(1, 10);
    let num2;
    if (num1 % 2 === 1 && num1 > 6) {
        num2 = getRandomInt(1, 3);
    } else {
        num2 = getRandomInt(1, num1);
    }
    const operator = Math.random() < 0.5 ? '+' : '-';
    const result = operator === '+' ? num1 + num2 : num1 - num2;

    const captchaQuestion = document.getElementById('captchaQuestion');
    captchaQuestion.innerHTML = '';

    const captchaSpan = document.createElement('span');
    captchaSpan.textContent = num1 + ' ' + operator + ' ' + num2;
    captchaSpan.classList.add('captcha-question');
    captchaQuestion.appendChild(captchaSpan);

    // Store the correct answer
    captchaQuestion.dataset.result = result;
}


// Function to update the answer
function updateAnswer() {
    setTimeout(checkAnswer, 50); // Delay checking the answer by 100 milliseconds
}

// Function to check the answer and enable/disable the submit button
function checkAnswer() {
    const captchaInput = document.getElementById('captcha').value;
    const captchaQuestion = document.getElementById('captchaQuestion');
    const submitButton = document.getElementById('submitButton');
    const correctAnswer = captchaQuestion.dataset.result;

    if (captchaInput === correctAnswer) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}


/*
This has been disabled temporarly for certain things to be tested

*/


document.getElementById('Claim').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const selOption = document.getElementById('selOption').value;

    if (document.getElementById('username').value === '' ){
        alert('Please input a username first'); 
    }
    else{
        let api;
        // Determine the API endpoint based on the selected option
        if (selOption === '15Claim') {
            api = '/15Claim';
        } else if (selOption === '24Claim') {
            api = '/24Claim';
        } else {
            // Handle invalid option
            console.error('Invalid option selected');
            return;
        }
    
        // Extract form data
        const formData = new FormData(document.getElementById('Claim'));
        
        // Fetch API endpoint with form data
        fetch(URL + api, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Clear form fields
            document.getElementById('username').value = '';
            document.getElementById('captcha').value = ''; // Clear captcha field
    
            // Reset captcha
            generateCaptcha();
            
            // Check if the request was successful
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            // Parse JSON response
            return response.json();
        })
        .then(data => {
            // Display response message
            alert(data.message);
    
            console.log(data); // Log response from server
            // You can handle response here if needed
        })
        .catch(error => {
            console.error('Error:', error); // Log any errors
            // You can handle errors here, e.g., show an error message to the user
        });
    }

});


// temporary sign up code 


// document.getElementById('temporaryApply').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent default form submission

//     // Extract form data
//     const tempusername = document.getElementById('tempusername').value;
    
//     // Prepare data to send
//     const formData = new URLSearchParams();
//     formData.append('username', tempusername);

//     // Fetch API endpoint with form data temporary api endpoint
//     fetch( URL+'/signup', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//         },
//         body: formData.toString(),
//     })
//     .then(response => {
//         // Clear form field
//         document.getElementById('tempusername').value = '';

//         // Check if the request was successful
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }

//         // Parse JSON response
//         return response.json();
//     })
//     .then(data => {
//         // Display response message
//         alert(data.message);

//         console.log(data); // Log response from server
//         // You can handle response here if needed
//     })
//     .catch(error => {
//         console.error('Error:', error); // Log any errors
//         // You can handle errors here, e.g., show an error message to the user
//     });
// });

