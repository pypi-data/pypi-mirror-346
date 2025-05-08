from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the deployed website
website = "https://ephemeral-cheesecake-c2e4e5.netlify.app"

# Path to save the recorded text file
rec_file = f"{getcwd()}\\input.txt"

def listen():
    try:
        # Open the deployed website
        driver.get(website)

        # Wait for the start button to be clickable and click it
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening...")

        output_text = ""
        previous_length = 0
        
        while True:
            # Wait for the output element to be present
            output_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()

            # Capture only the new text added since the last read
            if len(current_text) > previous_length:
                new_text = current_text[previous_length:]  # Only capture newly added text
                previous_length = len(current_text)  # Update previous length
                
                # Save the new message only
                with open(rec_file, "a") as file:  # Append new text
                    file.write(new_text.lower())
                    print("ADNAN: " + new_text.strip())
                    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

# Start listening
listen()
