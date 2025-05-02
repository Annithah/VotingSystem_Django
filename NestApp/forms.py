from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


#the following are the codes that will help the given form to be used in the register.html page
#the form will be used to create a new user in the system
#and the help_text will be removed from the form
#the help_text is the text that is shown below the field in the form, this means that the form will not show any help text to the user
#the help_text is removed to make the form look cleaner and more user friendly

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Remove help_text for each field
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
