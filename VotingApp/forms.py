from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

# Custom registration form with placeholders and no labels
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholder_names = {
            "username": "Enter username",
            "email": "Enter email address",
            "password1": "Enter password",
            "password2": "Confirm password"
        }

        for field_name, field in self.fields.items():
            field.label = ""
            field.help_text = ""
            field.widget.attrs.update({
                "placeholder": placeholder_names.get(field_name, ""),
                "class": "form-control",  # Add Bootstrap style class (optional)
            })

# Comment form with placeholder and no label
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].label = ""
        self.fields["text"].widget.attrs.update({
            "placeholder": "Write your comment here...",
            "class": "form-control",
            "rows": 3,
        })
