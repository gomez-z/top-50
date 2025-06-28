import re
import sys
import unicodedata

class TextFileParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}

    def parse_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
            for idx in range(0, len(lines), 3):
                group = lines[idx:idx+3]
                # Strip any character that is not a number for group[0]
                group[0] = re.sub(r'\D', '', group[0])
                # Normalize retaurant titles to remove accents and diacritics
                group[1] = ''.join(
                    c for c in unicodedata.normalize('NFKD', group[1])
                    if not unicodedata.combining(c)
                )
                # Higlight The BOTB for the year
                if group[0] == '1':
                    group[0] = 'BOTB'
                self.data[idx // 3] = group

    def append_to_column(self, column_index, append_str):
        for key, group in self.data.items():
            if column_index < len(group):
                group[column_index] = f"{append_str} - {group[column_index]}"

    def swap_columns(self, col1_index, col2_index):
        for group in self.data.values():
            if col1_index < len(group) and col2_index < len(group):
                group[col1_index], group[col2_index] = group[col2_index], group[col1_index]

    def extract_year_from_filepath(self):
        match = re.search(r'(19|20)\d{2}', self.filepath)
        return match.group(0) if match else None

    def get_data(self):
        return list(self.data.values())
    
def parse_and_format(filepath):
    parser = TextFileParser(filepath)
    parser.parse_file()
    year = parser.extract_year_from_filepath()
    parser.append_to_column(0, year)
    parser.swap_columns(0, 1)
    parser.swap_columns(1, 2)
    return parser.get_data()

if __name__ == "__main__":
    data = parse_and_format('InputData/Top 100 2024.txt')
    print(data)
           
