from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

#Initialization
options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 2  # 1: Allow, 2: Block
})
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.jobsatamazon.co.uk/app#/jobSearch"
driver.get(url)

# Handle the cookie consent prompt
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/button[1]/div"))
    ).click()
except Exception as e:
    print("Cookie consent prompt not found or an issue occurred:", e)

#  Function to check for job vacancies in the desired location
def check_vacancy():
    try:
        # Wait for the job listings to load, with a longer timeout
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test-component='StencilText' and contains(., 'Portadown')]")))

# Print the text of the element
        print(element.text)

        if element.text:
            print(f"Job found in {element.text}")
            return True, element.text

        return False

    except Exception as e:
        print("Error checking for job vacancies:", e)
        return False

 # Function to send an email alert
def send_alert():
    # Define the email subject and body
    subject = f"Amazon Warehouse Operative Vacancy at {check_vacancy()[1]}"
    body = (
        f'''Hello, \n
There is a vacancy at {check_vacancy()[1]}. Click here: https://www.jobsatamazon.co.uk/app#/jobSearch 
\n\nThank you'''
    )
    # Change your credentials
    sender_email = "youremail@gmail.com"
    receiver_email = "receiveremail@gmail.com"
    password = "**** **** **** ****"  # Use your email app password if you have 2FA enabled

    # SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Fill in the body of the email
    vacancy_info = check_vacancy()[1]  # Assume this returns the vacancy information
    body = body.format(vacancy=vacancy_info)
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Main loop to keep checking for vacancies
if __name__ == "__main__":
    while True:
        if check_vacancy():
            send_alert()
        else:
            print(f"No job found in {check_vacancy()[1]}. Checking again in 10 mins...")
        time.sleep(60)

    driver.quit()

