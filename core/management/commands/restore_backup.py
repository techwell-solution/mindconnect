import sqlite3

from django.core.management.base import BaseCommand

from core.models import Services, CaseStudy, ProcessStep
from events.models import Event
from contacts.models import Contact


class Command(BaseCommand):
    help = "Restore data from db_backup.sqlite3"

    def handle(self, *args, **options):

        conn = sqlite3.connect("db_backup.sqlite3")
        cursor = conn.cursor()

        self.stdout.write(self.style.SUCCESS("Connected to backup database."))

        # -------------------------
        # SERVICES
        # -------------------------
        cursor.execute("SELECT * FROM core_services")
        rows = cursor.fetchall()

        restored = 0

        for row in rows:
            _, title, slug, short_description, description, image, icon, is_featured, is_active, created_at = row

            if not Services.objects.filter(slug=slug).exists():
                Services.objects.create(
                    title=title,
                    slug=slug,
                    short_description=short_description,
                    description=description,
                    image=image,
                    icon=icon,
                    is_featured=bool(is_featured),
                    is_active=bool(is_active),
                )
                restored += 1

        self.stdout.write(
            self.style.SUCCESS(f"Services restored: {restored}")
        )

        # -------------------------
        # CASE STUDIES
        # -------------------------
        cursor.execute("SELECT * FROM core_casestudy")
        rows = cursor.fetchall()

        restored = 0

        for row in rows:
            (
                _,
                title,
                slug,
                short_description,
                description,
                image,
                client_profile,
                challenge,
                approach,
                outcome,
                icon,
                status,
                is_featured,
                is_active,
                created_at,
            ) = row

            if not CaseStudy.objects.filter(slug=slug).exists():
                CaseStudy.objects.create(
                    title=title,
                    slug=slug,
                    short_description=short_description,
                    description=description,
                    image=image,
                    client_profile=client_profile,
                    challenge=challenge,
                    approach=approach,
                    outcome=outcome,
                    icon=icon,
                    status=status,
                    is_featured=bool(is_featured),
                    is_active=bool(is_active),
                )
                restored += 1

        self.stdout.write(
            self.style.SUCCESS(f"Case Studies restored: {restored}")
        )

        # -------------------------
        # PROCESS STEPS
        # -------------------------
        cursor.execute("SELECT * FROM core_processstep")
        rows = cursor.fetchall()

        restored = 0

        for row in rows:
            _, title, description, order, is_active = row

            if not ProcessStep.objects.filter(
                title=title,
                order=order,
            ).exists():
                ProcessStep.objects.create(
                    title=title,
                    description=description,
                    order=order,
                    is_active=bool(is_active),
                )
                restored += 1

        self.stdout.write(
            self.style.SUCCESS(f"Process Steps restored: {restored}")
        )

        # -------------------------
        # EVENTS
        # -------------------------
        cursor.execute("SELECT * FROM events_event")
        rows = cursor.fetchall()

        restored = 0

        for row in rows:
            (
                _,
                title,
                slug,
                short_description,
                description,
                image,
                event_date,
                start_time,
                end_time,
                venue,
                registration_link,
                button_text,
                is_active,
                created_at,
            ) = row

            if not Event.objects.filter(slug=slug).exists():
                Event.objects.create(
                    title=title,
                    slug=slug,
                    short_description=short_description,
                    description=description,
                    image=image,
                    event_date=event_date,
                    start_time=start_time,
                    end_time=end_time,
                    venue=venue,
                    registration_link=registration_link,
                    button_text=button_text,
                    is_active=bool(is_active),
                )
                restored += 1

        self.stdout.write(
            self.style.SUCCESS(f"Events restored: {restored}")
        )

        # -------------------------
        # CONTACTS
        # -------------------------
        cursor.execute("SELECT * FROM contacts_contact")
        rows = cursor.fetchall()

        restored = 0

        for row in rows:
            (
                _,
                full_name,
                email,
                phone,
                subject,
                message,
                status,
                created_at,
                updated_at,
            ) = row

            if not Contact.objects.filter(
                email=email,
                subject=subject,
            ).exists():
                Contact.objects.create(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message,
                    status=status,
                )
                restored += 1

        self.stdout.write(
            self.style.SUCCESS(f"Contacts restored: {restored}")
        )

        conn.close()

        self.stdout.write(
            self.style.SUCCESS("✅ Backup restoration completed successfully!")
        )