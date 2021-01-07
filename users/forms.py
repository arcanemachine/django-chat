from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class ChatUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data['username']) < 3:
            raise ValidationError(
                "Usernames must contain 3 or more characters.")
        return cleaned_data
