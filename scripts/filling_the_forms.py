import csv
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_input_data():
    print("Enter the fields you want to include in the form. Press Enter without typing to finish adding fields.")

    fields = []
    while True:
        # Prompt the user for the field name
        field = input("Enter the name of the field: ").strip()
        if not field:  # Stop if input is empty
            break
        fields.append(field)

    if not fields:
        print("No fields were provided. Exiting.")
        return

    print("\nEnter the data for each field. Leave a blank value to finish data entry for that field.")

    data = []
    while True:
        entry = {}
        print("\nEnter values for a new entry (press Enter without typing to finish):")
        for field in fields:
            value = input(f"{field}: ").strip()
            if not value:  # Stop if input is empty
                break
            entry[field] = value

        if not entry:  # Stop when no values are entered for a row
            break
        data.append(entry)

    if not data:
        print("No data entries were provided. Exiting.")
        return
    return fields, data


def create_csv(csv_file):
    fields, data = get_input_data()
    # Write the collected data to a CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV file '{csv_file}' created successfully with {len(data)} entries.")


def load_data_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


# Fill out a form
def fill_form(data, driver, fields):
    for entry in data:
        try:
            # Navigate to the webpage with the form
            driver.get("https://ats.rippling.com/portside/jobs/a35cfcd8-a4bd-403a-af43-5241c885af46/apply?src=LinkedIn&jobSite=LinkedIn&step=application")

            # Fill the form fields dynamically based on provided field names
            for field in fields:
                field_id = field.lower().replace(" ", "_")  # Assume IDs are in snake_case
                driver.find_element(By.ID, field_id).send_keys(entry[field])

            # Submit the form (example for a button with ID "submit")
            driver.find_element(By.ID, "submit").click()

            # Wait for a success message or redirection
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "success-message"))
            )
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
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
