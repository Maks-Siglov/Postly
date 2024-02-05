document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll('.like-comment-button');
    const dislikeButtons = document.querySelectorAll('.dislike-comment-button');

    likeButtons.forEach(function (button) {
        handleCommentButtonClick(button, readyXhr);
    });

    dislikeButtons.forEach(function (button) {
        handleCommentButtonClick(button, readyXhr);
    });

    function handleCommentButtonClick(button, actionCallback) {
        button.addEventListener('click', function (event) {

            const url = this.getAttribute('data-url');
            const commentId = this.getAttribute('data-comment-id');

            const csrftoken = getCookie('csrftoken');

            const xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);

            xhr.onreadystatechange = function () {
                actionCallback(xhr, commentId);
            };
            xhr.send();
            event.preventDefault();
        });
    }

    function readyXhr(xhr, commentId) {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const success = response.success;
            const likeCount = response.like_count;
            const dislikeCount = response.dislike_count;

            if (success) {
                let likeCountSpan = document.getElementById('like-comment-count-' + commentId);
                likeCountSpan.textContent = likeCount;
                let dislikeCountSpan = document.getElementById('dislike-comment-count-' + commentId);
                dislikeCountSpan.textContent = dislikeCount;
            } else {
                console.error('Error disliking the post.');
            }
        }
    }

    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
});
