document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll('.like-button');
    const dislikeButtons = document.querySelectorAll('.dislike-button');

    likeButtons.forEach(function (button) {
        handleButtonClick(button);
    });

    dislikeButtons.forEach(function (button) {
        handleButtonClick(button);
    });

    function handleButtonClick(button, actionCallback) {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const url = this.getAttribute('data-url');
            const postId = this.getAttribute('data-post-id');

            const csrftoken = getCookie('csrftoken');

            const xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);

            xhr.onreadystatechange = function () {
                readyXhr(xhr, postId);
            };

            xhr.send();
        });
    }

    function readyXhr(xhr, postId) {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const success = response.success;
            const likeCount = response.like_count;
            const dislikeCount = response.dislike_count;

            if (success) {
                let likeCountSpan = document.getElementById('like-count-' + postId);
                likeCountSpan.textContent = likeCount;
                let dislikeCountSpan = document.getElementById('dislike-count-' + postId);
                dislikeCountSpan.textContent = dislikeCount;
            } else {
                console.error('Error during disliking the post.');
            }
        }
    }

    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
});
