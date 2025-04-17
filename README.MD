# README

## Introduction
This package scrapes and extracts data from the [Perkins Core Indicator Reports](https://datamart.cccco.edu/Perkins/Core_Indicator_Reports/Forms_All.aspx). The scraped data includes all TOP6 code-level Perkins Core Indicator data for the college of interest, as well as college- and/or district-level Perkins Core Indicator data. This package automates the data extraction process, making it easier to collect and analyze Perkins Core Indicator Reports.

## Instructions

### 1. Install Python and Relevant Tools
Before running the scraper, make sure you have Python installed along with Jupyter Notebook or Visual Studio:

- **Install Python**: You can download and install Python from the official [Python website](https://www.python.org/downloads/).
- **Install Jupyter Notebook or Visual Studio**:
    - Option1: Download and install Jupyter Notebook via Anaconda (Recommended for Python Beginners):
        - Download and install [Anaconda](https://www.anaconda.com/download).
        - Once installed, open Anaconda Navigator and launch Jupyter Notebook.
    - Option2: Download and install [Visual Studio Code](https://code.visualstudio.com/Download).

### 2. Download ChromeDriver
Make sure you have GoogleChrome browser and Follow these steps to download the appropriate version of `chromedriver` for your operating system:

#### Step 1: Find Your Chrome Version
1. Open Google Chrome and type `chrome://settings/help` in the address bar to see the version number.
   - Example version: `96.0.4664.110`.

#### Step 2: Download the Correct Version of ChromeDriver
1. Go to the [ChromeDriver download page](https://googlechromelabs.github.io/chrome-for-testing/#stable).
2. Select the version that matches your Chrome version. For example:
   - If you are using Chrome version `96.0.4664.x`, download the `ChromeDriver 96.x.x` version.
3. Download the driver for your operating system:
   - **Windows:** Download the `chromedriver_win32.zip` file.
   - **macOS:** Download the `chromedriver_mac64.zip` file.

#### Step 3: Extract the Driver
After downloading, extract the ZIP file:
- **Windows:** Right-click the ZIP file and select "Extract All" to extract the contents.
- **macOS/Linux:** Use the `unzip` command or the GUI to extract the ZIP.

#### Step 4: Place `chromedriver` in the Project Folder
- Move the extracted `chromedriver` to the PerkinsReportScraper folder. 

Alternatively, if you want to store `chromedriver` elsewhere on your system, you can add its location to your system’s `PATH` environment variable. This way, Selenium will be able to find `chromedriver` without needing to specify its full path.

### 3. Configuring Parameters (Optional)
The `config.yml` file contains all the necessary parameters for the scraping process. To customize the scraping data:
- Open the `config.yml` file in a text editor.
- Modify the parameters such as `data_folder`, `pages_to_scrape`, or `output_file` as needed.
- Save the changes.

### 4. Running the Scraper
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

### ⚠️ Important Note: Adjust Sleep Settings
To ensure the scraper runs without interruption, we recommend adjusting your computer’s sleep settings so it does **not go to sleep** during the scraping process. If your laptop goes to sleep or becomes inactive, the script may stop running.

#### For macOS:
- Go to **System Settings** > **Displays** > **Advanced...**
- Toggle **"Prevent automatic sleeping when the display is off"** to **on**

#### For Windows:
- Go to **Settings** > **System** > **Power & Sleep**
- Set **Sleep** to **Never** while plugged in

### 5. Output
The scraped data will be saved in the folder you specified in `config.yml`.

### 6. Combining and Cleaning the Data (Optional)
I have also created a script that combines each individual TOP6 code-level file into one master file and cleans the data. After running this script, you can directly import the resulting file into Power BI or Tableau for visualization. 

SDCCD has also developed a [Perkins Core Indicators Dashboard](https://app.powerbi.com/view?r=eyJrIjoiMWI3N2Q4ZjMtNzJmZi00MDZhLTg5YTAtNWY4NThhOWRlOGZiIiwidCI6IjA0MGM2MDMxLTNhYmItNDgzNS1iMzBjLTlkODg5NTViNGM2OSIsImMiOjZ9) for reference.

---
Happy scraping!
This code is created by Sunny Xu, CTE Research Expert, San Diego Community College District
For questions, feel free to reach out at qxu@sdccd.edu
