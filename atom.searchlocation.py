import os
import xml.etree.ElementTree as ET

def parse_atom_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Error parsing file {file_path}: {e}")
        return None

def get_event_data(entry, namespace):
    title = entry.find('atom:title', namespace).text
    link = entry.find('atom:link', namespace).get('href')
    published = entry.find('atom:updated', namespace).text
    coordinates = entry.find('georss:point', namespace).text
    elevation = entry.find('georss:elev', namespace).text

    location_parts = title.split(' - ')
    if len(location_parts) > 1:
        city_place = location_parts[-1].split(', ')
        if len(city_place) == 2:
            city = city_place[0] 
            place = city_place[1]  
        else:
            city, place = '', ''  
    else:
        city, place = '', ''

    age = None
    for category in entry.findall('atom:category', namespace):
        if category.get('label') == 'Age':
            age = category.get('term')

    magnitude = None
    for category in entry.findall('atom:category', namespace):
        if category.get('label') == 'Magnitude':
            magnitude = category.get('term')

    event_data = {
        'title': title,
        'link': link,
        'published': published,
        'coordinates': coordinates,
        'elevation': elevation,
        'age': age,
        'magnitude': magnitude,
        'city': city,
        'place': place
    }

    return event_data

def search_atom_files(folder_path, search_place):
    namespace = {'atom': 'http://www.w3.org/2005/Atom', 'georss': 'http://www.georss.org/georss'}
    matching_entries = [] 

    with open('displayfiles\\display_search_results.txt', 'w') as result_file:
        for filename in os.listdir(folder_path):
            if filename.endswith('.atom'):
                file_path = os.path.join(folder_path, filename)
                root = parse_atom_file(file_path)

                if root is not None:
                    result_file.write("\n\nThe following took place in " + search_place + "\n")
                    result_file.write("=" * 40 + "\n\n")
                    result_file.write(f"File path data was retrieved from: {file_path}\n")
                    result_file.write("-" * 40 + "\n\n")
                    result_file.write("All matching entries:\n")
                    result_file.write("*" * 40 + "\n\n")

                    matching_entries.clear()
                    for entry in root.findall('atom:entry', namespace):
                        event_data = get_event_data(entry, namespace)
                        
                        if search_place.lower() == event_data['place'].lower():
                            matching_entries.append(event_data)

                
                    if matching_entries:
                        for entry_data in matching_entries:
                            result_file.write(f"Title: {entry_data['title']}\n")
                            result_file.write(f"ID: {entry_data['link']}\n")
                            result_file.write(f"Published: {entry_data['published']}\n")
                            result_file.write(f"Coordinates: {entry_data['coordinates']}\n")
                            result_file.write(f"Elevation/Depth: {entry_data['elevation']}\n")
                            result_file.write(f"Occurred: {entry_data['age']}\n")
                            result_file.write(f"Magnitude: {entry_data['magnitude']}\n")
                            result_file.write("-" * 120 + "\n")
                    else:
                        result_file.write("No matching entries found.\n")

                    
                    result_file.write("*" * 40 + "\n")

    print(f"Search results written to 'displayfiles\\display_search_results.txt'")

def main():
    folder_path = '25-01-28'  
    search_place = input("Enter the place (city) to search for: ").strip()

    search_atom_files(folder_path, search_place)

if __name__ == "__main__":
    main()
