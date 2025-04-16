import sys
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
import re

class TopCodeTableParser:
    # Table Content
    TABLE_DIV_ID = 'VisibleReportContentASPxRoundPanel2_ReportViewer2_ctl09'
    # Table Columns
    COLUMNS = [
        'CI Number', 'CI Info', 'DESCR', 'Count', 'Total',
        'Negotiated Level - State', 'Negotiated Level - District',
        'College Performance', 'Percent Above or Below Negotiated Level',
        'Percent Above or Below 90% Negotiated Level', 'Demographic'
    ]
    
    def __init__(self, soup, output_folder, title = 'None'):
        """
        Initialize with the BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup object): The parsed HTML content.
        - columns (list): Optional custom column names for the DataFrame.
        """
        self.soup = soup
        self.raw_data_ls = None
        self.clean_data_ls = None
        self.columns = self.COLUMNS
        self.table_div_id = self.TABLE_DIV_ID
        self.df = None
        self.title = title
        self.enrollment = ''
        self.headcount = ''
        self.output_folder = output_folder

    def parse_table(self):
        """
        Parses the table from the soup content and extracts the data.

        Parameters:
        - table_div_id (str): The ID of the div containing the table.

        Returns:
        - data (list): A list of rows, where each row is a list of column values.
        """
        data = []
        if self.soup is None:
            print("No content to parse. Please provide a valid BeautifulSoup object.")
            return data
        try:
            table_div = self.soup.find('div', id=self.table_div_id)
            if not table_div:
                print(f"Table with div id '{table_div_id}' not found.")
                return data
            table = table_div.find('table')
            if not table:
                print("No table found within the specified div.")
                return data
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                row_data = [col.text.strip() for col in columns]
                data.append(row_data)
            self.raw_data_ls = data
            return self.raw_data_ls
        except Exception as e:
            print(f"An error occurred while parsing the table: {e}")
            return data

    def clean_rows(self):
        """
        Cleans the raw data extracted from the table.
    
        Returns:
        - clean_data (list): The cleaned data.
        """
        data = self.raw_data_ls
        count = 0
        CI_number = ''
        CI_info = ''
        intermediate_data = []
        
        # First pass: initial cleaning and extraction
        while count < len(data):
            row = data[count]
            # Skip rows that are all empty strings
            if all(elem == '' for elem in row):
                count += 1
                continue
            if len(row) == 7:
                CI_number = row[2]
                CI_info = data[count+1][2] if count+1 < len(data) else ''
                count += 3
            
            # if there are number index in front of each row of the table, use next line instead
            # elif len(row) == 11:
            elif len(row) == 10:
                row[0] = CI_number
                row[1] = CI_info
                intermediate_data.append(row)
                count += 1
            else:
                count += 1
    
        # Second pass: further cleaning based on your code
        clean_data = []
        demo = ''
        for row in intermediate_data:
            # Skip rows that are all empty strings
            if all(elem == '' for elem in row):
                continue
            if 'CTE' in row[2]:
                demo = 'CTE'
                row.append(demo)
                clean_data.append(row)
            elif row[3:] == [''] * 7:
                demo = row[2]
                continue
            else:
                row.append(demo)
                clean_data.append(row)

        
    
        self.clean_data_ls = clean_data
        return self.clean_data_ls

    def to_df(self):
        """
        Converts the cleaned data into a Pandas DataFrame.

        Returns:
        - df (DataFrame): The resulting DataFrame.
        """
        if self.clean_data_ls is None:
            print("No clean data to convert. Please run 'clean_rows' method first.")
            return None
        self.df = pd.DataFrame(self.clean_data_ls, columns=self.columns)
        return self.df

    def get_CTE_enrollment_and_headcount(self):
        """
        Extracts CTE enrollment and headcount from the soup content.

        Returns:
        - enrollment (str): The enrollment number.
        - headcount (str): The headcount number.
        """
        enrollment = ''
        headcount = ''
        try:
            table_div = self.soup.find('div', id=self.table_div_id)
            if not table_div:
                print(f"Table with div id '{self.table_div_id}' not found.")
                return enrollment, headcount
            table = table_div.find('table')
            if not table:
                print("No table found within the specified div.")
                return enrollment, headcount
            rows = table.find_all('tr')
            for i in range(len(rows)):
                row = rows[i]
                columns = [col.text.strip() for col in row.find_all('td')]
                if columns and columns[0] == 'Cohort Year CTE Enrollments:':
                    enrollment = rows[i+1].find('td').text.strip().replace(',', '')
                    self.enrollment = enrollment
                if columns and columns[0] == 'CTE Headcount:':
                    headcount = rows[i+1].find('td').text.strip().replace(',', '')
                    self.headcount = headcount
                if self.enrollment and self.headcount:
                    return self.enrollment, self.headcount
            return enrollment, headcount
        except Exception as e:
            print("An error occurred while extracting enrollment and headcount.")
            return enrollment, headcount

    def get_table_info(self):
        """
        Orchestrates the extraction and cleaning of table data.

        Parameters:
        - table_div_id (str): The ID of the div containing the table.

        Returns:
        - df (DataFrame): The cleaned data as a DataFrame.
        - enrollment (str): The enrollment number.
        - headcount (str): The headcount number.
        """
        raw_data = self.parse_table()
        if not raw_data:
            print("No data extracted from the table.")
            return None, None, None
        clean_data = self.clean_rows()
        if not clean_data:
            print("No clean data obtained after processing.")
            return None, None, None
        df = self.to_df()
        enrollment, headcount = self.get_CTE_enrollment_and_headcount()
        return df, enrollment, headcount
        
    def save_df(self):
        if self.df is None:
            print("No DataFrame available to save. Please ensure 'to_df' method has been called.")
            return False

        # Construct the filename
        df_name = f'{self.title}.csv'
        df_path = os.path.join(self.output_folder, df_name)
    
        try:
            # Ensure the folder exists
            os.makedirs(self.output_folder, exist_ok=True)
    
            # Save the DataFrame
            self.df.to_csv(df_path, index=False)
            return True
        except Exception as e:
            print(f"An error occurred while saving the DataFrame: {e}")
            return False


class CollegeTableParser:
    # Table Content
    TABLE_DIV_ID = 'VisibleReportContentASPxRoundPanel2_ReportViewer2_ctl09'
    # Table Columns
    COLUMNS = [
        'CI Number', 'CI Info', 'Demographic', 'DESCR', 'Count', 'Total',
        'Negotiated Level - State', 'Negotiated Level - District',
        'College Performance', 'Percent Above or Below Negotiated Level',
        'Percent Above or Below 90% Negotiated Level'
    ]

    
    def __init__(self, soup, output_folder, title = 'None'):
        """
        Initialize with the BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup object): The parsed HTML content.
        - columns (list): Optional custom column names for the DataFrame.
        """
        self.soup = soup
        self.raw_data_ls = None
        self.clean_data_ls = None
        self.columns = self.COLUMNS
        self.table_div_id = self.TABLE_DIV_ID
        self.df = None
        self.title = title
        self.enrollment = ''
        self.headcount = ''
        self.output_folder = output_folder

    def parse_table(self):
        """
        Parses the table from the soup content and extracts the data.

        Parameters:
        - table_div_id (str): The ID of the div containing the table.

        Returns:
        - data (list): A list of rows, where each row is a list of column values.
        """
        data = []
        if self.soup is None:
            print("No content to parse. Please provide a valid BeautifulSoup object.")
            return data
        try:
            table_div = self.soup.find('div', id=self.table_div_id)
            if not table_div:
                print(f"Table with div id '{table_div_id}' not found.")
                return data
            table = table_div.find('table')
            if not table:
                print("No table found within the specified div.")
                return data
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                row_data = [col.text.strip() for col in columns]
                data.append(row_data)
            self.raw_data_ls = data
            return self.raw_data_ls
        except Exception as e:
            print(f"An error occurred while parsing the table: {e}")
            return data

    def clean_rows(self):
        """
        Cleans the raw data extracted from the table.
    
        Returns:
        - clean_data (list): The cleaned data.
        """
        data = self.raw_data_ls
        count = 0
        CI_number = ''
        CI_info = ''
        intermediate_data = []
        
        # First pass: initial cleaning and extraction
        while count < len(data):
            row = data[count]
            # Skip rows that are all empty strings
            if all(elem == '' for elem in row):
                count += 1
                continue
            if len(row) == 7:
                CI_number = row[2]
                CI_info = data[count+1][2] if count+1 < len(data) else ''
                count += 3
            
            # if there are number index in front of each row of the table, use next line instead
            elif len(row) == 11:
                row[0] = CI_number
                row[1] = CI_info
                intermediate_data.append(row)
                count += 1
            else:
                count += 1
    
        # Second pass: further cleaning based on your code
        
        clean_data = []
        demo = ''
        for row in intermediate_data:
            # Skip rows that are all empty strings
            if all(elem == '' for elem in row):
                continue
            if 'CTE' in row[3]:
                demo = 'CTE'
                row[2] = 'CTE'
                clean_data.append(row)
            elif row[4:] == [''] * 7:
                demo = row[3]
                continue
            else:
                row[2] = demo
                clean_data.append(row)
    
        self.clean_data_ls = clean_data
        return self.clean_data_ls

    def to_df(self):
        """
        Converts the cleaned data into a Pandas DataFrame.

        Returns:
        - df (DataFrame): The resulting DataFrame.
        """
        if self.clean_data_ls is None:
            print("No clean data to convert. Please run 'clean_rows' method first.")
            return None
        self.df = pd.DataFrame(self.clean_data_ls, columns=self.columns)
        return self.df

    def get_CTE_enrollment_and_headcount(self):
        """
        Extracts CTE enrollment and headcount from the soup content.

        Returns:
        - enrollment (str): The enrollment number.
        - headcount (str): The headcount number.
        """
        enrollment = ''
        headcount = ''
        try:
            table_div = self.soup.find('div', id=self.table_div_id)
            if not table_div:
                print(f"Table with div id '{self.table_div_id}' not found.")
                return enrollment, headcount
            table = table_div.find('table')
            if not table:
                print("No table found within the specified div.")
                return enrollment, headcount
            rows = table.find_all('tr')
            for i in range(len(rows)):
                row = rows[i]
                columns = [col.text.strip() for col in row.find_all('td')]
                if columns and columns[0] == 'Cohort Year CTE Enrollments:':
                    enrollment = rows[i+1].find('td').text.strip().replace(',', '')
                    self.enrollment = enrollment
                if columns and columns[0] == 'CTE Headcount:':
                    headcount = rows[i+1].find('td').text.strip().replace(',', '')
                    self.headcount = headcount
                if self.enrollment and self.headcount:
                    return self.enrollment, self.headcount
            return enrollment, headcount
        except Exception as e:
            print("An error occurred while extracting enrollment and headcount.")
            return enrollment, headcount

    def get_table_info(self):
        """
        Orchestrates the extraction and cleaning of table data.

        Parameters:
        - table_div_id (str): The ID of the div containing the table.

        Returns:
        - df (DataFrame): The cleaned data as a DataFrame.
        - enrollment (str): The enrollment number.
        - headcount (str): The headcount number.
        """
        raw_data = self.parse_table()
        if not raw_data:
            print("No data extracted from the table.")
            return None, None, None
        clean_data = self.clean_rows()
        if not clean_data:
            print("No clean data obtained after processing.")
            return None, None, None
        df = self.to_df()
        enrollment, headcount = self.get_CTE_enrollment_and_headcount()
        return df, enrollment, headcount
        
    def save_df(self):
        if self.df is None:
            print("No DataFrame available to save. Please ensure 'to_df' method has been called.")
            return False

        # Construct the filename
        df_name = f'{self.title}.csv'
        df_path = os.path.join(self.output_folder, df_name)
    
        try:
            # Ensure the folder exists
            os.makedirs(self.output_folder, exist_ok=True)
    
            # Save the DataFrame
            self.df.to_csv(df_path, index=False)
            return True
        except Exception as e:
            print(f"An error occurred while saving the DataFrame: {e}")
            return False