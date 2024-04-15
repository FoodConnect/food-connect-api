from allauth.user.adapter import DefaultAccountAdapter

class CustomUserAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.role = data.get('role')
        user.save()
        return user