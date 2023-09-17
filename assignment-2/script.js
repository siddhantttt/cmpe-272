// Function to make POST request and create a tweet
function createTweet() {
    const tweetText = document.getElementById("tweetText").value;
    fetch("http://127.0.0.1:5000/tweets", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: tweetText })
    })
    .then(response => response.json())
    .then(data => {
        alert("Tweet created successfully!");
    })
    .catch(error => {
        console.error("Error creating tweet:", error);
    });
}

// Function to make DELETE request and delete a tweet
function deleteTweet() {
    const tweetId = document.getElementById("tweetId").value;
    fetch(`http://127.0.0.1:5000/tweets/${tweetId}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert("Tweet deleted successfully!");
    })
    .catch(error => {
        console.error("Error deleting tweet:", error);
    });
}

// Function to get authenticated user info
function getAuthenticatedUser() {
    fetch("http://127.0.0.1:5000/users/me")
    .then(response => response.json())
    .then(data => {
        const userInfo = document.getElementById("userInfo");
        userInfo.innerHTML = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error("Error getting user info:", error);
    });
}

// Function to get user tweets
function getUserTweets() {
    const userId = document.getElementById("userId").value;
    fetch(`http://127.0.0.1:5000/user/${userId}/tweets`)
    .then(response => response.json())
    .then(data => {
        const userTweets = document.getElementById("userTweets");
        userTweets.innerHTML = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error("Error getting user tweets:", error);
    });
}
