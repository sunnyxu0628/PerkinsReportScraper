# README

## Introduction
This package scrapes and extracts data from the [Perkins Core Indicator Reports](https://datamart.cccco.edu/Perkins/Core_Indicator_Reports/Forms_All.aspx). The scraped data includes all TOP6 code-level Perkins Core Indicator data for the college of interest, as well as college- and/or district-level Perkins Core Indicator data. This package automates the data extraction process, making it easier to collect and analyze Perkins Core Indicator Reports.

## Instructions

### 1. Configuring Parameters (Optional)
The `config.yml` file contains all the necessary parameters for the scraping process. To customize the scraping data:
- Open the `config.yml` file in a text editor.
- Modify the parameters such as `data_folder`, `pages_to_scrape`, or `output_file` as needed.
- Save the changes.

### 2. Running the Scraper
You can run the scraper using either the Jupyter Notebook `run.ipynb` or the Python script `run.py`:

#### Option 1: Using `run.ipynb`(Recommended for Python Beginners)
1. Open the `run.ipynb` file in Jupyter Notebook.
2. Run each cell in sequence to scrape the data.

#### Option 2: Using `run.py`
1. Open a terminal or command prompt.
2. Navigate to the directory containing the package.
3. Run the following command:
    ```
    python run.py
    ```

### 3. Output
The scraped data will be saved in the folder you specified in `config.yml`.

Happy scraping!
Created by Sunny Xu
CTE Research Expert, San Diego Community College District
For questions, feel free to reach out at qxu@sdccd.edu

Note: I have also created a script that combines each individual TOP6 code-level file into one master file and cleans the data. After running this script, you can directly import the resulting file into Power BI or Tableau for visualization. SDCCD has also developed a [SDCCD Perkins Core Indicators dashboard](https://app.powerbi.com/view?r=eyJrIjoiMWI3N2Q4ZjMtNzJmZi00MDZhLTg5YTAtNWY4NThhOWRlOGZiIiwidCI6IjA0MGM2MDMxLTNhYmItNDgzNS1iMzBjLTlkODg5NTViNGM2OSIsImMiOjZ9) for reference.
