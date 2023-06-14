$(function () {
    $("#button_delete_note_click").on("click", function (e) {
        e.preventDefault();
        var url = $("#delete-note-url").val();
        var csrfToken = $("#csrf-token").val();
        var language = $("#language").val();
        var noteSlug = $("#note-slug").val();
        var nextUrl = $("#notes-project-url").val();
        var noProjectUrl = $("#no-project-title-url").val();
        var projectTitle = $("#notes-project-title").val();
        openDeleteNoteModal(url, csrfToken, language, noteSlug, nextUrl, noProjectUrl, projectTitle);
    });
});

function openDeleteNoteModal(url, csrfToken, language, noteSlug, nextUrl, noProjectUrl, projectTitle) {
    $("#click_delete_note_modal").dialog({
        modal: true,
        height: "auto",
        width: "30vw",
        title: translate('Delete Confirmation', language),
        buttons: {
            [translate('Delete Note', language)]: function () {
                deleteNote(url, csrfToken, noteSlug, nextUrl, noProjectUrl, projectTitle);
            },
            [translate('Cancel', language)]: function () {
                $(this).dialog("close");
            }
        }
    });
}

function deleteNote(url, csrfToken, noteSlug, nextUrl, noProjectUrl, projectTitle) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            csrfmiddlewaretoken: csrfToken,
            note_slug: noteSlug,
        },
        success: function (data) {
            if (data['success'] === true) {
                if (projectTitle == null) {
                    location.replace(noProjectUrl);
                } else {
                    location.replace(nextUrl);
                }
            }
            if (data['success'] === false) {
                alert(data['status']);
                return false
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}