from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import sys
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import csv
from selenium.webdriver.chrome.options import Options
import re
import yaml

def load_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

class PerkinsWebScraper:
    config = load_config()
    URL = config['URL']
    SELECT_FORM_TYPE = config['ELEMENT_INFO']['form_type']
    SELECT_DISTRICT_COLLEGE = config['ELEMENT_INFO']['district_college']
    FISCAL_YEAR = config['ELEMENT_INFO']['fiscal_year']
    TOP_CODE = config['ELEMENT_INFO']['top_code']
    TABLE_DIV_ID = config['TABLE_DIV_ID']
    VIEW_REPORT = config['VIEW_REPORT']
    ELEMENT_INFO = config['ELEMENT_INFO']

    @classmethod
    def get_form_types(cls):
        return cls.config['forms']

    @classmethod
    def get_college_list(cls):
        return cls.config['colleges']
    
    @classmethod
    def get_district_list(cls):
        return cls.config['districts']
    
    @classmethod
    def get_year_list(cls):
        return cls.config['years']
    
    @classmethod
    def get_data_paths(cls):
        return cls.config['paths']

    def __init__(self, url=URL, implicit_wait=None, explicit_wait=None, record_csv_path=None, headless=None):
        """
        Initialize the webdriver and open the given URL.

        Parameters use config values by default if not specified:
        - url (str): The URL to navigate to
        - implicit_wait (int): The implicit wait time in seconds
        - explicit_wait (int): The explicit wait time in seconds for WebDriverWait
        - record_csv_path (str): Path to the CSV file for recording scraped parameters
        - headless (bool): Whether to run browser in headless mode
        """
        self.config = PerkinsWebScraper.config
        implicit_wait = implicit_wait or self.config['scraping_params']['implicit_wait']
        explicit_wait = explicit_wait or self.config['scraping_params']['explicit_wait']
        headless = headless if headless is not None else self.config['scraping_params']['headless']
        record_csv_path = record_csv_path or self.config['paths']['record_csv']

        if headless:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
        else:
            chrome_options = None
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(implicit_wait)
        self.wait = WebDriverWait(self.driver, explicit_wait)
        self.url = url
        self.soup = None
        self.record_csv_path = record_csv_path
        self.form_type = 'None'
        self.district_college = 'None'
        self.fiscal_year = 'None'
        self.top_code = 'NA'
        if record_csv_path:
            try:
                self.scrape_record = pd.read_csv(record_csv_path, keep_default_na=False)
            except FileNotFoundError:
                # If the file doesn't exist, create an empty DataFrame with the required columns
                self.scrape_record = pd.DataFrame(columns=['form_type', 'district_college', 'fiscal_year', 'top_code', 'headcount', 'enrollment', 'file_path'])
        else:
            self.scrape_record = pd.DataFrame(columns=['form_type', 'district_college', 'fiscal_year', 'top_code', 'headcount', 'enrollment', 'file_path'])

    def get_url(self):
        self.driver.get(self.url)
    
    def is_recorded(self, form_type, district_college, fiscal_year, top_code):
        """
        Check if the given parameters are already recorded in the scrape_record.
        """
        if self.scrape_record.empty:
            #print("No records to check against.")
            return False

        # Create a boolean mask for the matching row
        mask = (
            (self.scrape_record['form_type'] == form_type) &
            (self.scrape_record['district_college'] == district_college.strip()) &
            (self.scrape_record['fiscal_year'] == fiscal_year) &
            (self.scrape_record['top_code'] == top_code)
        )
        exists = mask.any()
        return exists
        

    def input_value(self, input_box, value):
        """
        Inputs a value into a specified input box on the webpage with improved dropdown handling.

        Parameters:
        - input_box (str): The key representing the input box in element_info.
        - value (str): The value to input into the box.
        """
        if value == 'NA':
            return
        if input_box not in self.ELEMENT_INFO:
            print(f"Box name should be one of these values: {list(self.ELEMENT_INFO.keys())}. Please input a proper box name.")
            return

        element_id = self.ELEMENT_INFO[input_box]
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            try:
                # Wait for element and ensure it's clickable
                input_element = self.wait.until(EC.element_to_be_clickable((By.ID, element_id)))
                
                # Clear existing text and click to ensure focus
                input_element.click()
                input_element.clear()
                time.sleep(0.5)  # Short pause for stability
                
                # Type the value and ensure it's set
                input_element.send_keys(value)
                time.sleep(0.5)  # Wait for dropdown to update
                
                # Verify the input was accepted
                actual_value = input_element.get_attribute('value')
                if actual_value == value:
                    return True
                
                attempt += 1
                if attempt < max_attempts:
                    time.sleep(1)  # Wait before retry
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for '{input_box}': {e}")
                attempt += 1
                if attempt < max_attempts:
                    time.sleep(1)
        
        print(f"Failed to input value into '{input_box}' after {max_attempts} attempts.")

    def view_report(self):
        """
        Clicks the report button to view a report.

        Parameters:
        - report_button (str): The identifier of the report button element.
        """
        try:
            report_button_element = self.wait.until(EC.element_to_be_clickable((By.ID, self.VIEW_REPORT)))
            report_button_element.click()
        except Exception as e:
            print(f"An error occurred while clicking the report button: {e}")

    def get_content(self, parser='html.parser'):
        """
        Waits for the table to appear and parses the page source with BeautifulSoup.

        Parameters:
        - table_div_id (str): The ID of the table's div element to wait for.
        - parser (str): The parser to use with BeautifulSoup.

        Returns:
        - soup (BeautifulSoup object): The parsed HTML content.
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, self.TABLE_DIV_ID)))
            page_source = self.driver.page_source
            self.soup = BeautifulSoup(page_source, parser)
            return self.soup
        except Exception as e:
            print(f"An error occurred while getting content: {e}")
            return None
        
    def get_top_codes(self, form_type, district_college, fiscal_year):
        """
        Get all available top codes given if form type is top code
        """
        self.get_url()
        self.input_value('form_type', form_type)
        self.input_value('fiscal_year', fiscal_year)
        time.sleep(1)
        self.input_value('district_college', district_college)
        # self.wait.until(EC.presence_of_element_located((By.ID, self.TOP_CODE)))
        # self.wait.until(EC.element_to_be_clickable((By.ID, self.TOP_CODE)))
        top_code_dropdown_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.TOP_CODE))
        )
        top_code_dropdown_button.click()
        time.sleep(1)
        top_code_dropdown_button.click()
        # self.wait.until(EC.element_to_be_clickable((By.ID, self.TOP_CODE)))
        # time.sleep(2)

        top_code_options = self.wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, "//table[@id='ASPxRoundPanel1_ASPxComboBoxTCode_DDD_L_LBT']//td[@class='dxeListBoxItem_Aqua']"))
        )
        top_codes = [top_code.text for top_code in top_code_options]
        self.close()
        return top_codes

    def scrape_report(self, form_type, district_college, fiscal_year, top_code):
        """
        Orchestrates the scraping process.

        Parameters:
        - form_type (str): The form type to input.
        - district_college (str): The college or district to select.
        - fiscal_year (str): The fiscal year to input.
        - top_code (str): The TOP code to input.

        Returns:
        - soup (BeautifulSoup object): The parsed HTML content.
        """
        if self.is_recorded(form_type, district_college, fiscal_year, top_code):
            print(f'{form_type}, {district_college.strip()}, {fiscal_year}, {top_code} is scraped already.')
            return None
        try:
            #get url
            self.get_url()
            # Input values
            self.input_value('form_type', form_type)
            self.input_value('fiscal_year', fiscal_year)
            time.sleep(1)
            self.input_value('district_college', district_college)
            if top_code and top_code != 'NA':
                #time.sleep(1)
                self.input_value('top_code', top_code)
                self.input_value('top_code', top_code)
                time.sleep(1)
            # Click the view report button
            #time.sleep(1)
            self.view_report()

            # Get and parse the content
            #time.sleep(2)
            self.wait.until(EC.visibility_of_element_located((By.ID, self.TABLE_DIV_ID)))
            soup = self.get_content()

            if soup:
                self.form_type = form_type
                self.district_college = district_college.strip()
                self.fiscal_year = fiscal_year
                self.top_code = top_code if top_code else 'NA'
                return soup
            else:
                print("Failed to retrieve content from the page.")
                return None
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            return None

    def add_record(self, headcount, enrollment, file_path):
        """
        Add a new record to the scrape_record DataFrame and save to CSV if path is provided.
        """
        new_record = pd.DataFrame([{
            'form_type': self.form_type,
            'district_college': self.district_college,
            'fiscal_year': self.fiscal_year,
            'top_code': self.top_code,
            'headcount': headcount,
            'enrollment': enrollment,
            'file_path': file_path
        }])
        self.scrape_record = pd.concat([self.scrape_record, new_record], ignore_index=True)

        if self.record_csv_path:
            self.scrape_record.to_csv(self.record_csv_path, index=False)

    def close(self):
        """
        Closes the webdriver instance if it is initialized.
        """
        if self.driver:
            self.driver.quit()
        self.driver.quit()