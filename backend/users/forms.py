from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class SingupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'genre')
