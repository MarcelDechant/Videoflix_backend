import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Export all data (videos, genres, and users) using their respective commands.'

    def handle(self, *args, **kwargs):
        commands = [
            ('export_videos', 'Videos export successful.'),
            ('export_genres', 'Genres export successful.'),
            ('export_users', 'Users export successful.')
        ]
        
        try:
            for command, success_message in commands:
                result = subprocess.run(['python', 'manage.py', command], check=True, capture_output=True, text=True)

                self.stdout.write(self.style.SUCCESS(success_message))

            self.stdout.write(self.style.SUCCESS('All exports completed successfully.'))

        except subprocess.CalledProcessError as e:
            
            self.stdout.write(self.style.ERROR(f'Error during export: {e.stderr}'))

        except Exception as e:
            
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))