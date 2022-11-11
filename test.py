from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=Service("C:\Drivers\chromedriver_win32\chromedriver.exe")) #Open browser

driver.get("https://www.careerguide.com/career-options") #Open careerguide link
driver.implicitly_wait(20)

jobs = driver.find_elements(By.CSS_SELECTOR, 'div.row:nth-child(8) div.col-md-4:nth-child(1) ul li:nth-child(n+1) > a') #Search all jobs in  IT category
listjob = [] #Create empty lists
for job in jobs:
    listjob.append(job.text) #Add each jobs in lists

driver.get("https://www.linkedin.com") #Open Linkedin link
driver.find_element(By.XPATH,'/html/body/nav/ul/li[4]/a').click() #Click on jobs

joburl = []
jobposition = []
companyname = []
joblocation = []
companydescription = []
companylocation = []
companyemployees = []


for job in listjob:
    driver.find_element(By.NAME,'keywords').send_keys(job) #Enter jobs
    driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/section/section[2]/form/section[2]/button').click() #click on cross in location to empty input
    driver.find_element(By.NAME,'location').send_keys('Delhi, India') #Enter location
    driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/section/section[2]/form/button').click() #Click on search button
    time.sleep(5)
    totaljobs = driver.find_elements(By.CSS_SELECTOR,'ul > li:nth-child(n+1) > div > a') #Find Total jobs


    for j in range(len(totaljobs)):
        # print(driver.find_element(By.CSS_SELECTOR,f'ul > li:nth-child({j+1}) > div > a').get_attribute('href')) #Fetch Url to apply for the job
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR,f'ul > li:nth-child({j+1}) > div > a').click() #Click on the job
        time.sleep(3)
        joburl.append(driver.current_url)
        jobposition.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1').text) #Fetch Position of the job
        companyname.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').text) #Fetch Company name
        joblocation.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]').text) #Fetch Location

        companyprofile = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').get_attribute('href') #Fetch Company profile link
        driver.get(companyprofile)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="contextual-sign-in"]/div/section/button'))) #Wait for modal box to popup
        if EC.presence_of_element_located((By.XPATH,'//*[@id="contextual-sign-in"]/div/section/button')):
            element.click() #Click to close modal box
        time.sleep(3)
        companydescription.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').text) #Fetch Description of the company
        companylocation.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[4]/dd').text) #Fetch Location of the company
        companyemployees.append(driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').text) #Fetch employees of the company

        time.sleep(2)
        driver.back()
        time.sleep(2)
        driver.back()

    driver.back()
    wrongurl = driver.current_url
    time.sleep(3)
    if "https://www.linkedin.com/authwall?trk=qf&original_referer=" in wrongurl:
        driver.back()
        driver.find_element(By.XPATH,'/html/body/nav/ul/li[4]/a').click() #Click on jobs
driver.close()

print(jobposition)
print("\n")
print(companyname)
print("\n")
print(joblocation)
print("\n")
print(companylocation)
print("\n")
print(companyemployees)
print("\n")