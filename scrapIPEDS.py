from tkinter.font import names
from matplotlib.pyplot import table
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


def processState(state, namesOfColleges):
    stateLink = "https://nces.ed.gov/collegenavigator/?s="+state

    for index in range(1, 100):
        pageLink = stateLink + "&pg=" + str(index)
        print(pageLink)
        driver.get(pageLink)

        try:

            findLinksToIndividualCollege(namesOfColleges)
        except:
            break


def findLinksToIndividualCollege(namesOfColleges):

    tableTag = driver.find_element(By.CLASS_NAME, "resultsTable")
    tbodyTag = tableTag.find_element(By.TAG_NAME, "tbody")

    trTags = tbodyTag.find_elements(By.XPATH, "./*")

    for trTag in trTags:
        tdTag = trTag.find_elements(By.XPATH, "./*")[1]
        aTag = tdTag.find_element(By.TAG_NAME, "a")
        # atag.click
        # scraper
        # back
        name = aTag.find_element(By.TAG_NAME, "strong")
        namesOfColleges.append(name.get_attribute("innerHTML"))
        print(name.get_attribute("innerHTML"))


def writeToFile(namesOfColleges):

    with open('listOfColleges.txt', 'w') as f:

        for name in namesOfColleges:
            f.write(name+"\n")


def main():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
              "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "AS", "FM", "GU", "MH", "MP", "PW", "PR", "VI"]

    namesOfColleges = []

    for state in states:
        processState(state, namesOfColleges)

    writeToFile(namesOfColleges)


main()
