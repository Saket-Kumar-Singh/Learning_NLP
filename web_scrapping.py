#Web_Scrpapping 
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.maximize_window()

driver.get("https://techport.nasa.gov/search")

search = driver.find_element(By.NAME, value = "searchVO.searchCriteria.searchOptions[0].input")

search.send_keys("Quantum")
button = driver.find_element(By.CLASS_NAME, "button-search")
button.click()

# urls = [ "https://techport.nasa.gov/view/118363"]
urls = []

box_ele = driver.find_element("xpath" , "//*[@id=\"search-results\"]/div[2]")
# print(box_ele)//*[@id="search-results"]/div[2]/div[20]/div[1]/div/div/div[1]/div/div/div[1]/h2/a
button = driver.find_element("xpath", f"//*[@id=\"search-results\"]/div[3]/div/div/div/a[3]")
for j in range(32):
    for i in range(20): 
        try:
            ele = driver.find_element("xpath", f"//*[@id=\"search-results\"]/div[2]/div[{i+1}]/div[1]/div/div/div[1]/div/div/div[1]/h2/a")
            urls.append(ele.get_attribute("href"))
        except:
            break
    try:    
        button = driver.find_element("xpath", f"//*[@id=\"search-results\"]/div[3]/div/div/div/a[3]")
        button.click()
    except:
        print(f"Button clicking issue at page {j+1}")
        break    

data = []

for Url in urls:
    txt = {} 
    print(f"Extracting data from URL : {Url}")
    html_text = requests.get(Url).text
    soup = BeautifulSoup(html_text, 'lxml')

    project_organisation = soup.find('div', class_ = 'sidebar-box project-organization')
    project_management = soup.find('div', class_ = 'sidebar-box project-management')
    project_duration = soup.find('div', class_ = 'sidebar-box project-duration')

    project_organisation = project_organisation.find('div', class_ = 'box-content collapsed')
    project_management = project_management.find('div', class_ = 'box-content collapsed')
    project_duration = project_duration.find('div', class_ = 'box-content collapsed')

    projects = project_organisation.find_all('h5')
    organisations = project_organisation.find_all('li')
    for i,project in enumerate(projects):
        txt[project.text.replace(" ", "").strip()] = organisations[i].text.replace('\n','').replace('\t','').strip()
    
    project_management_columns = project_management.find_all('div', class_ = 'box-content-column')
    for column in project_management_columns:
        txt[column.find('h5').text.replace(' ', '').replace('\n','').replace('\t','')] = column.find('li').text.replace(' ', '').replace('\n','').replace('\t','')
    
    durations = project_duration.find_all('div', class_ = 'box-content-column')
    # print(durations)
    for duration in durations:
        # print()
        txt[duration.find('strong').text.replace(' ', '').replace('\n','').replace('\t','')[:-1]] = duration.text.replace(' ', '').replace('\n','').replace('\t','').split(':')[1]

    data.append(txt)

# print(data)
data = pd.DataFrame(data)
data.to_csv("Quantum_Mission_Data.csv")
# print(data)
driver.quit()