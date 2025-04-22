import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to get data from the website
def scrape_data():
    # Initialize lists to store column data
    Year = []
    Jan = []
    Feb = []
    Mar = []
    Apr = []
    May = []
    Jun = []
    Jul = []
    Aug = []
    Sep = []
    Oct = []
    Nov = []
    Dec = []
    Ave = []

    try:
        # Install Webdriver
        service = Service(ChromeDriverManager().install())
        
        # Create Driver Instance
        driver = webdriver.Chrome(service=service)
        
        # Get Web Page
        driver.get('https://www.usinflationcalculator.com/inflation/historical-inflation-rates/#google_vignette')
        
        # Wait for the elements to load
        wait = WebDriverWait(driver, 10)
        
        # Locate the table rows
        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@border='1']/tbody/tr")))

        # Loop through the rows and extract data
        for row in rows[1:]:  # Skipping the header row
            cells = row.find_elements(By.TAG_NAME, "td")
            Year.append(row.find_element(By.TAG_NAME, "th").text)
            Jan.append(cells[0].text if cells[0].text else "-")
            Feb.append(cells[1].text if cells[1].text else "-")
            Mar.append(cells[2].text if cells[2].text else "-")
            Apr.append(cells[3].text if cells[3].text else "-")
            May.append(cells[4].text if cells[4].text else "-")
            Jun.append(cells[5].text if cells[5].text else "-")
            Jul.append(cells[6].text if cells[6].text else "-")
            Aug.append(cells[7].text if cells[7].text else "-")
            Sep.append(cells[8].text if cells[8].text else "-")
            Oct.append(cells[9].text if cells[9].text else "-")
            Nov.append(cells[10].text if cells[10].text else "-")
            Dec.append(cells[11].text if cells[11].text else "-")
            Ave.append(cells[12].text if cells[12].text else "-")
        
        # Close the webdriver
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

    # Convert data to a pandas DataFrame
    data = {
        "Years": Year,
        "January": Jan,
        "Febuary": Feb,
        "March": Mar,
        "April": Apr,
        "May": May,
        "June": Jun,
        "July": Jul,
        "August": Aug,
        "September": Sep,
        "October": Oct,
        "November": Nov,
        "December": Dec,
        "Average": Ave,
    }

    df = pd.DataFrame(data)
    return df

# Retry logic
max_retries = 5
for attempt in range(max_retries):
    df = scrape_data()
    if df is not None:
        # Give your path below where the file need to be saved------------------------
        desktop_path = 'C:/Users/iv14822/OneDrive - Newell Brands/Desktop/inflation_data.csv'
        df.to_csv(desktop_path, index=False)
        print(df)
        print(f"Data saved to {desktop_path}")
        break
    else:
        print(f"Attempt {attempt + 1} failed. Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying

if df is None:
    print("Failed to scrape data after multiple attempts.")
