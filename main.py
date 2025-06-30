import TextFileParser  # Assuming TextFileParser is a module that provides the parse_file function
import os
import pickle
import csv
import geocoder
import yaml

def main():
    global API_KEY
    # Load configuration from YAML file
    with open('configuration.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    saved_table = config.get('pickle_file')
    current_year = config.get('current_year')
    api_key = config.get('google_api_key')
    if api_key:
        print("Google API key detected.")
        print("WARNING: Using Google API may incur costs!")

    # Load list of files in InputData directory
    txt_files = [f for f in os.listdir('InputData') if 'Top' in f and f.endswith('.txt')]

    # Check if pickle file exists, if so load it instead of starting fresh
    if os.path.exists(saved_table):
        with open(saved_table, 'rb') as f:
            hash_table = pickle.load(f)
        print(f"Loaded hash table from {saved_table}")
    else:
        # Pickle file doesn't exist, start fresh
        hash_table = {}

    # Go through every file and load all the data into a hash table
    for file in txt_files:
        print(f"Processing file: {file}")
        fileData = TextFileParser.parse_and_format(os.path.join('InputData', file))
        append_to_hash_table(fileData, hash_table, api_key)

    # print_hash_table(hash_table)
    export_hash_table_to_csv(hash_table, current_year, 'top100')
    # Save changes to the hash table
    save_hash_table(hash_table, saved_table)

def append_to_hash_table(fileData, table, api_key):
    for entry in fileData:
            key = entry[0]  # or another unique identifier
            # Need to account for 3 use cases: 1 = Not exist, add; 2 = Exist, but new year; 3 = Exist, duplicate
            if key in table:
                if entry[2] in table[key][2]: # 3. Duplicate
                    # print(f"Duplicate entry: {key}, {entry[2]}. Skipping")
                    continue
                else:  # 2. New Year
                    # Update the second column with the new entry
                    table[key][2] = f"{table[key][2]}, {entry[2]}"
  
                    # Split, sort by leading number descending, and join back
                    items = table[key][2].split(', ')
                    items.sort(key=lambda x: int(x.split()[0]) if x.split()[0].isdigit() else float('-inf'), reverse=True)
                    table[key][2] = ', '.join(items)
            else: # 1. Doesnt exist, geocode and add
                print(f"Adding new entry: {key}")
                address_str = f"{entry[0]}, {entry[1]}"
                formatted_address = geocoder.get_address(address_str, api_key)
                
                # We have added the address, now we append to entry and add to table
                if formatted_address:
                    entry.append(formatted_address)
                else:
                    print(f"Address not found on either API for {address_str}")
                    entry.append("AddressMissing")
                
                table[key] = entry

def save_hash_table(hash_table, filename):
    with open(filename, 'wb') as f:
        pickle.dump(hash_table, f)

def load_hash_table(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def print_hash_table(hash_table):
    # Print the hash table
    for key, value in hash_table.items():
        if isinstance(value, list):
            print(f"{key}: {', '.join(map(str, value))}")
        else:
            print(f"{key}: {value}")

def export_hash_table_to_csv(hash_table, year, filename='top100'):
    """
    Export the hash table to a CSV file.
    Each key-value pair is written as a row.
    """
    with open(filename + '_all.csv', 'w', newline='', encoding='utf-8') as csvall, open(
        filename + '_botb.csv', 'w', newline='', encoding='utf-8') as csvbotb, open(
            filename + '_current.csv', 'w', newline='', encoding='utf-8') as csvcurrent, open(
                filename + '_modern.csv', 'w', newline='', encoding='utf-8') as csvmodern, open(
                    filename + '_old.csv', 'w', newline='', encoding='utf-8') as csvold:

        # Create CSV writers for each file
        writer_all = csv.writer(csvall)
        writer_botb = csv.writer(csvbotb)
        writer_current = csv.writer(csvcurrent)
        writer_modern = csv.writer(csvmodern)
        writer_old = csv.writer(csvold)

        # Write headers
        writer_all.writerow(['Name', 'Detail', 'Address'])
        writer_botb.writerow(['Name', 'Detail', 'Address'])
        writer_current.writerow(['Name', 'Detail', 'Address'])
        writer_modern.writerow(['Name', 'Detail', 'Address'])
        writer_old.writerow(['Name', 'Detail', 'Address'])

        for key, value in hash_table.items():
            newest = value[2].split(' ')[0]  # Get latest entry
            row = [value[0], value[2], value[3]]
            writer_all.writerow(row)

            if "BOTB" in value[2]:
                writer_botb.writerow(row)
            elif str(newest) == str(year):
                writer_current.writerow(row)
            elif int(newest) > 2020:
                writer_modern.writerow(row)
            else:
                writer_old.writerow(row)

if __name__ == "__main__":
    main()
