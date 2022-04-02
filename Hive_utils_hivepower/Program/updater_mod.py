from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import time
import schedule
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys


class Hive_power_tracker:

    def __init__(self, username, email_address, treshold, resend_time):

        # getting drivers / webscraping working
        options = FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path = r'/home/butterfly/home/Documents/Project/Blockchain/Hive_utils/Hive_utils_hivepower/Drivers/geckodriver', options=options) #this is the path where my geckodriver exists

        # getting data paramaters accessible for the whole class
        self.username = username
        self.email_address = email_address
        self.treshold = treshold
        self.resend_time = resend_time
        self.vote_value_percentage = ''
        self.time_to_100 = ''
        self.effective_hive_power = ''
        self.hive_power = ''
        self.total_minute_value = 0

        # getting user data 
        # self.get_user_data()
        self.email()
        #print(self)
        

    # gets user data
    def get_user_data(self):

        hivestats_url = 'https://hivestats.io/@' + self.username
        self.driver.get(hivestats_url)
        time.sleep(3)
        self.vote_value_percentage = self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/div[2]/section[1]/div[2]/div/div/span[1]/span[2]')
        self.time_to_100 = self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/div[2]/section[3]/div[2]/table/tbody/tr[8]/td[2]')
        self.effective_hive_power = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[2]/section[3]/div[2]/table/tbody/tr[1]/td[2]/span')
        self.hive_power = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[2]/section[3]/div[2]/table/tbody/tr[2]/td[2]/span')

        
        
        return 0

            
    # prints out user data 
    def __repr__(self): 
        print("---------------","\nUser:", self.username, "\nVote Power:", self.vote_value_percentage.text, "\nTime untill full:", self.time_to_100.text, "\nEffective HP:", self.effective_hive_power.text, "\nActual HP:", self.hive_power.text, "\nFull Hive Power in: ", self.total_minute_value, " minutes")
        #return "User: % s Vote Power: % s Time untill full: % s Effective HP: % s Actual HP: % s" % (self.username, self.vote_value_percentage, self.time_to_100, self.effective_hive_power, self.hive_power) 
        return "---------------"

    # gets the number of minutes left for the user to have full hive power again
    def get_time(self):
        string = str(self.time_to_100.text)
        temp = string.replace(" ", "")
        self.total_minute_value = 0
        
        if (temp.find("Full") == 0):
            self.total_minute_value = 0

        # Getting the number of minutes remaining based on the day value
        if (temp.find("day") != -1):
            day_index = temp.find("day")
            day_value = int(temp[day_index-1])
            minute_day_value = day_value * 1440
            self.total_minute_value += minute_day_value

            # Getting the number of minutes remaining based on the hour value
        if (temp.find("hour") != -1):
            hour_index = temp.find("hour")
           
                
            if (temp[hour_index-2].isdigit()):
                hour_value = int(temp[hour_index-2] + temp[hour_index-1])
                minute_hour_value = hour_value * 60
                self.total_minute_value += minute_hour_value

            elif (temp[hour_index-1].isdigit()):
                hour_value = int(temp[hour_index-1])
                minute_hour_value = hour_value * 60
                self.total_minute_value += minute_hour_value

            # Getting the number of minutes remaining based on the minute value
        if (temp.find("minute") != -1):
            minute_index = temp.find("minute")
            if (temp[minute_index-2].isdigit()):
                minute_value = int(temp[minute_index-2] + temp[minute_index-1])
                self.total_minute_value += minute_value

            elif (temp[minute_index-1].isdigit()):
                minute_value = int(temp[minute_index-1])
                self.total_minute_value += minute_value

        return self.total_minute_value



    def email(self):

        # email things
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "hivepower100@gmail.com"  # Enter your address
        password = "100%_hivepower_0%"
        subject = self.username + " YOUR HIVE POWER IS FULL"
        body =  "Hello there: " + self.username + "\n\nYour hive power is full"
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = self.email_address
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        text = message.as_string()

        print("Getting User Data")
        self.get_user_data()
        print("Getting check back time")
        check_back_time = self.get_time()
        
        schedule.every(check_back_time).minutes.do(self.email)
        while 1:
           
            if check_back_time == self.treshold:
                print("Prepping email")
                # Create a secure SSL context
                context = ssl.create_default_context()
                # create server variable
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    # log in to email
                    server.login(sender_email, password)
                    # send email
                    
                    server.sendmail(sender_email, self.email_address, text)
                    print("Sent email")
                # ending the session
                check_back_time = self.resend_time
                schedule.every(check_back_time).minutes.do(self.email)

                schedule.run_pending()
                time.sleep(5)
        

        

        
