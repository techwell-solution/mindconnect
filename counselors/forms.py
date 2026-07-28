from django import forms
from .models import SessionNote


class SessionNoteForm(forms.ModelForm):

    class Meta:
        model = SessionNote
        exclude = (
            "session",
            "counsellor",
            "created_at",
            "updated_at",
        )

        widgets = {
            "diagnosis": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Diagnosis (optional)"
            }),

            "observations": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Write your observations..."
            }),

            "interventions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Therapeutic interventions used..."
            }),

            "recommendations": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Recommendations for the client..."
            }),

            "next_session_plan": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Plan for the next session..."
            }),

            "is_private": forms.CheckboxInput(attrs={
                "class": "checkbox"
            }),
        }