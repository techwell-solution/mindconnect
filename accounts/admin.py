from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import User, ClientProfile, CounsellorProfile

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_verified",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "MindConnect",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "is_verified",
                )
            },
        ),
    )

admin.site.register(ClientProfile)
admin.site.register(CounsellorProfile)