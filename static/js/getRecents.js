$(document).ready(function() {
    $.getJSON( "/api/v1/posts", function(resp) {
        if (resp.success == "failure") {
            return;
        }
        $.each(JSON.parse(resp.data), function(index, post) {
            $("#postContainer").append(`
                <div class="col-md-2 border border-dark m-2 p-2" id="${post.id}">
                    <a href="/${post.board}/${post.id}">
                        <img class="img-fluid" src="${post.thumb}">
                    </a>
                    <h5>${post.subject}</h5>
                    <p style="max-height: 50px; overflow: hidden;"><small>${post.body}</small></p>
                </div>
            `);
        });
    });
});