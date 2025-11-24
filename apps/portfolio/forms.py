from django import forms
#from django_recaptcha.fields import ReCaptchaField, ReCaptchaV2Checkbox

class ContactForm(forms.Form):
    your_name = forms.CharField(
        label='Tu nombre',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu nombre',
                'class': 'form-control',
                'id': 'your_name',  # opcional
            }
        ),
        required=True
    )

    your_email = forms.EmailField(
        label='Tu email',
        widget=forms.EmailInput(            # mejor EmailInput
            attrs={
                'placeholder': 'Tu email',
                'class': 'form-control',
                'id': 'your_email',        # opcional
            }
        ),
        required=True
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Asunto',
                'class': 'form-control',
                'id': 'subject',
            }
        ),
        required=True
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Mensaje',
                'class': 'form-control',
                'rows': '5',
                'id': 'message',          # si quieres
            }
        ),
        required=True
    )
