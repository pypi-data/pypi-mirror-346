'''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--use-fake-ui-for-media-stream")
# # chrome_options.add_argument("--headless=new")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

# website = f"{getcwd()}\\index.html"

# driver.get(website)

# rec_file = f"{getcwd()}\\input.txt"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
def listen():

website = "https://ephemeral-cheesecake-c2e4e5.netlify.app"

driver.get(website)

rec_file = f"{getcwd()}\\input.txt"

    try:
        start_button =WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'startButton')))
        start_button.click()
        print ("Listening...")
        output_text = ""
        is_second_click = False
        while True:
            output_element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'output')))
            current_text = output_element.text.strip()
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = True
            elif "Listening..." in start_button.text:
                is_second_click = False
            if current_text != output_text:
                output_text = current_text
                with open(rec_file,"w") as file:
                    file.write(output_text.lower())
                    print ("ADNAN: " + output_text)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

listen()'''

'''from selenium import webdriver
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
        is_second_click = False
        
        while True:
            # Wait for the output element to be present
            output_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()
            
            # Logic to handle clicks and text updates
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = True
            elif "Listening..." in start_button.text:
                is_second_click = False
            
            if current_text != output_text:
                output_text = current_text
                with open(rec_file, "w") as file:
                    file.write(output_text.lower())
                    print("ADNAN: " + output_text)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

# Start listening
listen()'''














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




# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from os import getcwd

# # Set up Chrome options
# chrome_options = webdriver.ChromeOptions()

# # Allow microphone & camera usage
# chrome_options.add_argument("--use-fake-ui-for-media-stream")
# chrome_options.add_argument("--use-fake-device-for-media-stream")  # Optional fake mic for testing
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-popup-blocking")

# # Permissions for mic/cam in Chrome
# chrome_options.add_experimental_option("prefs", {
#     "profile.default_content_setting_values.media_stream_mic": 1,
#     "profile.default_content_setting_values.media_stream_camera": 1,
#     "profile.default_content_setting_values.geolocation": 1,
#     "profile.default_content_setting_values.notifications": 1
# })

# # ❌ Do NOT use headless while testing mic
# # chrome_options.add_argument("--headless=new")

# # Initialize the Chrome driver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# # URL of your deployed speech-to-text site
# website = "https://ephemeral-cheesecake-c2e4e5.netlify.app"

# # Path to save the recorded text
# rec_file = f"{getcwd()}\\input.txt"

# def listen():
#     try:
#         # Open the website
#         driver.get(website)

#         # Wait and click the start button
#         start_button = WebDriverWait(driver, 30).until(
#             EC.element_to_be_clickable((By.ID, 'startButton'))
#         )
#         start_button.click()
#         print("Listening...")

#         output_text = ""
#         previous_length = 0

#         while True:
#             # Get output container
#             output_element = WebDriverWait(driver, 20).until(
#                 EC.presence_of_element_located((By.ID, 'output'))
#             )
#             current_text = output_element.text.strip()

#             # Save only new text
#             if len(current_text) > previous_length:
#                 new_text = current_text[previous_length:]
#                 previous_length = len(current_text)

#                 with open(rec_file, "a") as file:
#                     file.write(new_text.lower() + "\n")
#                     print("ADNAN:", new_text.strip())

#     except KeyboardInterrupt:
#         print("Stopped by user.")
#     except Exception as e:
#         print("Error:", e)

# # Start the listener
# listen()


