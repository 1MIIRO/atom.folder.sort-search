import os
import xml.etree.ElementTree as ET

def write_matching_entries(results, search_option, user_input):
    with open('displayfiles\\display_search_results.txt', 'w') as file:
        if search_option == 'date':
            file.write(f"\nThe following took place on {user_input}\n")
        elif search_option == 'time':
            file.write(f"\nThe following took place at {user_input}\n")
        elif search_option == 'both':
            file.write(f"\nThe following took place on {user_input}\n")
        
        file.write("\n=========================================\n")
        
        for result in results:
            file.write(f"File path data was retrieved from: {result['file_path']}\n")
            file.write("\n----------------------------------------\n")
            file.write("All matching entries\n")
            file.write("***************************************\n")
            
            for entry in result['entries']:
                file.write(f"Title: {entry['title']}\n")
                file.write(f"ID: {entry['id']}\n")
                file.write(f"Published: {entry['published']}\n")
                file.write(f"Coordinates: {entry['coordinates']}\n")
                file.write(f"Elevation/Depth: {entry['elevation']}\n")
                file.write(f"Occurred: {entry['age']}\n")
                file.write(f"Magnitude: {entry['magnitude']}\n")
                file.write("-" * 120 + "\n")

def search_atom_files(folder_path, search_option, user_input):
    results = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.atom'):
            file_path = os.path.join(folder_path, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            namespace = {'atom': 'http://www.w3.org/2005/Atom', 'georss': 'http://www.georss.org/georss'}
            
            matching_entries = []
            
            for entry in root.findall('atom:entry', namespace):
                updated = entry.find('atom:updated', namespace).text
                date, time = updated.split('T')
                
                if search_option == 'date' and date.startswith(user_input):
                    matching_entries.append(parse_entry(entry, namespace))
                elif search_option == 'time' and time.startswith(user_input):
                    matching_entries.append(parse_entry(entry, namespace))
                elif search_option == 'both' and (date.startswith(user_input[:10]) and time.startswith(user_input[11:])):
                    matching_entries.append(parse_entry(entry, namespace))

            if matching_entries:
                results.append({
                    'file_path': file_path,
                    'entries': matching_entries
                })
    
  
    if results:
        write_matching_entries(results, search_option, user_input)
    else:
        print("No matching entries found.")

def parse_entry(entry, namespace):
    title = entry.find('atom:title', namespace).text
    id = entry.find('atom:id', namespace).text
    published = entry.find('atom:updated', namespace).text
    coordinates = entry.find('georss:point', namespace).text
    elevation = entry.find('georss:elev', namespace).text

    age = None
    magnitude = None
    for category in entry.findall('atom:category', namespace):
        if category.get('label') == 'Age':
            age = category.get('term')
        if category.get('label') == 'Magnitude':
            magnitude = category.get('term')

    return {
        'title': title,
        'id': id,
        'published': published,
        'coordinates': coordinates,
        'elevation': elevation,
        'age': age,
        'magnitude': magnitude
    }


def get_user_input_and_search():
    folder_path = '25-01-28'

    print("Choose your search option:")
    print("1. Search by Date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    print("2. Search by Time (HH, HH-MM)")
    print("3. Search by both Date and Time (YYYY-MM-DD-HH-MM)")
    choice = input("Enter 1, 2, or 3: ")

    if choice == '1':
        search_option = 'date'
        user_input = input("Enter the date (YYYY, YYYY-MM, or YYYY-MM-DD): ")
    elif choice == '2':
        search_option = 'time'
        user_input = input("Enter the time (HH or HH-MM): ")
    elif choice == '3':
        search_option = 'both'
        user_input = input("Enter the combined date and time (YYYY-MM-DD-HH-MM): ")
    else:
        print("Invalid choice. Exiting.")
        return

    search_atom_files(folder_path, search_option, user_input)

get_user_input_and_search()
