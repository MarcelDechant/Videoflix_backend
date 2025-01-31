import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import all data (videos, genres, and users) using their respective commands.'

    def handle(self, *args, **kwargs):
        try:
            # import_videos
            self.import_data('import_videos')

            # import_genres
            self.import_data('import_genres')

            # import_users
            self.import_data('import_users')

            self.stdout.write(self.style.SUCCESS('All imports completed successfully.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during import: {e}'))

    def import_data(self, command):
        """Import data using the specified command."""
        result = subprocess.run(
            ['python', 'manage.py', command],
            capture_output=True,  # Capture both stdout and stderr
            text=True              # Return stdout and stderr as strings (instead of bytes)
        )

        # Prüfen, ob der Befehl erfolgreich war
        if result.returncode != 0:
            raise Exception(f"Error during {command}:\n{result.stderr}")

        self.stdout.write(self.style.SUCCESS(f'{command.replace("import_", "").capitalize()} import successful.'))
        self.stdout.write(self.style.NOTICE(f'Output: {result.stdout}'))