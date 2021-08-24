from django import forms


class RejectPostForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    delete_after = forms.IntegerField()
