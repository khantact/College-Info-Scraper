from bs4 import BeautifulSoup
import csv
import re
from pandas import array
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


# Helper Functions
# ----------------------------------------------------------------------------------------------------------------------


def extractInfo(info, before, after):
    info = re.split(before + '|' + after, info)
    del info[0::2]
    info = info[0].split('\n')
    for i in range(len(info)-1):
        if info[i] == '':
            del info[i]
    return info

# Array to String


def array_toString(array):
    string = ''
    for i in range(len(array)):
        string += array[i] + ', '
    return string


def elementToArray(element):
    array = []
    for i in range(len(element)):
        array.append(element[i].text)
    return array


def findElement(element, before: str, after: str, index: int):
    """Finds the requested element within a list of elements

    Args:
        element (list): list of elements
        before (str): string before the element
        after (str): string after the element

    Returns:
        str: returns the element
    """
    array = []
    found = False
    for i in range(len(element)):
        if element[i] == before:
            found = True
            array = []
            array.append(element[i])
        elif element[i] == after:
            if found == True:
                break
        else:
            array.append(element[i])
    return array[index]


def elementSplit(element: str, condition1: str, condition2: str):
    """Splits the element based on condition1 and condition2

    Args:
        element (str): WebElement str
        condition1 (str): a condition to split the text by
        condition2 (str): a condition to split the text by
    """
    element = re.split(condition1 + '|' + condition2, element)
    return element


def elementSplit(element: str, condition1: str, condition2: str, condition3: str):
    """Splits the element based on condition1, condition2 and condition3

    Args:
        element (str): WebElement str
        condition1 (str): a condition to split the text by
        condition2 (str): a condition to split the text by
    """
    element = re.split(condition1 + '|' + condition2 +
                       '|' + condition3, element)
    return element


# ----------------------------------------------------------------------------------------------------------------------
driver = webdriver.Chrome()
print("Opening Chrome...")
driver.get("https://nces.ed.gov/collegenavigator/")

file = open('collegeinfo.csv', 'w')
writer = csv.writer(file)

# Write header rows
writer.writerow(['College Name', 'Phone#', 'Website', 'Type', 'Degrees', 'Campus Type', 'Campus Housing',
                'Student Pop', 'StudentsToTeachers', 'MissionStatement', 'Classification', 'SLOs', 'Religious Affiliation',  'Credits Accepted', 'Faculty(full-time)', 'Faculty(part-time)', 'Graduate Assistants', 'Tuition', 'Books/Supplies', 'Room/Board',
                 'Total Expenses', 'Avg Tuition', 'Avg Aid(grants)', 'Gender Demographic(Male)', 'Gender Demographic(Female)', 'Ethnic Demographic (American Indian or Alaska Native)', 'Ethnic Demographic(Black or African American)',
                 'Ethnic Demographic(Hispanic/Latino)', 'Ethnic Demographic(Native Hawaiian or other Pacific Islander)', 'Ethnic Demographic(White)', 'Ethnic Demographic(Two or more races)', 'Ethnic Demographic(Unknown)',
                 'Ethnic Demographic(Non-resident alien)', 'Avg Student Age', 'Avg Student Residence', 'Graduate Attendance Status', 'Undergraduate Remote Status', 'Graduate Remote Status', 'Total Applicants', 'Percent Admitted', 'Percent Admitted Enrolled',
                 'Secondary School GPA', 'Secondary School Rank', 'Secondary School Record', 'Completion of College-Prep Program', 'Recommendation', 'SAT/ACT', 'TOEFL', 'Students Submitting Scores (SAT)', 'Students Submitting Scores (ACT)',
                 'SAT English 25th Percentile', 'SAT English 75th Percentile', 'SAT Math 25th percentile', 'SAT Math 75th Percentile', 'ACT Composite 25th Percentile', 'ACT Composite 75th Percentile', 'ACT English 25th Percentile',
                 'ACT English 75th Percentile', 'ACT Math 25th Percentile', 'ACT Math 75th Percentile', 'First-to-Second Year Retention Rate', 'Graduation/Transfer Rate', 'Graduation Rate (Male)', 'Graduation Rate (Female)',
                 'Graduation Rate by Race/Ethnicity(American Indian or Alaska Native)', 'Graduation Rate by Race/Ethnicity(Asian)', 'Graduation Rate by Race/Ethnicity(Black or African American)', 'Graduation Rate by Race/Ethnicity(Hispanic/Latino)',
                 'Graduation Rate by Race/Ethnicity(Native Hawaiian or other Pacific Islander)', 'Graduation Rate by Race/Ethnicity(White)', 'Graduation Rate by Race/Ethnicity(Two or more Races)', 'Graduation Rate by Race/Ethnicity(Race/Ethnicity Unknown)',
                 'Graduation Rate by Race/Ethnicity(Non-resident Alien)', 'Area,Ethnic,Cultural,Gender, and Group Studies',
                 'Biological and Biomedical Sciences', 'Computer and Information Sciences and Support Services', 'Education', 'English Languages, Literatures, and Linguistics', 'History', 'Liberal Arts and Sciences, General Studies and Humanities',
                 'Mathematics and Statistics', 'Multi/Interdisciplinary Studies', 'Natural Resources and Conservation', 'Philosophy and Religious Studies', 'Physical Sciences', 'Psychology', 'Social Sciences', 'Visual and Performing Arts',
                 'Murder/Non-negligent Manslaughter', 'Negligent Manslaughter', 'Rape', 'Fondling', 'Incest', 'Statutory Rape', 'Aggravated Assault', 'Burglary', 'Motor Vehicle Theft', 'Arson', 'Dating Violence', 'Stalking', 'Weapons Arrests',
                 'Drug Abuse Arrests', 'Liquor Law Violation Arrests', 'Weapons Disciplinary Action', 'Drug Abuse Disciplinary Action', 'Liquor Law Violation Disciplinary Action'])

# Inputs each college from a list of colleges and goes to their respective pages
collegeinput = driver.find_element(
    "xpath", "//input[@name='ctl00$cphCollegeNavBody$ucSearchMain$txtName']")
collegeinput.send_keys("Colgate University")
driver.find_element(
    'xpath', "//input[@name='ctl00$cphCollegeNavBody$ucSearchMain$btnSearch']").click()
driver.find_element('xpath', '//a[strong]').click()
driver.find_element(
    'xpath', '// a[@onclick="dall(true);return(false);"]').click()


# Datasets
generalinfo = driver.find_element(
    'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divNPC"]').text
tuitiondataset = elementToArray(driver.find_elements(
    'xpath', '//div[@class="tabconstraint"]//table/tbody/tr/td'))

missionstatement = driver.find_element(
    'xpath', '//div[@class="mscontainer"]/a')
classification = extractInfo(
    generalinfo, 'Carnegie Classification', 'Religious Affiliation')
slo = extractInfo(
    generalinfo, 'Special Learning Opportunities', 'Student Services')
religion = extractInfo(
    generalinfo, 'Religious Affiliation', 'Federal Aid')
creditsaccepted = extractInfo(generalinfo, 'Credit Accepted', 'n/a')
ftfaculty = driver.find_elements(
    'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty"]/div/table/tbody/tr/td')[1].text
ptfaculty = driver.find_elements(
    'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty"]/div/table/tbody/tr/td')[2].text
gradassistants = driver.find_elements(
    'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty"]/div/table/tbody/tr/td')[11].text
tuition = (findElement(
    tuitiondataset, 'Tuition and fees', 'Books and supplies', -2))
booksandsupplies = (findElement(
    tuitiondataset, 'Books and supplies', 'Living arrangement', -2))
roomandboard = (findElement(tuitiondataset, 'Room and board', 'Other', -2))
totalexpenses = (findElement(tuitiondataset, 'TOTAL EXPENSES', '', -2))
avgtuition = (findElement(tuitiondataset, 'Tuition', 'Fees', -1))
avg_aid = (findElement(tuitiondataset,
                       'Grant or scholarship aid', 'Federal grants', -1))
maledemographic = elementSplit(driver.find_elements(
    'xpath', '//table[@class="graphtabs"]/tbody/tr/td/img')[1].get_attribute('alt'), ':\n', ': ', '\n')[-3]
femaledemographic = elementSplit(driver.find_elements(
    'xpath', '//table[@class="graphtabs"]/tbody/tr/td/img')[1].get_attribute('alt'), ':\n', ': ', '\n')[-1]


# TODO
writer.writerow(['Colgate University', '999-999-9999', 'tobeimplemented.com', '4-year',
                "Bachelor's Degree , Master's degree", 'Town: Distant', 'Yes', '3421', '9 to 1', missionstatement.text, array_toString(
                    classification), array_toString(slo), array_toString(religion),
                 array_toString(creditsaccepted), ftfaculty, ptfaculty, gradassistants, tuition, booksandsupplies, roomandboard, totalexpenses, avgtuition, avg_aid, maledemographic, femaledemographic])

# Testing

# Clean up
file.close()
driver.quit()
