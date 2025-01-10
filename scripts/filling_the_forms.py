import csv
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def get_input_data():
    print("Enter the fields you want to include in the form. Press Enter without typing to finish adding fields.")

    fields, data = [], []
    while True:
        # Prompt the user for the field name
        field = input("Enter the name of the field: ").strip()
        if not field:  # Stop if input is empty
            break
        fields.append(field)

    print("\nEnter the data for each field. Leave a blank value to finish data entry for that field.")

    entry = {}
    print("\nEnter values for a new entry (press Enter without typing to finish):")
    for field in fields:
        value = input(f"{field}: ").strip()
        if not value:  # Stop if input is empty
            break
        entry[field] = value

    data.append(entry)

    return fields, data


def create_csv(csv_file):
    fields, data = get_input_data()
    if not fields or not data:
        print("No data were provided. Exiting.")
        return
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV file '{csv_file}' created successfully with {len(data)} entries.")


def load_data_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def fill_form(data, driver, fields):
    for entry in data:
        try:
            # Navigate to the webpage with the form
            driver.get("https://ats.rippling.com/portside/jobs/a35cfcd8-a4bd-403a-af43-5241c885af46/apply?src=LinkedIn&jobSite=LinkedIn&step=application")

            # Fill the form fields dynamically based on provided field names
            for field in fields:
                field_id = field.lower().replace(" ", "_")  # Assume IDs are in snake_case
                try:
                    driver.find_element(By.CSS_SELECTOR, f'input[data-input={field_id}]').send_keys(entry[field])
                except NoSuchElementException:
                    print(f"couldn't find {field_id} on page..continue..")
                    continue

            submit = input("Do you want to submit?): ").strip().lower()
            if submit in ['yes', 'y']:
                driver.find_element(By.ID, "submit").click()
                print(f"Form submitted for {entry[fields[0]]}")

        except Exception as e:
            print(f"Failed to submit form for {entry[fields[0]]}: {e}")


def main():
    csv_file = "form_data.csv"

    choice = input("Do you want to create a new CSV file? (yes/no): ").strip().lower()
    if choice in ['yes', 'y']:
        create_csv(csv_file)

    data = load_data_csv(csv_file)

    # Get fields from the CSV header
    fields = list(data[0].keys()) if data else []
    if not fields:
        print("No data available in the CSV file. Exiting.")
        return

    # Path to the WebDriver executable (e.g., chromedriver)
    driver_path = "/Users/dilyara/drivers/chromedriver-mac-arm64/chromedriver"

    # Initialize the WebDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        fill_form(data, driver, fields)
    except Exception as e:
        print(f"Exception {str(e)}")
    finally:
        time.sleep(20)
        driver.quit()


if __name__ == "__main__":
    main()
