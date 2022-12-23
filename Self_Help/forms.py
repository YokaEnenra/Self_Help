from django import forms


class NewProject(forms.Form):
    project_title = forms.CharField(label="project_title", required=True, max_length=100)


class EditProject(forms.Form):
    new_project_title = forms.CharField(label="new_project_title", required=True, max_length=100)


class NewNote(forms.Form):
    note_title = forms.CharField(label="note_title", required=True, max_length=100)
    note_text = forms.CharField(label="note_text", required=False, max_length=1000, widget=forms.Textarea)
    vid_url = forms.CharField(label="note_title", max_length=200, required=False)


class EditNote(forms.Form):
    new_note_title = forms.CharField(label="note_title", required=True, max_length=100)
    new_note_text = forms.CharField(label="note_text", required=False, max_length=1000, widget=forms.Textarea)
    new_vid_url = forms.CharField(label="note_title", max_length=200, required=False)

