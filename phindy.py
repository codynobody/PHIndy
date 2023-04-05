import os
import re

# Define PHI dictionary
phi_dict = {
    'SSN': r"\d{3}[-\s]?\d{2}[-\s]?(\d{4}|[xX]{4})",
    'DOB': r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    'PHONE': r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    'ADDRESS': r"\d+\s+([\w\s\.]+)\s+(?:street|st|avenue|ave|road|rd|blvd|way|hwy|drive|dr)\.?"
}

def find_phi(file_path, phi_dict, output_file):
    with open(file_path, 'r', encoding='utf8', errors='ignore') as file:
        file_contents = file.read()

        phi_count = {}
        for phi_type, phi_pattern in phi_dict.items():
            phi_matches = re.findall(phi_pattern, file_contents)
            phi_count[phi_type] = len(phi_matches)

        total_phi_count = sum(phi_count.values())
        if total_phi_count > 0:
            output_file.write(f"File: {file_path}\n")
            for phi_type, count in phi_count.items():
                if count > 0:
                    output_file.write(f"{phi_type}: {count}\n")
            output_file.write(f"Total PHI Count: {total_phi_count}\n\n")
        return phi_count

def search_directory(dir_path, phi_dict):
    phi_counts = {k: 0 for k in phi_dict.keys()}
    with open('phi_discovery.txt', 'w') as output_file:
        for dirpath, _, filenames in os.walk(dir_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if file_path.lower().endswith(('.txt', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.pdf', '.json')):
                    file_phi_counts = find_phi(file_path, phi_dict, output_file)
                    for phi_type, count in file_phi_counts.items():
                        phi_counts[phi_type] += count
    return phi_counts

def main():
    dir_path = input("Enter directory path: ")
    phi_counts = search_directory(dir_path, phi_dict)

    with open('phi_discovery.txt', 'r+') as output_file:
        current_content = output_file.read()
        output_file.seek(0, 0)
        output_file.write(f"SSN: {phi_counts['SSN']}\n")
        output_file.write(f"DOB: {phi_counts['DOB']}\n")
        output_file.write(f"PHONE: {phi_counts['PHONE']}\n")
        output_file.write(f"ADDRESS: {phi_counts['ADDRESS']}\n\n")
        output_file.write(current_content)

    print(f'SSN count: {phi_counts["SSN"]}')
    print(f'DOB count: {phi_counts["DOB"]}')
    print(f'Phone number count: {phi_counts["PHONE"]}')
    print(f'Address count: {phi_counts["ADDRESS"]}')
    print(f'Total PHI Record count: {sum(phi_counts.values())}')

if __name__ == "__main__":
    main()
