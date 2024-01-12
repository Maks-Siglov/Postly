
var notification = $('#notification');
if (notification.length > 0) {
    setTimeout(function () {
        notification.alert('close');
    }, 5000);
}


$(document).ready(function () {
    $(".like-button, .dislike-button").on("click", function (e) {
        e.preventDefault();
        var button = $(this);
        var postId = button.data("post-id");
        var action = button.hasClass("like-button") ? "like" : "dislike";
        var url = action === "like" ? $(".like-button").data("like-url") : $(".dislike-button").data("dislike-url");
        var csrf_token = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: url,
            method: "POST",
            data: {
                post_id: postId,
                action: action,
                csrfmiddlewaretoken: csrf_token
            },
            success: function (data) {
                  if (action === "like") {
                    $("#like-count-" + postId).text(data.likes_count);
                } else {
                    $("#dislike-count-" + postId).text(data.dislikes_count);
                }
            },
            error: function (error) {
                console.log("Error:", error);
            }
        });
    });
});
