$(function () {
    $("#button_edit_project_click").on("click", function (e) {
        e.preventDefault();
        var url = $("#edit-project-url").val();
        var csrfToken = $("#csrf-token").val();
        var language = $("#language").val();
        var projectSlug = $('#project-slug').val();
        var nexUrl = $('#all-projects-page-url').val();
        openEditProjectModal(url, csrfToken, language, projectSlug, nexUrl);
    });
});

function openEditProjectModal(url, csrfToken, language, projectSlug, nexUrl) {
    $("#click_edit_project_modal").dialog({
            modal: true,
            height: "auto",
            width: "30vw",
            title: translate('Project Editing', language),
            buttons: {
                [translate('Confirm Changes', language)]: function () {
                    editProject(url, csrfToken, projectSlug, nexUrl);
                },
                [translate('Cancel', language)]: function () {
                    $(this).dialog("close");
                }
            }
        })
}

function editProject(url, csrfToken, projectSlug, nexUrl) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            csrfmiddlewaretoken: csrfToken,
            project_slug: projectSlug,
            new_project_title: $('#id_new_project_title').val(),
        },
        success: function (data) {
            if (data['success'] === true) {
                location.replace(nexUrl);
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