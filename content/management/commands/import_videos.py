import os
from django.core.management.base import BaseCommand
from content.admin import VideoResource
from tablib import Dataset

class Command(BaseCommand):
    help = 'Import data from a JSON file.'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('data', 'data_videos.json')

        # Überprüfen, ob die Datei existiert
        if not self.is_valid_file(file_path):
            return

        try:
            # Datei lesen und Daten importieren
            json_data = self.read_file(file_path)
            self.import_data(json_data)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during import: {str(e)}'))

    def is_valid_file(self, file_path):
        """Überprüft, ob die Datei existiert und ein gültiger JSON-Dateipfad ist."""
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} does not exist.'))
            return False
        return True

    def read_file(self, file_path):
        """Liest den Inhalt der Datei und gibt den JSON-Text zurück."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except IOError as e:
            self.stdout.write(self.style.ERROR(f'Error reading file {file_path}: {str(e)}'))
            raise  # Fehler erneut auslösen, damit die Verarbeitung gestoppt wird

    def import_data(self, json_data):
        """Lädt die JSON-Daten in ein Dataset und importiert sie."""
        try:
            # Dataset erstellen und JSON-Daten laden
            dataset = Dataset().load(json_data, format='json')

            video_resource = VideoResource()
            result = video_resource.import_data(dataset, raise_errors=False)  # Fehler nicht automatisch auslösen

            # Ergebnisse prüfen und entsprechende Ausgabe geben
            if result.has_errors():
                error_count = len(result.errors)
                self.stdout.write(self.style.ERROR(f'Import completed with {error_count} errors.'))
            else:
                self.stdout.write(self.style.SUCCESS('Data successfully imported from JSON file.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during data import: {str(e)}'))