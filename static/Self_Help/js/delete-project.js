$(function () {
    $("#button_delete_project_click").on("click", function (e) {
        e.preventDefault();
        var url = $("#delete-project-url").val();
        var csrfToken = $("#csrf-token").val();
        var language = $("#language").val();
        var projectSlug = $("#project-slug").val();
        var nextUrl = $("#all-projects-page-url").val();
        openDeleteProjectModal(url, csrfToken, language, projectSlug, nextUrl);
    });
});

function openDeleteProjectModal(url, csrfToken, language, projectSlug, nextUrl) {
    $("#click_delete_project_modal").dialog({
        modal: true,
        height: "auto",
        width: "30vw",
        title: translate('Delete Confirmation', language),
        buttons: {
            [translate('Delete Project', language)]: function() {
                deleteProject(url, csrfToken, projectSlug, nextUrl);
            },
            [translate('Cancel', language)]: function () {
                $(this).dialog("close");
            }
        }
    });
}

function deleteProject(url, csrfToken, projectSlug, nextUrl) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            csrfmiddlewaretoken: csrfToken,
            project_slug: projectSlug,
        },
        success: function (data) {
            if (data['success'] === true) {
                setTimeout(function () {
                    location.replace(nextUrl);
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