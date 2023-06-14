$(function () {
    $("#button_add_user_to_project").on("click", function (e) {
        e.preventDefault();
        var url = $("#add-user-to-project-url").val();
        var csrfToken = $("#csrf-token").val();
        var language = $("#language").val();
        openAddUserToProjectModal(url, csrfToken, language);
    });
});

function openAddUserToProjectModal(url, csrfToken, language) {
    $("#click_add_user_to_project_modal").dialog({
        modal: true,
        height: "auto",
        width: "30vw",
        title: translate('User addition', language),
        buttons: {
            [translate('Add user', language)]: function () {
                addUserToProject(url, csrfToken);
            },
            [translate('Cancel', language)]: function () {
                $(this).dialog("close");
            }
        }
    });
}

function addUserToProject(url, csrfToken) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            csrfmiddlewaretoken: csrfToken,
            project_slug: $('#project-slug').val(),
            new_user_email: $('#id_new_user_email').val(),
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
        }
        ,
    })
}