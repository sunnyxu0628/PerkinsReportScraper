import sys
import os
from tqdm import tqdm
import yaml

# Define the project root directory
project_root = os.getcwd()

# Add the project root to sys.path if not already present
if project_root not in sys.path:
    sys.path.append(project_root)

# Load configuration
with open(os.path.join(project_root, 'config.yml'), 'r') as f:
    config = yaml.safe_load(f)

# Now you can import your modules
from src.PerkinsWebScraper import PerkinsWebScraper
from src.TableParser import TopCodeTableParser, CollegeTableParser

# Get parameters from config
FORM_TYPE_LS = config['forms']
COLLEGE_LS = config['colleges']
YEAR_LS = config['years']

# Define your file path here
#====================================================================================
# folder to store all data
data_folder = config['paths']['data_folder']

# Using os.path.join for subdirectories
college_fp = os.path.join(data_folder, config['paths']['college_folder'])
district_fp = os.path.join(data_folder, config['paths']['district_folder'])
top_code_fp = os.path.join(data_folder, config['paths']['top_code_folder'])

# csv file path to log the scraping record.
record_csv_path = os.path.join(data_folder, config['paths']['record_csv'])

# Create directories if they don't exist
os.makedirs(college_fp, exist_ok=True)
os.makedirs(district_fp, exist_ok=True)
os.makedirs(top_code_fp, exist_ok=True)
#====================================================================================


def scrape(form_type, district_college, fiscal_year, top_code, record_csv_path, output_folder, headless=False):
    # scrape content soup
    scraper = PerkinsWebScraper(
        implicit_wait=config['scraping_params']['implicit_wait'], 
        explicit_wait=config['scraping_params']['explicit_wait'], 
        headless=headless, 
        record_csv_path=record_csv_path
    )
    try:
        soup = scraper.scrape_report(form_type, district_college, fiscal_year, top_code)
        
        # parse table
        if soup:
            title = f"{district_college.strip()}_{fiscal_year}_{top_code.replace('/', '&') if top_code != 'NA' else 'NA'}"
            if form_type == 'Form 1 Part E-C - College':
                parser = CollegeTableParser(soup, output_folder=output_folder, title=title)
            else:
                parser = TopCodeTableParser(soup, output_folder=output_folder, title=title)
            df, enrollment, headcount = parser.get_table_info()
            success = parser.save_df()
            if success:
                scraper.add_record(headcount=parser.headcount, enrollment=parser.enrollment, file_path=os.path.join(parser.output_folder, f'{parser.title}.csv'))
    finally:
        scraper.close()


def run(form_type, college_ls=COLLEGE_LS, year_ls=YEAR_LS):
    headless = config['scraping_params']['headless']
    
    if form_type == 'Form 1 Part E-C - College':
        top_code = 'NA'
        for college in college_ls:
            print(f'Working on {college.strip()}...')
            for fiscal_year in tqdm(year_ls, desc='Fiscal Years', unit='year', leave=True, position=0):
                scrape(
                    form_type,
                    college,
                    fiscal_year,
                    top_code,
                    record_csv_path=record_csv_path,
                    output_folder=college_fp,
                    headless=headless
                )
                
    elif form_type == 'Form 1 Part E-D - District':
        print(f'Download the files yourself and put them in {district_fp}.')
    
    elif form_type == 'Form 1 Part F by 6 Digit TOP Code - College':
        for college in college_ls:
            for fiscal_year in year_ls:
                get_top_codes = PerkinsWebScraper(headless=headless)
                try:
                    top_codes = get_top_codes.get_top_codes(form_type, college, fiscal_year)
                    print(f'Working on {college.strip()} in {fiscal_year}...')
                    for top_code in tqdm(top_codes, desc='Top Codes', unit='code', leave=True, position=0):
                        out_folder = os.path.join(top_code_fp, college.strip())
                        os.makedirs(out_folder, exist_ok=True)
                        scrape(
                            form_type,
                            college,
                            fiscal_year,
                            top_code,
                            record_csv_path=record_csv_path,
                            output_folder=out_folder,
                            headless=headless
                        )
                finally:
                    get_top_codes.close()
                print(f'Finished all top codes of {college.strip()} in {fiscal_year}!')

if __name__ == '__main__':
    # Get scraping parameters from config
    implicit_wait = config['scraping_params']['implicit_wait']
    explicit_wait = config['scraping_params']['explicit_wait']
    headless = config['scraping_params']['headless']

    for form_type in FORM_TYPE_LS:
        run(form_type)


























