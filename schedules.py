import csv
import os

class Schedule:
    def __init__(self, name, films):
        self.name = name
        self.films = [(film, 0, False) if isinstance(film, str) else film for film in films]
    
    def export_to_csv(self, filename=None, overwrite=False):
        """
        Export schedule titles to CSV file with header title
        uses schedule name with .csv extension
        Set overwrite=True to replace existing files
        """
        if filename is None:
            filename = f"CSVs/{self.name}.csv"
        

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        

        if not overwrite and os.path.exists(filename):
            return None
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title'])  # Header row as list
            for film in self.films:
                writer.writerow([film[0]])  # Title only as list
        return filename




films_test = [
    "The 400 Blows",
    "8½",
    "Aguirre, the Wrath of God",
    "Badlands",
    "The Battle of Algiers",
    "Beauty and the Beast",
    "Bicycle Thieves",
    "Breathless",
    "A Brighter Summer Day",
    "Chungking Express",
    "Close-Up",
    "Cléo from 5 to 7",
    "Contempt",
    "Days of Heaven",
    "Dogtooth",
    "Dogville",
    "The Double Life of Véronique",
    "Enter the Void",
    "Fanny and Alexander",
    "Fitzcarraldo",
    "Fox and His Friends",
    "The Great Beauty",
    "Harakiri",
    "The Holy Mountain",
    "Hour of the Wolf",
    "House",
    "I Am Cuba",
    "Ikiru",
    "In the Mood for Love",
    "Jules and Jim",
    "Kwaidan",
    "L'Atalante",
    "La Dolce Vita",
    "Le Bonheur",
    "Le Samouraï",
    "M",
    "Melancholia",
    "Paris, Texas",
    "The Passion of Joan of Arc",
    "Pather Panchali",
    "Pickpocket",
    "Rashomon",
    "The Seventh Seal",
    "Solaris",
    "Three Colours: Blue",
    "Tokyo Story",
    "The Tree of Life",
    "Wild Strawberries",
    "A Woman Under the Influence",
    "Yi Yi"
]

schedule_test = Schedule("Schedule_test", films_test)



# Add new ones here
schedules = [schedule_test]

for i in schedules:
    i.export_to_csv(overwrite=False)