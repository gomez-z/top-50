# Top 50 Restaurants

A curated application for discovering, managing, and reviewing the top 100 restaurants for every year since incpetion.  
Data source comes from here: https://www.theworlds50best.com/list/1-50.  
This repository parses data for every year and creates csv files that are designed to be imported into Google My Maps to obtain all restaurants in one convenient place

![Alt text](Top50.png?raw=true "NYC")

## Features

### 1. Data Source
- Data comes from txt files in InputData/
- Data is organized by year and pulled directly from webiste
- Because it was pulled directly, information is limited to name and city
- This is why some APIs struggle to return addresses

### 2. Output
- The program outputs 5 different csv files:
    - top100_all.csv = All restaurants
    - top100_botb.csv = Best Of The Best; #1 Restaurants
    - top100_current.csv = Restaurants of the current year
    - top100_modern.csv = Restaurants between 2021 and current year
    - top100_old.csv = Restaurants older than 2021
- Note: There is no guarantee that restaurant in list is still open or still good! Do your own research  before travelling.

### 3. CSV Structure
- There are three columns in each csv
    - Name - Restaurant Name
    - Detail - Honors; *Year - Rank*
    - Address - Geocoded address ready to map

### 4. Program Structure
- The program will parse every txt file in InputData and add data for every entry into a hash table where the restaurant name is the key
   - If the key doesnt exist, it will geocode using the name and city and add all the data
   - If the key exists but is for a differnt year, only the *Detail* column will be updated
   - If there is no new data, the entry is skipped altogether
- Once the parsing is complete, it gets fed to the csv function that creates the files
- Pickle - The hash table is pickled and saved to a pkl file to allow subsequent executions to only perform updates on new data
   - After the pkl file has been created, it is loaded in upon startup so the data will always persist.

### 4. Mapping Output
Data can be mapped using google's My Maps (This is different from Google Maps). Just create a new map and import desired CSV file into your layer(s)
- Pin colors can be changed per layer or per entry but by default My Maps blasts any formatting.
- Do not go down the rabbit hole of .kml or .kmz files.  
Ask me how I know...

## Getting Started

1. **Clone the repository:**
     ```bash
     git clone https://github.com/gomez-z/top-50.git
     cd top-50-restaurants
     ```

2. **Install dependencies:**
     ```bash
     pip3 install csv requests googlemaps unidecode arcgis
     ```

3. **Execution:**
     ```bash
     python3 main.py
     ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please open an issue or contact the maintainer.
