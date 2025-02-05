import os
import xml.etree.ElementTree as ET

def get_magnitude_entries(magnitude_option, files_path):
    magnitude_dict = {
        '0': ['Magnitude 0'],
        '>=0': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2', 'Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '>0': ['Magnitude 1', 'Magnitude 2', 'Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '1': ['Magnitude 1'],
        '>=1': ['Magnitude 1', 'Magnitude 2', 'Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '>1': ['Magnitude 2', 'Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '<=1': ['Magnitude 0', 'Magnitude 1'],
        '<1': ['Magnitude 0'],
        '2': ['Magnitude 2'],
        '>=2': ['Magnitude 2', 'Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '>2': ['Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '<=2': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2'],
        '<2': ['Magnitude 0', 'Magnitude 1'],
        '3': ['Magnitude 3'],
        '>=3': ['Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '>3': ['Magnitude 4', 'Magnitude 5'],
        '<=3': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2', 'Magnitude 3'],
        '<3': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2'],
        '4': ['Magnitude 4'],
        '>=4': ['Magnitude 4', 'Magnitude 5'],
        '>4': ['Magnitude 5'],
        '<=4': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2', 'Magnitude 3', 'Magnitude 4'],
        '<4': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2', 'Magnitude 3'],
        '5': ['Magnitude 5'],
        '<=5': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2', 'Magnitude 3', 'Magnitude 4', 'Magnitude 5'],
        '<5': ['Magnitude 0', 'Magnitude 1', 'Magnitude 2', 'Magnitude 3', 'Magnitude 4']
    }

    if magnitude_option not in magnitude_dict:
        return  

    valid_magnitudes = magnitude_dict[magnitude_option]
    all_entries = []

    for filename in os.listdir(files_path):
        if filename.endswith(".atom"):
            file_path = os.path.join(files_path, filename)

            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
            except ET.ParseError as e:
                continue

            namespace = {
                'atom': 'http://www.w3.org/2005/Atom',
                'georss': 'http://www.georss.org/georss'
            }

            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace).text
                link = entry.find('atom:link', namespace).get('href')
                published = entry.find('atom:updated', namespace).text
                coordinates = entry.find('georss:point', namespace).text
                elevation = entry.find('georss:elev', namespace).text

                age = None
                for category in entry.findall('atom:category', namespace):
                    if category.get('label') == 'Age':
                        age = category.get('term')

                magnitude = None
                for category in entry.findall('atom:category', namespace):
                    if category.get('label') == 'Magnitude':
                        magnitude = category.get('term')

                if magnitude in valid_magnitudes:
                    event_data = f"Title: {title}\nID: {link}\nPublished: {published}\nCoordinates: {coordinates}\nElevation/Depth: {elevation}\nOccurred: {age if age else 'N/A'}\nMagnitude: {magnitude if magnitude else 'N/A'}\n{'-'*120}"
                    all_entries.append((file_path, event_data))

    if not all_entries:
        return

    output_file = 'displayfiles//display_search_results.txt'
    with open(output_file, 'w') as file:
        file.write(f"\nThe following are of magnitude {magnitude_option}\n")
        file.write("="*50 + "\n")

        for file_path, entry_data in all_entries:
            file.write(f"\nFile path data was retrieved from: {file_path}\n")
            file.write("-"*40 + "\n")
            file.write(entry_data + "\n")
            file.write("*" * 40 + "\n")

magnitude_option = input("Enter the magnitude option (e.g., >=1, <3, etc.): ").strip()

folder_path = '25-01-28'  

get_magnitude_entries(magnitude_option, folder_path)
