# README

## Introduction
This package is designed to scrape data from [the Perkins Core Indicator Reports](https://datamart.cccco.edu/Perkins/Core_Indicator_Reports/Forms_All.aspx). The data being scraped includes [Insert Data Types, e.g., product details, user reviews, etc.]. The purpose of this package is to automate the data extraction process, making it easier to collect and analyze the required information.

## Instructions

### 1. Configuring Parameters (Optional)
The `config.yml` file contains all the necessary parameters for the scraping process. To customize the scraping data:
- Open the `config.yml` file in a text editor.
- Modify the parameters such as `data_folder`, `pages_to_scrape`, or `output_file` as needed.
- Save the changes.

### 2. Running the Scraper
You can run the scraper using either the Jupyter Notebook `run.ipynb` or the Python script `run.py`:

#### Using `run.ipynb`(Recommend for Python Beginners)
1. Open the `run.ipynb` file in Jupyter Notebook.
2. Execute the cells in sequence to scrape the data.

#### Option 2: Using `run.py`
1. Open a terminal or command prompt.
2. Navigate to the directory containing the package.
3. Run the following command:
    ```
    python run.py
    ```

### 3. Output
The scraped data will be saved in the folder you specified in `config.yml`

Happy scraping!
Sunny Xu