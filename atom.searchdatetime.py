import os
import xml.etree.ElementTree as ET
from datetime import datetime
import dateutil.parser

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

    age = None
    for category in entry.findall('atom:category', namespace):
        if category.get('label') == 'Age':
            age = category.get('term')

    magnitude = None
    for category in entry.findall('atom:category', namespace):
        if category.get('label') == 'Magnitude':
            magnitude = category.get('term')

    event_data = f"Title: {title}\nID: {entry_id}\nPublished: {updated}\nCoordinates: {coordinates}\nElevation/Depth: {elevation}\nOccurred: {age if age else 'N/A'}\nMagnitude: {magnitude if magnitude else 'N/A'}\n{'-'*120}"
    return updated, event_data

def parse_date(date_str):
    try:
        return dateutil.parser.parse(date_str).date()
    except ValueError:
        return None

def parse_time(time_str):
    try:
        return dateutil.parser.parse(time_str).time()
    except ValueError:
        return None

def search_atom_files(folder_path, date_range_start, date_range_end, time_range_start, time_range_end):
    matching_entries = []
    namespace = {'atom': 'http://www.w3.org/2005/Atom', 'georss': 'http://www.georss.org/georss'}

    # Open file with UTF-8 encoding to avoid UnicodeEncodeError
    with open('displayfiles\\display_search_results.txt', 'w', encoding='utf-8') as result_file:
        for filename in os.listdir(folder_path):
            if filename.endswith('.atom'):
                file_path = os.path.join(folder_path, filename)
                root = parse_atom_file(file_path)

                if root is not None:
                    result_file.write(f"\n\nThe following are of Time range {time_range_start} and {time_range_end}\n")
                    result_file.write("=" * 40 + "\n\n")
                    result_file.write(f"File path data was retrieved from: {file_path}\n")
                    result_file.write("-" * 40 + "\n\n")
                    result_file.write("All matching entries:\n")
                    result_file.write("*" * 40 + "\n\n")

                    matching_entries.clear()

                    for entry in root.findall('atom:entry', namespace):
                        updated, event_data = get_event_data(entry, namespace)

                        entry_date = updated.split('T')[0]
                        entry_time = updated.split('T')[1].split('Z')[0]

                        # Date Range Logic
                        entry_datetime = parse_date(entry_date)
                        if date_range_start and date_range_end:
                            if not (date_range_start <= entry_datetime <= date_range_end):
                                continue

                        # Time Range Logic
                        entry_time_obj = parse_time(entry_time)
                        if entry_time_obj:
                            if time_range_start and time_range_end:
                                if not (time_range_start <= entry_time_obj <= time_range_end):
                                    continue
                            
                        matching_entries.append(event_data)

                    if matching_entries:
                        for entry_data in matching_entries:
                            result_file.write(entry_data + "\n")
                    else:
                        result_file.write("No matching entries found.\n")

                    result_file.write("*" * 40 + "\n")

    print(f"Search results written to 'displayfiles\\display_search_results.txt'")

def main():
    folder_path = '25-02-04'  
    search_type = input("Choose search type:\n1. Search by Date Range\n2. Search by Time Range\n3. Search by Both Date and Time Range\nEnter choice (1/2/3): ")

    if search_type == '1':
        date_range_start = input("Enter start date (YYYY-MM or YYYY-MM-DD): ")
        date_range_end = input("Enter end date (YYYY-MM or YYYY-MM-DD): ")
        date_range_start = parse_date(date_range_start)
        date_range_end = parse_date(date_range_end)
        if date_range_start and date_range_end:
            if date_range_start > date_range_end:
                print("Invalid date range: Start date cannot be after end date.")
                return
        search_atom_files(folder_path, date_range_start, date_range_end, None, None)

    elif search_type == '2':
        # Time range search
        time_range_start = input("Enter start time (HH or HH:MM): ")
        time_range_end = input("Enter end time (HH or HH:MM): ")
        time_range_start = parse_time(time_range_start)
        time_range_end = parse_time(time_range_end)
        if time_range_start and time_range_end:
            if time_range_start > time_range_end:
                print("Invalid time range: Start time cannot be after end time.")
                return
        search_atom_files(folder_path, None, None, time_range_start, time_range_end)

    elif search_type == '3':
        # Date and time range search
        date_range_start = input("Enter start date (YYYY-MM or YYYY-MM-DD): ")
        date_range_end = input("Enter end date (YYYY-MM or YYYY-MM-DD): ")
        time_range_start = input("Enter start time (HH or HH:MM): ")
        time_range_end = input("Enter end time (HH or HH:MM): ")

        date_range_start = parse_date(date_range_start)
        date_range_end = parse_date(date_range_end)
        time_range_start = parse_time(time_range_start)
        time_range_end = parse_time(time_range_end)

        if date_range_start and date_range_end:
            if date_range_start > date_range_end:
                print("Invalid date range: Start date cannot be after end date.")
                return

        if time_range_start and time_range_end:
            if time_range_start > time_range_end:
                print("Invalid time range: Start time cannot be after end time.")
                return

        search_atom_files(folder_path, date_range_start, date_range_end, time_range_start, time_range_end)

if __name__ == "__main__":
    main()
