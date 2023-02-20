import os
import sys
import hashlib
import csv

def find_duplicates(directory):
    # Create a dictionary to store file hashes and paths
    files_dict = {}

    # Create a counter for the duplicate ID
    id_counter = 1
    count = 1

    # Iterate through all the files in the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            
            count += 1
            # Get the full path to the file
            path = os.path.join(root, filename)

            # Open the file and read its contents
            try:
                with open(path, 'rb') as f:
                    contents = f.read()
            except FileNotFoundError:
                # If the file can't be opened, skip it and move on to the next one
                continue

            # Calculate the SHA256 hash of the file contents
            file_hash = hashlib.sha256(contents).hexdigest()

            # If the hash already exists in the dictionary, it's a duplicate
            if file_hash in files_dict:
                existing_file = files_dict[file_hash]
                if os.path.getsize(existing_file) > 10240:

                    existing_size = round(os.path.getsize(existing_file) / 1048576, 2)
                    new_size = round(os.path.getsize(path) / 1048576, 2)
                    file_row = {'id': id_counter, 'path': path, 'size (MB)': new_size}
                    existing_row = {'id': id_counter, 'path': existing_file, 'size (MB)': existing_size}
                    rows = [file_row, existing_row]
                    write_to_csv(rows)
                    id_counter += 1

            else:
                # Otherwise, add the hash and path to the dictionary
                files_dict[file_hash] = path

            # Print the name of the file being processed
            sys.stdout.write(f"\rNumber of duplicated file(s) found / Total number of file(s): {id_counter-1} / {count}")
            sys.stdout.flush()

    # Sort the CSV by largest to smallest file size
    with open('duplicates.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        sorted_rows = sorted(reader, key=lambda row: float(row[2]), reverse=True)

    # Write the sorted rows back to the CSV
    with open('duplicates.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(sorted_rows)


def write_to_csv(rows):
    # Write the given rows to the CSV file
    with open('duplicates.csv', 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['id', 'path', 'size (MB)'])
        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    # Check that a directory argument was provided
    if len(sys.argv) != 2:
        print('Usage: python find_duplicates.py <directory>')
    else:
        directory = sys.argv[1]

        # Remove the CSV file if it already exists
        if os.path.exists('duplicates.csv'):
            os.remove('duplicates.csv')

        # Create the CSV file and write the header row
        with open('duplicates.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['id', 'path', 'size (MB)'])

        # Find the duplicates in the directory and write them to the CSV
        find_duplicates(directory)

        # Print a message indicating the location of the CSV file
        print(f'Duplicate files written to {os.path.abspath("duplicates.csv")}')
