import os
import json
from django.core.management.base import BaseCommand
from content.admin import GenreResource

class Command(BaseCommand):
    help = 'Export data to a JSON file.'

    def handle(self, *args, **kwargs):
        try:
            self.export_genres()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during export: {e}'))

    def export_genres(self):
        # Sicherstellen, dass das Verzeichnis existiert
        os.makedirs('data', exist_ok=True)

        # Daten exportieren
        dataset = GenreResource().export()
        
        # Pfad zur Export-Datei
        file_path = os.path.join('data', 'data_genres.json')

        # JSON-Daten in die Datei schreiben
        try:
            with open(file_path, 'w') as file:
                json.dump(dataset.dict, file, ensure_ascii=False, indent=4)

            self.stdout.write(self.style.SUCCESS(f'Data successfully exported to {file_path}'))
        
        except IOError as e:
            self.stdout.write(self.style.ERROR(f'File write error: {e}'))