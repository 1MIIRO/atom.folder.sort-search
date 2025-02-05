import os
import xml.etree.ElementTree as ET
import re

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
    entry_id = entry.find('atom:id', namespace).text
    updated = entry.find('atom:updated', namespace).text
    coordinates = entry.find('georss:point', namespace).text
    elevation = entry.find('georss:elev', namespace).text

    magnitude = None
    match = re.search(r'M\s*([\d.]+)', title)
    if match:
        magnitude = float(match.group(1))  

    age = None
    for category in entry.findall('atom:category', namespace):
        if category.get('label') == 'Age':
            age = category.get('term')

    event_data = f"Title: {title}\nID: {entry_id}\nPublished: {updated}\nCoordinates: {coordinates}\nElevation/Depth: {elevation}\nOccurred: {age if age else 'N/A'}\nMagnitude: {magnitude if magnitude else 'N/A'}\n{'-'*120}"
    return title, event_data, magnitude

def check_magnitude(magnitude, search_type):
    try:
        if search_type.startswith('='):
            return magnitude == float(search_type[1:])
        elif search_type.startswith('<'):
           
            if search_type.startswith('<=' ):
                return magnitude <= float(search_type[2:])
            return magnitude < float(search_type[1:])
        elif search_type.startswith('>'):
            
            if search_type.startswith('>='):
                return magnitude >= float(search_type[2:])
            return magnitude > float(search_type[1:])
        else:
           
            return magnitude == float(search_type)
    except ValueError:
        return False


def search_atom_files(folder_path, search_type):
    matching_entries = []  

    namespace = {'atom': 'http://www.w3.org/2005/Atom', 'georss': 'http://www.georss.org/georss'}

    with open('displayfiles\\display_search_results.txt', 'w') as result_file:
        for filename in os.listdir(folder_path):
            if filename.endswith('.atom'):
                file_path = os.path.join(folder_path, filename)
                root = parse_atom_file(file_path)

                if root is not None:
                    result_file.write("\n\nThe following are of magnitude " + search_type + "\n")
                    result_file.write("="*40 + "\n\n")
                    result_file.write(f"File path data was retrieved from: {file_path}\n")
                    result_file.write("-" * 40 + "\n\n")
                    result_file.write("All matching entries:\n")
                    result_file.write("*" * 40 + "\n\n")

                  
                    for entry in root.findall('atom:entry', namespace):
                        _, event_data, magnitude = get_event_data(entry, namespace)

                        if magnitude is not None and check_magnitude(magnitude, search_type):
                            matching_entries.append(event_data)

                   
                    if matching_entries:
                        for entry_data in matching_entries:
                            result_file.write(entry_data + "\n")
                    else:
                        result_file.write("No matching entries found.\n")

                    result_file.write("*" * 40 + "\n")

    print(f"Search results written to 'displayfiles\\display_search_results.txt'")


def main():
    folder_path = '25-01-28'  
    search_type = input("Enter the magnitude size or range (e.g., 1.5, >2, <=3.0): ").strip()

    
    if not is_valid_input(search_type):
        print("Invalid input. Please enter a valid magnitude or range.")
        return

    
    search_atom_files(folder_path, search_type)


def is_valid_input(input_str):
    """ Check if input is within acceptable magnitude ranges """
    valid_ranges = ["<", ">", "<=", ">=", "="]
    if input_str[0] in valid_ranges:
        try:
            float(input_str[1:])
            return True
        except ValueError:
            return False
    else:
        try:
            float(input_str)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    main()
