from django.db import models
from django.utils.text import slugify

# Create your models here.
class Services(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    short_description = models.CharField(max_length=200, default="Professional counselling service.")
    description = models.TextField()
    image = models.URLField()
    icon = models.CharField(max_length=50, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=200, default="Professional case study.")
    description = models.TextField()
    image = models.URLField()
    client_profile = models.TextField()
    challenge = models.TextField()
    approach = models.TextField(help_text="Enter each point on a new line.")
    outcome = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    status = models.CharField(
    max_length=20,
    choices=[
        ("draft", "Draft"),
        ("published", "Published"),
    ],default="draft",)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"

    def approach_list(self):
        return [
            item.strip() 
            for item in self.approach.split("\n") 
            if item.strip()
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

