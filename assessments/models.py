from django.db import models
from django.conf import settings

# Create your models here.
class PHQ9Assessment(models.Model):
    RESPONSES = [
        (0, "Not at all"),
        (1, "Several days"),
        (2, "More than half the days"),
        (3, "Nearly every day"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="phq9_assessments"
    )

    q1 = models.IntegerField(choices=RESPONSES)
    q2 = models.IntegerField(choices=RESPONSES)
    q3 = models.IntegerField(choices=RESPONSES)
    q4 = models.IntegerField(choices=RESPONSES)
    q5 = models.IntegerField(choices=RESPONSES)
    q6 = models.IntegerField(choices=RESPONSES)
    q7 = models.IntegerField(choices=RESPONSES)
    q8 = models.IntegerField(choices=RESPONSES)
    q9 = models.IntegerField(choices=RESPONSES)

    total_score = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        return (
            self.q1 + self.q2 + self.q3 +
            self.q4 + self.q5 + self.q6 +
            self.q7 + self.q8 + self.q9
        )

    def interpretation(self):
        score = self.total_score

        if score <= 4:
            return "Minimal Depression"

        elif score <= 9:
            return "Mild Depression"

        elif score <= 14:
            return "Moderate Depression"

        elif score <= 19:
            return "Moderately Severe Depression"

        return "Severe Depression"

    def save(self, *args, **kwargs):
        self.total_score = self.calculate_score()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - PHQ-9 ({self.total_score})"

class GAD7Assessment(models.Model):
    CHOICES = [
        (0, "Not at all"),
        (1, "Several days"),
        (2, "More than half the days"),
        (3, "Nearly every day"),
    ]

    DIFFICULTY_CHOICES = [
        ("not", "Not difficult at all"),
        ("somewhat", "Somewhat difficult"),
        ("very", "Very difficult"),
        ("extremely", "Extremely difficult"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    q1 = models.PositiveSmallIntegerField(choices=CHOICES)
    q2 = models.PositiveSmallIntegerField(choices=CHOICES)
    q3 = models.PositiveSmallIntegerField(choices=CHOICES)
    q4 = models.PositiveSmallIntegerField(choices=CHOICES)
    q5 = models.PositiveSmallIntegerField(choices=CHOICES)
    q6 = models.PositiveSmallIntegerField(choices=CHOICES)
    q7 = models.PositiveSmallIntegerField(choices=CHOICES)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        blank=True
    )

    total_score = models.PositiveSmallIntegerField(default=0)
    interpretation = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GAD-7 Assessment"
        verbose_name_plural = "GAD-7 Assessments"

    def calculate_score(self):
        return (
            self.q1 +
            self.q2 +
            self.q3 +
            self.q4 +
            self.q5 +
            self.q6 +
            self.q7
        )

    def get_interpretation(self):
        if self.total_score <= 4:
            return "Minimal Anxiety"
        elif self.total_score <= 9:
            return "Mild Anxiety"
        elif self.total_score <= 14:
            return "Moderate Anxiety"
        return "Severe Anxiety"

    def save(self, *args, **kwargs):
        self.total_score = self.calculate_score()
        self.interpretation = self.get_interpretation()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.total_score}/21"

class StressAssessment(models.Model):
    INTERPRETATION_CHOICES = [
        ("Minimal Stress", "Minimal Stress"),
        ("Mild Stress", "Mild Stress"),
        ("Moderate Stress", "Moderate Stress"),
        ("High Stress", "High Stress"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stress_assessments"
    )

    q1 = models.PositiveSmallIntegerField()
    q2 = models.PositiveSmallIntegerField()
    q3 = models.PositiveSmallIntegerField()
    q4 = models.PositiveSmallIntegerField()
    q5 = models.PositiveSmallIntegerField()
    q6 = models.PositiveSmallIntegerField()
    q7 = models.PositiveSmallIntegerField()
    q8 = models.PositiveSmallIntegerField()
    q9 = models.PositiveSmallIntegerField()
    q10 = models.PositiveSmallIntegerField()

    total_score = models.PositiveSmallIntegerField(default=0)
    interpretation = models.CharField(
        max_length=30,
        choices=INTERPRETATION_CHOICES,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Stress Assessment"
        verbose_name_plural = "Stress Assessments"

    def __str__(self):
        return f"{self.user.username} - {self.total_score}"

    def save(self, *args, **kwargs):
        self.total_score = (
            self.q1 +
            self.q2 +
            self.q3 +
            self.q4 +
            self.q5 +
            self.q6 +
            self.q7 +
            self.q8 +
            self.q9 +
            self.q10
        )

        if self.total_score <= 7:
            self.interpretation = "Minimal Stress"
        elif self.total_score <= 14:
            self.interpretation = "Mild Stress"
        elif self.total_score <= 21:
            self.interpretation = "Moderate Stress"
        else:
            self.interpretation = "High Stress"

        super().save(*args, **kwargs)