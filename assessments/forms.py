from django import forms
from .models import PHQ9Assessment, GAD7Assessment, StressAssessment

QUESTIONS = {
    "q1": "Little interest or pleasure in doing things",
    "q2": "Feeling down, depressed, or hopeless",
    "q3": "Trouble falling or staying asleep, or sleeping too much",
    "q4": "Feeling tired or having little energy",
    "q5": "Poor appetite or overeating",
    "q6": "Feeling bad about yourself—or that you are a failure or have let yourself or your family down",
    "q7": "Trouble concentrating on things, such as reading the newspaper or watching television",
    "q8": "Moving or speaking so slowly that other people could have noticed? Or the opposite—being so fidgety or restless that you've been moving around a lot more than usual",
    "q9": "Thoughts that you would be better off dead or of hurting yourself in some way",
}

class PHQ9Form(forms.ModelForm):

    class Meta:
        model = PHQ9Assessment
        exclude = ["user", "total_score", "created_at"]

        widgets = {
            field: forms.RadioSelect
            for field in [
                "q1","q2","q3","q4","q5",
                "q6","q7","q8","q9"
            ]
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field, question in QUESTIONS.items():
            self.fields[field].label = question

class GAD7Form(forms.ModelForm):
    class Meta:
        model = GAD7Assessment
        exclude = [
            "user",
            "total_score",
            "interpretation",
            "created_at",
        ]

        widgets = {
            "q1": forms.RadioSelect,
            "q2": forms.RadioSelect,
            "q3": forms.RadioSelect,
            "q4": forms.RadioSelect,
            "q5": forms.RadioSelect,
            "q6": forms.RadioSelect,
            "q7": forms.RadioSelect,
            "difficulty": forms.RadioSelect,
        }

        labels = {
            "q1": "Feeling nervous, anxious, or on edge",
            "q2": "Not being able to stop or control worrying",
            "q3": "Worrying too much about different things",
            "q4": "Trouble relaxing",
            "q5": "Being so restless that it is hard to sit still",
            "q6": "Becoming easily annoyed or irritable",
            "q7": "Feeling afraid as if something awful might happen",
            "difficulty": (
                "If you checked off any problems, how difficult have these "
                "problems made it for you to do your work, take care of "
                "things at home, or get along with other people?"
            ),
        }
        
STRESS_CHOICES = [
    (0, "Not at all"),
    (1, "Several days"),
    (2, "More than half the days"),
    (3, "Nearly every day"),
]


class StressAssessmentForm(forms.ModelForm):

    class Meta:
        model = StressAssessment
        exclude = ["user", "total_score", "interpretation", "created_at"]

        widgets = {
            "q1": forms.RadioSelect(choices=STRESS_CHOICES),
            "q2": forms.RadioSelect(choices=STRESS_CHOICES),
            "q3": forms.RadioSelect(choices=STRESS_CHOICES),
            "q4": forms.RadioSelect(choices=STRESS_CHOICES),
            "q5": forms.RadioSelect(choices=STRESS_CHOICES),
            "q6": forms.RadioSelect(choices=STRESS_CHOICES),
            "q7": forms.RadioSelect(choices=STRESS_CHOICES),
            "q8": forms.RadioSelect(choices=STRESS_CHOICES),
            "q9": forms.RadioSelect(choices=STRESS_CHOICES),
            "q10": forms.RadioSelect(choices=STRESS_CHOICES),
        }

        labels = {
            "q1": "1. I felt overwhelmed by my responsibilities.",
            "q2": "2. I found it difficult to relax even when I had time to rest.",
            "q3": "3. I felt tense or unable to calm down.",
            "q4": "4. I had trouble sleeping because of worries or stress.",
            "q5": "5. I became easily irritated or frustrated.",
            "q6": "6. I found it hard to concentrate on my daily tasks.",
            "q7": "7. I felt mentally exhausted or drained.",
            "q8": "8. I worried excessively about work, school, family, or finances.",
            "q9": "9. I felt pressure to meet expectations from others.",
            "q10": "10. Stress affected my physical health (e.g., headaches, muscle tension, stomach discomfort, or fatigue).",
        }
