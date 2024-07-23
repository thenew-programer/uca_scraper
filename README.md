# Resultats de S5 du parcours Licence D'Excellence Finance Appliquee

# Student Grades Scraper

Ce script extrait les notes de semestre 5 des etudiants de la Licence d'Excellence option Finance Appliquee, du site des notes ``
This Python script scrapes student grades from a Cadi Ayyad website, parses the data, calculates averages, and sorts the students by their marks. [Website](http://e-apps.fsjes.uca.ma/scolarite/resultat/index.php)

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

1. Clone the repository or download the script.

    ```bash
       git clone https://github.com/thenew-programer/uca_scraper.git
    ```

2. Navigate to the project directory.

    ```bash
    cd student-grades-scraper
    ```

3. Install the required dependencies.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script.

    ```bash
    ./student_grades_scraper.py
    ```

2. Follow the on-screen prompts to enter your Apogee number or provide a file containing multiple Apogee numbers.

3. The script will fetch the grades, calculate the averages, and generate a report in `report.txt`.

## How It Works

1. **Getting Apogee Numbers:** The script asks for your Apogee number or a file containing multiple Apogee numbers.

2. **Fetching Data:** It sends a request to the university's result page with the provided Apogee number(s).

3. **Parsing Marks:** The script uses BeautifulSoup to parse the HTML content and extract the grades for each subject.

4. **Calculating Averages:** It calculates the weighted average of the grades.

5. **Generating Report:** The script sorts the students by their average marks and writes the sorted data to `report.txt`.

## Dependencies

- Python 3.x
- requests
- pandas
- beautifulsoup4
- openpyxl

You can install the dependencies using the command below:

```bash
pip install requests pandas bs4 openpyxl
```
