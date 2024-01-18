document.addEventListener('DOMContentLoaded', function () {
    // Get all elements with the class 'like-button'
    var likeButtons = document.querySelectorAll('.like-button');
    var dislikeButtons = document.querySelectorAll('.dislike-button');

    // Function to handle like and dislike actions
    function handleLikeDislike(button, dataUrl) {
        // Get the post ID from the data attribute
        var postId = button.getAttribute('data-post-id');
        var countElement = document.getElementById('like-count-' + postId);

        // Make an asynchronous request to the server to handle the action
        fetch(dataUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
            },
            body: JSON.stringify({}),
        })
        .then(response => response.json())
        .then(data => {
            // Update the count on the page
            countElement.textContent = data.like_count;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Loop through each like button
    likeButtons.forEach(function (likeButton) {
        likeButton.addEventListener('click', function (event) {
            event.preventDefault();
            handleLikeDislike(likeButton, likeButton.getAttribute('data-like-url'));
        });
    });

    // Loop through each dislike button
    dislikeButtons.forEach(function (dislikeButton) {
        dislikeButton.addEventListener('click', function (event) {
            event.preventDefault();
            handleLikeDislike(dislikeButton, dislikeButton.getAttribute('data-dislike-url'));
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Check if the cookie name matches the expected format
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
