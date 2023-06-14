$(function () {
    $("#button_create_project_click").on("click", function (e) {
        e.preventDefault();
        var url = $("#create-project-url").val();
        var csrfToken = $("#csrf-token").val();
        var language = $("#language").val();
        openCreateProjectModal(url, csrfToken, language);
    });
});

function openCreateProjectModal(url, csrfToken, language) {
    $("#click_create_project_modal").dialog({
        modal: true,
        height: "auto",
        width: "30vw",
        title: translate('New project creation', language),
        buttons: {
            [translate('Create project', language)]: function () {
                createProject(url, csrfToken);
            },
            [translate('Cancel', language)]: function () {
                $(this).dialog("close");
            }
        }
    });
}

function createProject(url, csrfToken) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            csrfmiddlewaretoken: csrfToken,
            project_title: $('#id_project_title').val(),
        },
        success: function (data) {
            if (data['success'] === true) {
                setTimeout(function () {
                    location.reload();
                }, 5);
            }
            if (data['success'] === false) {
                alert(data['status']);
                return false;
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}