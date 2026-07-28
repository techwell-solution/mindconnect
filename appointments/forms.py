from django import forms
from .models import Session, JournalEntry, ProgressGoal


class SessionForm(forms.ModelForm):

    class Meta:
        model = Session

        fields = [
            "session_type",
            "session_mode",
            "appointment_date",
            "appointment_time",
            "notes",
        ]

        widgets = {
            "appointment_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "appointment_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 4}
            ),
        }

class JournalEntryForm(forms.ModelForm):

    class Meta:
        model = JournalEntry
        fields = [
            "title",
            "mood",
            "content",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Give your journal entry a title..."
            }),

            "mood": forms.Select(attrs={
                "class": "form-control"
            }),

            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 10,
                "placeholder": "How are you feeling today?"
            }),
        }

class ProgressGoalForm(forms.ModelForm):

    class Meta:
        model = ProgressGoal
        exclude = ["user", "created_at"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "progress-input",
                "placeholder": "Goal title"
            }),

            "description": forms.Textarea(attrs={
                "class": "progress-textarea",
                "rows": 4,
                "placeholder": "Describe your goal"
            }),

            "target_date": forms.DateInput(attrs={
                "class": "progress-input",
                "type": "date"
            }),

            "progress": forms.NumberInput(attrs={
                "class": "progress-input",
                "min": 0,
                "max": 100
            }),

            "status": forms.Select(attrs={
                "class": "progress-input"
            }),
        }
