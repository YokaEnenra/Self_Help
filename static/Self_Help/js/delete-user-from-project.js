$(function() {
    $(".button-delete-added-user").on("click", function(e) {
        e.preventDefault();
        var email = $(this).data("email");
        if($.isEmptyObject(email)){
            return;
        }
        var url = $("#delete-user-from-project-url").val();
        var csrfToken = $("#csrf-token").val();
        var language = $("#language").val();
        openDeleteUserFromProjectModal(email, url, csrfToken, language);
    });
});

function openDeleteUserFromProjectModal(email, url, csrfToken, language) {
    var message = $("#delete_user_from_project_message");

    message.text(translate('Are you sure you want to delete "', language)
        + email + translate('" from this project?', language));

    $("#click_delete_user_from_project_modal").dialog({
        modal: true,
        height: "auto",
        width: "30vw",
        title: translate('User Deletion', language),
        buttons: {
            [translate('Delete user', language)]: function() {
                deleteUser(email, url, csrfToken);
            },
            [translate('Cancel', language)]: function() {
                $(this).dialog("close");
            }
        }
    });
}

function deleteUser(email, url, csrfToken) {
    $.ajax({
        type: "POST",
        url: url,
        data: {
            csrfmiddlewaretoken: csrfToken,
            project_slug: $('#project-slug').val(),
            user_email: email,
        },
        success: function (data) {
            if (data['success'] === true) {
                setTimeout(function () {
                    location.reload();
                }, 5);
            }

            if (data['success'] === false) {
                alert(data['status']);

                return false
            }

        },
        error: function (error) {
            console.log(error)
        },
    });
}
