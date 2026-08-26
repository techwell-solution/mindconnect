from django.db import models

# Create your models here.
class Testimonial(models.Model):
    name = models.CharField(max_length=100)

    position = models.CharField(
        max_length=150,
        blank=True,
        help_text="Example: Individual Therapy, Anxiety Therapy, Couple's Therapy"
    )

    message = models.TextField()

    photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True
    )

    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ],
        default=5
    )

    is_featured = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name