from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"you@example.com"}))
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.widget.attrs.update({"class":"form-control"})
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit: user.save()
        return user
class UploadDocumentForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept":".pdf,.txt"}))
    def clean_file(self):
        file = self.cleaned_data["file"]
        extension = file.name.lower().rsplit(".", 1)[-1] if "." in file.name else ""
        if extension not in {"pdf", "txt"}: raise forms.ValidationError("Only PDF and TXT files are supported.")
        if file.size > 10 * 1024 * 1024: raise forms.ValidationError("Maximum file size is 10 MB.")
        return file
class AskQuestionForm(forms.Form):
    message = forms.CharField(max_length=6000, widget=forms.Textarea(attrs={"rows":1, "placeholder":"Ask a study or coding question...", "autocomplete":"off"}))
