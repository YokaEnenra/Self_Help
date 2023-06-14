$(function () {
    $("#button_create_note_click").on("click", function (e) {
        e.preventDefault();
        var url = $("#create-note-url").val();
        var csrfToken = $("#csrf-token").val();
        var language = $("#language").val();
        openCreateNoteModal(url, csrfToken, language);
    });
});

function openCreateNoteModal(url, csrfToken, language) {
    $("#click_create_note_modal").dialog({
        modal: true,
        height: "auto",
        width: "30vw",
        title: translate('New note creation', language),
        buttons: {
            [translate('Create note', language)]: function () {
                createNote(url, csrfToken);
            },
            [translate('Cancel', language)]: function () {
                $(this).dialog("close");
            }
        }
    });
}

function createNote(url, csrfToken) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            csrfmiddlewaretoken: csrfToken,
            note_title: $('#id_note_title').val(),
            note_text: $('#id_note_text').val(),
            vid_url: $('#id_vid_url').val(),
            project_slug: $('#project-slug').val(),
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