from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import mysql.connector


driver = webdriver.Chrome(service=Service("C:\Drivers\chromedriver_win32\chromedriver.exe")) #Open browser

driver.get("https://www.careerguide.com/career-options") #Open careerguide link
driver.implicitly_wait(20)

jobcategories = driver.find_elements(By.CSS_SELECTOR, 'div.c-content-panel > div > div > div > h2 > a') #Search all jobs category
jobcategory = [] #Create empty lists for job category
for jobcat in jobcategories:
    jobcategory.append(jobcat.text)

jobs = driver.find_elements(By.CSS_SELECTOR, 'div.row:nth-child(8) div.col-md-4:nth-child(1) ul li:nth-child(n+1) > a') #Search all jobs in  IT category
listjob = [] #Create empty lists
for job in jobs:
    listjob.append(job.text) #Add each jobs in lists

time.sleep(5)
driver.get("https://www.linkedin.com") #Open Linkedin link
time.sleep(5)
driver.find_element(By.XPATH,'/html/body/nav/ul/li[4]/a').click() #Click on jobs
time.sleep(5)

state = ["Delhi", "Uttar Pradesh", "Uttarakhand", "Arunachal Pradesh", "Uttaranchal", "Rajasthan"]
joburl = []
jobposition = []
companyname = []
joblocation = []
companydescription = []
companylocation = []
companyemployees = []


for job in listjob:
    driver.find_element(By.NAME,'keywords').send_keys(job) #Enter jobs
    time.sleep(5)
    driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/section/section[2]/form/section[2]/button').click() #click on cross in location to empty input
    driver.find_element(By.NAME,'location').send_keys('Delhi, India') #Enter location
    time.sleep(5)
    driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/section/section[2]/form/button').click() #Click on search button
    time.sleep(10)
    totaljobs = driver.find_elements(By.CSS_SELECTOR,'ul > li:nth-child(n+1) > div > a') #Find Total jobs


    for j in range(len(totaljobs)):
        # print(driver.find_element(By.CSS_SELECTOR,f'ul > li:nth-child({j+1}) > div > a').get_attribute('href')) #Fetch Url to apply for the job
        time.sleep(10)
        driver.find_element(By.CSS_SELECTOR,f'ul > li:nth-child({j+1}) > div > a').click() #Click on the job
        time.sleep(10)
        joburl.append(driver.current_url)
        jobposition.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1').text) #Fetch Position of the job
        companyname.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').text) #Fetch Company name
        joblocation.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]').text) #Fetch Location

        companyprofile = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').get_attribute('href') #Fetch Company profile link
        driver.get(companyprofile)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="contextual-sign-in"]/div/section/button'))) #Wait for modal box to popup
        
        # Removed below condition as it creates problem
        ''' if driver.find_element(By.XPATH,'//*[@id="contextual-sign-in"]/div/section/button'):
             element.click() #Click to close modal box'''
        
        time.sleep(5)
        # companydescription.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').text) #Fetch Description of the company
        companylocation.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[4]/dd').text) #Fetch Location of the company
        companyemployees.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').text) #Fetch employees of the company

        time.sleep(5)
        driver.back()
        time.sleep(5)
        driver.back()

    driver.back()
    wrongurl = driver.current_url
    time.sleep(5)
    if "https://www.linkedin.com/authwall?trk=qf&original_referer=" in wrongurl:
        driver.back()
        driver.find_element(By.XPATH,'/html/body/nav/ul/li[4]/a').click() #Click on jobs
driver.close()

#Changing lists into tuples to insert data in database
mysql_jobcategory = [(x,) for x in jobcategory]
mysql_listjob = [(x,"22") for x in listjob]
mysql_state = [(x,) for x in state]
mysql_companyprofile = list(zip(companyname,companydescription,state,listjob))
mysql_jobs = list(zip(companyname,jobposition,joblocation))



# Initialising Mysql to insert all of the fetched data

# To create a new database Use the below code

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root"
# )

# mycursor = db.cursor()

# mycursor.execute("CREATE DATABASE selenium_assignment")


# In this I have already create a database name 'fake'
db = mysql.connector.connect(
    host="localhost", #If you are using localhost
    user="root",    #Enter database username in place of 'root'
    password="root",  #Enter database password in place of 'root'
    database="fake" #Enter the database name in place of 'fake'
)

mycursor = db.cursor()


# To create tables

# Queries
# Q1 = "CREATE TABLE JobType1 (Category_ID INT AUTO_INCREMENT PRIMARY KEY, Category VARCHAR(50))"

# Q2 = "CREATE TABLE JobType2 (Sub_Category_ID INT AUTO_INCREMENT PRIMARY KEY, Sub_Category VARCHAR(50), Category_ID INT, FOREIGN KEY(Category_ID) REFERENCES JobType1(Category_ID))"

# Q3 = "CREATE TABLE States (State_ID INT AUTO_INCREMENT PRIMARY KEY, State VARCHAR(50))"

# Q4 = "CREATE TABLE CompanyProfile (Company_ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(50), Description VARCHAR(255), State VARCHAR(50), Sub_Category VARCHAR(50), Sub_Category_ID INT, FOREIGN KEY(Sub_Category_ID) REFERENCES JobType2(Sub_Category_ID))"

# Q5 = "CREATE TABLE Jobs (Job_ID INT AUTO_INCREMENT PRIMARY KEY, Company_Name VARCHAR(50), Position VARCHAR(50), Location VARCHAR(50), Company_ID INT, FOREIGN KEY(Company_ID) REFERENCES CompanyProfile(Company_ID))"

# mycursor.execute(Q1)
# mycursor.execute(Q2)
# mycursor.execute(Q3)
# mycursor.execute(Q4)
# mycursor.execute(Q5)


# In this case I have already created tables

# Now to Insert data in each tables

#Queries
Q1 = "INSERT INTO JobType1 (Category) VALUES (%s)"
mycursor.executemany(Q1,(mysql_jobcategory))
db.commit()

Q2 = "INSERT INTO JobType2 (Sub_Category, Category_ID) VALUES (%s, %s)"
mycursor.executemany(Q2,(mysql_listjob))
db.commit()

Q3 = "INSERT INTO States (State) VALUES (%s)"
mycursor.executemany(Q3,(mysql_state))
db.commit()

Q4 = "INSERT INTO CompanyProfile (Name, Description, State, Sub_Category) VALUES (%s, %s, %s, %s)"
mycursor.executemany(Q4,(mysql_companyprofile))
db.commit()

Q5 = "INSERT INTO Jobs (Company_Name, Position, Location) VALUES (%s, %s, %s)"
mycursor.executemany(Q5,(mysql_jobs))
db.commit()