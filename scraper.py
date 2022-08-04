import os
import csv
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

# Helper Functions
# ----------------------------------------------------------------------------------------------------------------------


def extractInfoFromGraph(element: list):
    """Generates a list of information given a list of WebElements from an image

    Args:
        element (list): list of WebElements
    """
    temp_array = []
    array = []
    for i in element:
        temp_array.append(elementSplit(
            i.get_attribute('alt'), ':\n', ': ', '\n'))
    for i in temp_array:
        array.extend(i)
    return array


def extractInfo(info, before, after):
    info = re.split(before + '|' + after, info)
    del info[0::2]
    info = info[0].split('\n')
    for i in range(len(info)-1):
        if info[i] == '':
            del info[i]
    return info


def search(element: list, search: str, strict: bool = False, skipfirst: bool = False):
    """Searches the list for a string strict determines if it must match directly

    Args:
        element (list): list of elements
        search (str): what to search for
        strict (bool): if true, will check if search is directly equal instead of just using in
        skipfirst (bool): if true, will skip the first element that was matched in the list

    Returns:
        bool: returns true if found, false if not found
    """
    for i in element:
        if strict == False:
            if search in i:
                if skipfirst == True:
                    continue
                return True
        else:
            if search == i:
                if skipfirst == True:
                    continue
                return True
    return False


def array_toString(array):
    """Converts an array to a string separated by commas


    Args: array (list): A list of elements to be converted to a string

    Returns:
        string (str): A string of the elements separated by commas
    """
    string = ",".join(array)
    return string


def elementToList(element):
    """Generates a list of elements from element WebElement

    Args:
        element (WebElement): WebElement Object to be converted to list

    Returns:
        list: A list of the elements within the WebElement Object
    """
    array = []
    for i in range(len(element)):
        array.append(element[i].text)
    return array


def findElementInGraph(element: list, search: str, strict: bool = False):
    """Searches within a list of images and finds their alt text and returns the correct image element that matches with the provided alt text

    Args:
        element (list): list of images
        search (str): string to search for 
        strict (bool, optional): determines if search should be strict or not. Defaults to False.

    Returns: 
        WebElement: returns the correct image element that matches with the provided alt text
        bool: returns false if the element is not found
    """
    for i in element:
        if strict == False:
            if search.lower() in i.get_attribute('alt').lower():
                return i.get_attribute('alt')
        else:
            if search.lower() == i.get_attribute('alt').lower():
                return i.get_attribute('alt')
    return False


def findElement(element: list, before: str, after, index: int, strict: bool = False, skipfirst: bool = False, numtoinclude: int = 1):
    """Finds the requested element within a list of elements given an index

    Args:
        element (list): list of elements (dataset)
        before (str): string before the element
        after (any): string after the element, if None, it will not be used
        index (int): index of the element to be found between before and after
        strict (bool): if true, will check if before/after are directly equal instead of just using in
        skipfirst (bool): if true, will skip the first element that was matched in the list
        numtoinclude (int): determines how many elements after the 'after' string to include in the final list
    Returns:
        str: returns the element
        bool: returns false if the element is not found
    """
    if element == False:
        return False
    array = []
    found = False
    if strict == False:
        if after == None:
            after = element[-1]
        for i in range(len(element)):
            if before in element[i]:
                if skipfirst == True:
                    skipfirst = False
                    continue
                found = True
                array = []
                array.append(element[i])

            elif after in element[i]:
                if found == True:
                    array.append(element[i])
                    if i+numtoinclude < len(element):
                        for j in range(1, numtoinclude+1):
                            array.append(element[i+j])
                        return array[index]
                    else:
                        return array[index]
            else:
                array.append(element[i])
    else:
        if after == None:
            after = element[-1]
        for i in range(len(element)):
            if element[i] == before:
                if skipfirst == True:
                    skipfirst = False
                    continue
                found = True
                array = []
                array.append(element[i])
            elif element[i] == after:
                if found == True:
                    array.append(element[i])
                    if i+1 < len(element):
                        array.append(element[i+1])
                        return array[index]
                    else:
                        return array[index]
            else:
                array.append(element[i])
    return False


def findAfterString(element: list, start: str, index: int, skipfirst: bool = False):
    """Finds the requested element within a list of elements starting at a start string

    Args:
        element (list): list of elements to search within
        start (str): find the start of the new list to create
        index (int): index of the requested element within the new list
        skipfirst (bool): if true, will skip the first element that was matched in the list

    Returns:
        str: returns the element
    """
    array = []
    for i in range(len(element)):
        if start in element[i]:
            if skipfirst == True:
                skipfirst = False
                continue
            for j in range(i, len(element)):
                array.append(element[j])
            return array[index]


def elementSlice(element: list, start: str, end: str):
    """Slices the element based on start and end

    Args:
        element (list): list of elements
        start (str): string before the element
        end (str): string after the element

    Returns:
        list: returns the element list starting from start and ending at end
    """
    array = []
    found = False
    for i in range(len(element)):
        if start in element[i]:
            found = True
            array = []
            array.append(element[i])
        elif end in element[i]:
            if found == True:
                return array
        else:
            array.append(element[i])
    return array


def elementSplit(element, condition1: str, condition2: str, condition3: str):
    """Splits the element based on condition1, condition2 and condition3, returns false if none of the conditions are met

    Args:
        element (str): WebElement str
        condition1 (str): a condition to split the text by
        condition2 (str): a condition to split the text by
    Returns:
        element (list): returns the split element in a list
    """
    if element == False:
        return False
    if condition2 == None and condition3 == None:
        element = re.split(condition1, element)
        return element
    elif condition3 == None:
        element = re.split(condition1 + '|' + condition2, element)
        return element
    elif condition3 != None:
        element = re.split(condition1 + '|' + condition2 +
                           '|' + condition3, element)
        return element
    return False


def stataddition(element: str, element2: str):
    """Adds two str elements (percent) together to return a combined percentage element

    Args:
        element (str): WebElement str
        element2 (str): WebElement str
    """
    element = element.replace('%', '')
    element2 = element2.replace('%', '')
    element = int(element) + int(element2)
    return str(element) + '%'


def determineRequirement(element: list):
    """Determines the requirement of the course

    Args:
        element (list): A list of X and '' elements

    Returns:
        string (str): Whether something is required, recommended or considered but not required
    """
    if element[1] == 'X':
        return 'Required'
    elif element[2] == 'X':
        return 'Recommended'
    else:
        return 'Considered but not required'


def cleanList(element: list):
    """Cleans the list of elements by removing empty elements

    Args:
        element (list): A list of elements to be cleaned

    Returns:
        list: Returns the cleaned list
    """
    return list(filter(None, element))

# --------------------------------------------Navigation Functions---------------------------------------------------


def navigateToSite():
    def processState(state, namesOfColleges):
        stateLink = "https://nces.ed.gov/collegenavigator/?s="+state

        for index in range(1, 100):
            pageLink = stateLink + "&pg=" + str(index)
            driver.get(pageLink)
            time.sleep(1)
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
            name = aTag.find_element(By.TAG_NAME, "strong").text
            print('Analyzing '+name)
            aTag.click()
            scraper(name, 'collegeinfo.csv')
            driver.execute_script('window.history.go(-1)')

    def start():
        states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
                  "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "AS", "FM", "GU", "MH", "MP", "PW", "PR", "VI"]
        namesOfColleges = []
        for state in states:
            processState(state, namesOfColleges)

    start()

# ----------------------------------------------------------------------------------------------------------------------


def scraper(college: str, filename: str):
    """Goes to the CollegeNavigator from the National Center for Education Statistics website and scrapes the data for each college in the list (listOfColleges.txt) and writes it to a csv file(collegeinfo.csv)

    Args:
        college (str): The college to be scraped
        filename (str): The name of the csv file to be written to

    Returns:
        bool: Returns True if the college was successfully scraped
    """
    file = open(filename, 'a+', newline='')
    writer = csv.writer(file)

    driver.find_element(
        'xpath', "//div[@class='fadeyell']/div[@class='expandcollapse colorful']/a[1]").click()
    # Write header rows
    if os.stat(filename).st_size == 0:
        writer.writerow(['College Name', 'Address', 'Phone#', 'Website', 'Type', 'Degrees', 'Campus Type', 'Campus Housing',
                        'Student Pop', 'StudentsToTeachers', 'MissionStatement', 'Classification', 'SLOs', 'Religious Affiliation',  'Credits Accepted', 'Faculty(full-time)', 'Faculty(part-time)', 'Graduate Assistants', 'Tuition', 'Books/Supplies', 'Room/Board',
                         'Total Expenses', 'Undergraduate Avg Tuition (In-State)', 'Undergraduate Avg Tuition (Out-of-State)', 'Graduate Avg Tuition (In-State)', 'Graduate Avg Tuition (Out-of-State)', 'Avg Tuition', 'Avg Aid(grants)', 'Gender Demographic(Male)', 'Gender Demographic(Female)', 'Ethnic Demographic (American Indian or Alaska Native)', 'Ethnic Demographic (Asian)', 'Ethnic Demographic(Black or African American)',
                         'Ethnic Demographic(Hispanic/Latino)', 'Ethnic Demographic(Native Hawaiian or other Pacific Islander)', 'Ethnic Demographic(White)', 'Ethnic Demographic(Two or more races)', 'Ethnic Demographic(Unknown)',
                         'Ethnic Demographic(Non-resident alien)', 'Avg Student Age (24 and Under)', 'Avg Student Age(25 and Over)', 'Avg Student Residence (In-State)', 'Avg Student Residence(Out-of-State)', 'Avg Student Residence(Foreign Countries)',
                         'Graduate Attendance Status(Full-time)', 'Graduate Attendance Status(Part-time)', 'Undergraduate Education Status (Remote)', 'Undergraduate Education Status (In-Person)', 'Graduate Education Status (Remote)', 'Graduate Education Status (In-Person)',
                         'Application Fee', 'Total Applicants', 'Percent Admitted', 'Percent Admitted Enrolled', 'Secondary School GPA', 'Secondary School Rank', 'Secondary School Record', 'Completion of College-Prep Program', 'Recommendation', 'SAT/ACT', 'TOEFL',
                         'Students Submitting Scores (SAT)',
                         'Students Submitting Scores (ACT)', 'SAT English 25th Percentile', 'SAT English 75th Percentile', 'SAT Math 25th percentile', 'SAT Math 75th Percentile', 'ACT Composite 25th Percentile', 'ACT Composite 75th Percentile', 'ACT English 25th Percentile',
                         'ACT English 75th Percentile', 'ACT Math 25th Percentile', 'ACT Math 75th Percentile', 'First-to-Second Year Retention Rate', 'Graduation Rate', 'Transfer Rate', 'Graduation Rate (Male)', 'Graduation Rate (Female)',
                         'Graduation Rate by Race/Ethnicity(American Indian or Alaska Native)', 'Graduation Rate by Race/Ethnicity(Asian)', 'Graduation Rate by Race/Ethnicity(Black or African American)', 'Graduation Rate by Race/Ethnicity(Hispanic/Latino)',
                         'Graduation Rate by Race/Ethnicity(Native Hawaiian or other Pacific Islander)', 'Graduation Rate by Race/Ethnicity(White)', 'Graduation Rate by Race/Ethnicity(Two or more Races)', 'Graduation Rate by Race/Ethnicity(Race/Ethnicity Unknown)',
                         'Graduation Rate by Race/Ethnicity(Non-resident Alien)',
                         'Murder/Non-negligent Manslaughter', 'Negligent Manslaughter', 'Rape', 'Fondling', 'Incest', 'Statutory Rape', 'Robbery', 'Aggravated Assault', 'Burglary', 'Motor Vehicle Theft', 'Arson', 'Domestic Violence', 'Dating Violence', 'Stalking', 'Weapons Arrests',
                         'Drug Abuse Arrests', 'Liquor Law Violation Arrests', 'Weapons Disciplinary Action', 'Drug Abuse Disciplinary Action', 'Liquor Law Violation Disciplinary Action', 'Programs'])

    # Inputs each college from a list of colleges and goes to their respective pages

    # Datasets -----------------------------------------------------------------------------------
    try:
        dashboarddataset = elementToList(driver.find_elements(
            'xpath', "//div[2]/table[@class='layouttab']/tbody/tr"))
    except NoSuchElementException:
        print(college + ' is missing vital data (dashboard info), skipping...')

    # -------------------------------------------------------------------------------------------
    with open('collegeinfo.csv', 'rt') as f:
        s = f.read()
        if college in s:
            print(college + ' already scraped, skipping...')
            return True
    # Check college/university validity
    if search(dashboarddataset, 'Related Institutions') == True and search(dashboarddataset, 'parent institution') == False:
        print(college + " is a branch of a parent college, skipping...")
        file.close()
        # driver.quit()
        return False
    try:
        if 'RETENTION' not in driver.find_element('xpath', "//div[@id='retgrad']/div[@class='collapsing2']").text:
            print(college + " is missing vital data (retention/grad rates), skipping...")
            file.close()
            driver.quit()
            return False
    except NoSuchElementException:
        print(college + " is missing vital data (retention/grad rates), skipping...")
        file.close()
        driver.quit()
        return False
    university = False
    if 'University' in college:
        university = True

    if 'Community College' in college:
        u_remotelearningdataset = driver.find_element(
            'xpath', "//div[@class='tabconstraint']/table[@class='graphtabs'][4]/tbody/tr/td/img").get_attribute('alt')
    try:
        u_remotelearningdataset = driver.find_element(
            'xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl03']/div[@class='tabconstraint']/table[@class='graphtabs'][5]/tbody/tr/td[1]/img").get_attribute('alt')
    except NoSuchElementException:
        u_remotelearningdataset = None
    try:
        g_remotelearningdataset = driver.find_element(
            'xpath', "//table[@class='graphtabs'][5]/tbody/tr/td[2]/img").get_attribute('alt')
    except NoSuchElementException:
        g_remotelearningdataset = None
    crimedataset = elementToList(driver.find_elements(
        'xpath', '//div[@id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl11"]/div/table/tbody/tr/td'))
    genderdemographicdataset = driver.find_element(
        'xpath', "//table[@class='graphtabs'][1]/tbody/tr/td[2]/img")
    # Datasets
    generalinfo = driver.find_element(
        'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divNPC"]').text
    dashboarddataset = elementToList(driver.find_elements(
        'xpath', "//div[2]/table[@class='layouttab']/tbody/tr"))
    tuitiondataset = elementToList(driver.find_elements(
        'xpath', "//div[@id = 'divctl00_cphCollegeNavBody_ucInstitutionMain_ctl00']/div[@class = 'tabconstraint']/table[@class = 'tabular']/tbody/tr/td"))
    admissiondataset = elementToList(driver.find_elements(
        'xpath', '//div[@id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04"]/div/table/tbody/tr/td'))
    graphdataset = driver.find_elements(
        'xpath', '//table[@class="graphtabs"]/tbody/tr/td/img')
    aiddataset = elementToList(driver.find_elements(
        'xpath', "//div[@id='RightContent']/div[9]/div[@id='finaid']/div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl01']/div/table/tbody/tr/td"))
    # --------------------------------------------------Data----------------------------------------------------------------
    address = elementSplit(driver.find_element(
        'xpath', "//div[@class='collegedash']/div[2]/span").text, '\n', None, None)[1]
    phonenum = driver.find_element(
        'xpath', "//div[2]/table[@class='layouttab']/tbody/tr[1]/td[2]").text
    website = driver.find_element(
        'xpath', "//div[2]/table[@class='layouttab']/tbody/tr[2]/td[2]").text
    type = driver.find_element(
        'xpath', "//div[2]/table[@class='layouttab']/tbody/tr[3]/td[2]").text
    awardsoffered = array_toString(cleanList(elementSplit(driver.find_element(
        'xpath', "//div[@class='collegedash']/div[2]/table[@class='layouttab']/tbody/tr[4]/td[2]").text, "([A-Z][^A-Z]*)", '\n', '')))
    campussetting = driver.find_element(
        'xpath', "//table[@class='layouttab']/tbody/tr[5]/td[2]").text
    campushousing = driver.find_element(
        'xpath', "//table[@class='layouttab']/tbody/tr[6]/td[2]").text
    studentpop = driver.find_element(
        'xpath', "//table[@class='layouttab']/tbody/tr[7]/td[2]").text
    try:
        if search(dashboarddataset, 'Student-to-faculty ratio'):
            studenttofaculty = elementSplit(
                dashboarddataset[7], ':   ', None, None)[1]
        else:
            studenttofaculty = 'n/a'
    except NoSuchElementException:
        studenttofaculty = 'n/a'

    missionstatement = elementSplit(driver.find_element(
        'xpath', '//div[@class="mscontainer"]').text, '\n  ', None, None)[1]
    classification = extractInfo(
        generalinfo, 'Carnegie Classification', 'Religious Affiliation')
    slo = extractInfo(
        generalinfo, 'Special Learning Opportunities', 'Student Services')
    religion = extractInfo(
        generalinfo, 'Religious Affiliation', 'Federal Aid')
    creditsaccepted = extractInfo(generalinfo, 'Credit Accepted', 'n/a')
    ptfaculty = "n/a"
    # Check if faculty datra is combined with a parent institution
    if 'parent institution' in driver.find_element('xpath', "//div[@id='ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty']/div[@class='detailseparate']").text:
        driver.find_element(
            'xpath', "//div[@id='ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty']/div[@class='detailseparate']/a").click()
        driver.find_element(
            'xpath', "//div[@id='RightContent']/div[@class='fadeyell']/div[@class='expandcollapse colorful']/a[1]").click()
        ftfaculty = driver.find_elements(
            'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty"]/div/table/tbody/tr/td')[1].text
        try:
            gradassistants = driver.find_element(
                'xpath', "//div[@class='detailseparate']/table[@class='tabular']/tbody/tr[4]/td[3]").text
        except NoSuchElementException:
            gradassistants = 'n/a'
        driver.execute_script('window.history.go(-1)')
        driver.find_element(
            'xpath', "//div[@id='RightContent']/div[@class='fadeyell']/div[@class='expandcollapse colorful']/a[1]").click()
    else:
        ftfaculty = driver.find_elements(
            'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty"]/div/table/tbody/tr/td')[1].text
        ptfaculty = driver.find_elements(
            'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divFaculty"]/div/table/tbody/tr/td')[2].text
    if university:
        try:
            gradassistants = driver.find_element(
                'xpath', "//div[@class='detailseparate']/table[@class='tabular']/tbody/tr[4]/td[3]").text
        except NoSuchElementException:
            gradassistants = 'n/a'
    booksandsupplies = (findElement(
        tuitiondataset, 'Books and supplies', 'Living arrangement', 4, False))
    roomandboard = (findElement(
        cleanList(tuitiondataset), 'Room and board', '%', 4))
    totalexpenses = (findElement(
        cleanList(tuitiondataset), '% CHANGE', '%', 6))

    # -----------------------------------------------------Tuition----------------------------------------------------------------
    instatetuition = 'n/a'
    outofstatetuition = 'n/a'
    avgtuition = 'n/a'
    tuition = 'n/a'
    g_instatetuition = 'n/a'
    g_outofstatetuition = 'n/a'
    try:
        if 'In-state' not in (cleanList(tuitiondataset)) and '%' in cleanList(tuitiondataset):
            tuition = findElement(cleanList(tuitiondataset),
                                  'Tuition and fees', '%', 4)
        if 'In-state' not in cleanList(tuitiondataset) and '%' not in cleanList(tuitiondataset):
            tuition = findElement(cleanList(tuitiondataset),
                                  'Tuition', 'Fees', 1, True)
    except NoSuchElementException:
        tuition = 'n/a'
    try:
        if search(cleanList(tuitiondataset), 'Graduate student tuition'):
            if search(cleanList(tuitiondataset), 'In-state tuition', True, True) and search(tuitiondataset, '%'):
                g_instatetuition = (findElement(cleanList(
                    tuitiondataset), 'In-state tuition', None, 4, True, True))
            else:
                g_instatetuition = (findElement(cleanList(
                    tuitiondataset), 'In-state tuition', None, 1, True, True))
            if search(cleanList(tuitiondataset), 'Out-of-state tuition', True, True) and search(tuitiondataset, '%'):
                g_outofstatetuition = (findElement(cleanList(
                    tuitiondataset), 'Out-of-state tuition', None, 4, True, True))
            else:
                g_outofstatetuition = (findElement(cleanList(
                    tuitiondataset), 'Out-of-state tuition', None, 1, True, True))

    except NoSuchElementException:
        pass
    try:
        if search(aiddataset, 'Grant or scholarship aid'):
            avg_aid = findElement(
                aiddataset, 'Grant or scholarship aid', '$', -1)
        else:
            avg_aid = 'n/a'
    except NoSuchElementException:
        avg_aid = 'n/a'

    try:
        if search(cleanList(tuitiondataset), 'In-state'):
            if search(tuitiondataset, '%'):
                instatetuition = (findElement(cleanList(
                    tuitiondataset), 'In-state', '%', 4))
            else:
                instatetuition = (findElement(cleanList(
                    tuitiondataset), 'In-state', '$', 1))
        if search(cleanList(tuitiondataset), 'Out-of-state'):
            if search(tuitiondataset, '%'):
                outofstatetuition = findElement(
                    cleanList(tuitiondataset), 'Out-of-state', '%', 4)
            else:
                outofstatetuition = findElement(
                    cleanList(tuitiondataset), 'Out-of-state', '$', 1)
    except NoSuchElementException:
        instatetuition = 'n/a'
        outofstatetuition = 'n/a'


# Redeclare datasets due to page backing
    generalinfo = driver.find_element(
        'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divNPC"]').text
    tuitiondataset = elementToList(driver.find_elements(
        'xpath', '//div[@class="tabconstraint"]//table/tbody/tr/td'))
    admissiondataset = elementToList(driver.find_elements(
        'xpath', '//div[@id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04"]/div/table/tbody/tr/td'))
    graphdataset = driver.find_elements(
        'xpath', '//table[@class="graphtabs"]/tbody/tr/td/img')
    genderdemographicdataset = driver.find_element(
        'xpath', "//table[@class='graphtabs'][1]/tbody/tr/td[2]/img")
    crimedataset = elementToList(driver.find_elements(
        'xpath', '//div[@id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl11"]/div/table/tbody/tr/td'))
    # ---------------------------------------------------------------------------------------------------------------------
    maledemographic = elementSplit(
        genderdemographicdataset.get_attribute('alt'), ':\n', ': ', '\n')[2]
    femaledemographic = elementSplit(
        genderdemographicdataset.get_attribute('alt'), ':\n', ': ', '\n')[-1]
    # Correlates to the different ethnicities and their makeup of college population
    ethnicitygraph = elementSplit(
        graphdataset[2].get_attribute('alt'), ':\n', ': ', '\n')
    ethnic1 = ethnicitygraph[2]
    ethnic2 = ethnicitygraph[4]
    ethnic3 = ethnicitygraph[6]
    ethnic4 = ethnicitygraph[8]
    ethnic5 = ethnicitygraph[10]
    ethnic6 = ethnicitygraph[12]
    ethnic7 = ethnicitygraph[14]
    ethnic8 = ethnicitygraph[16]
    ethnic9 = ethnicitygraph[18]
    # Age context being 24
    underage = elementSplit(
        graphdataset[3].get_attribute('alt'), ':\n', ': ', '\n')[2]
    overage = elementSplit(
        graphdataset[3].get_attribute('alt'), ':\n', ': ', '\n')[4]

    # Distinguishes between a university and college
    if university:
        fulltimegraduate = elementSplit(
            graphdataset[5].get_attribute('alt'), ':\n', ': ', '\n')[2]
        parttimegraduate = elementSplit(
            graphdataset[5].get_attribute('alt'), ':\n', ': ', '\n')[4]
        u_remotelearning = stataddition(
            elementSplit(u_remotelearningdataset, ':\n', ': ', '\n')[2],
            elementSplit(u_remotelearningdataset, ':\n', ': ', '\n')[4])
        u_inpersonlearning = elementSplit(
            u_remotelearningdataset, ':\n', ': ', '\n')[6]
        g_remotelearning = stataddition(
            elementSplit(g_remotelearningdataset, ':\n', ': ', '\n')[2],
            elementSplit(g_remotelearningdataset, ':\n', ': ', '\n')[4])
        g_inpersonlearning = elementSplit(
            g_remotelearningdataset, ':\n', ': ', '\n')[6]

    else:
        remotelearndata = extractInfoFromGraph(graphdataset)
        fulltimegraduate = 'n/a'
        parttimegraduate = 'n/a'
        g_remotelearning = 'n/a'
        g_inpersonlearning = 'n/a'
        gradassistants = 'n/a'
        u_remotelearning = 'n/a'
        u_inpersonlearning = 'n/a'
        if findElement(remotelearndata, 'Undergraduate Enrollment by Distance Education', 'Not enrolled in any distance', 2) != False:
            u_remotelearning = stataddition(
                findElement(remotelearndata, 'Undergraduate Enrollment by Distance Education', 'Not enrolled in any distance', 2), findElement(remotelearndata, 'Undergraduate Enrollment by Distance Education', 'Not enrolled in any distance', 4))
            u_inpersonlearning = findElement(extractInfoFromGraph(
                graphdataset), 'Undergraduate Enrollment by Distance Education', 'Not enrolled in any distance', -1)
        if findElement(remotelearndata, 'Graduate Enrollment by Distance Education', 'Not enrolled in any distance', 2) != False:
            g_remotelearning = stataddition(
                findElement(remotelearndata, 'Enrolled only in distance education', 'Not enrolled in any distance', 1), findElement(remotelearndata, 'Enrolled only in distance education', 'Not enrolled in any distance', 3))
            for i in range(len(extractInfoFromGraph(graphdataset))):
                if extractInfoFromGraph(graphdataset)[i] == 'Not enrolled in any distance education':
                    g_inpersonlearning = extractInfoFromGraph(graphdataset)[
                        i + 1]
                    break
    #--------------------------------------Student Avg Residence--------------------------------------------------------#
    try:
        residence = elementSplit(driver.find_element(
            'xpath', "//table[@class='graphtabs'][3]/tbody/tr/td[2]/img").get_attribute('alt'), ':\n', ': ', '\n')
        instateresidence = residence[2]
        outofstateresidence = residence[4]
        foreigncountriesresidence = residence[6]
    except NoSuchElementException:
        instateresidence = 'n/a'
        outofstateresidence = 'n/a'
        foreigncountriesresidence = 'n/a'
    #----------------------------------------------------------------------------------------------#
    openadmission = 'open admission policy contact institution for more information'
    applicationfee = 'open admission policy contact institution for more information'
    if '$' in driver.find_element('xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04']/div[@class='tabconstraint']").text:
        applicationfee = driver.find_element(
            'xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04']/div[@class='tabconstraint']/table[@class='tabular'][1]/tbody/tr/td[2]").text
    if 'open admission policy' in driver.find_element('xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04']/div[@class='tabconstraint']").text:
        applicationfee = driver.find_element(
            'xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04']/div[@class='tabconstraint']").text
        totalapplicants = openadmission
        percentadmitted = openadmission
        admittedandenrolled = openadmission
        secondaryschoolgpa = openadmission
        secondaryschoolrank = openadmission
        secondarschoolrecord = openadmission
        collegeprepprogram = openadmission
        recommendations = openadmission
        admissiontestscores = openadmission
        toefl = openadmission
    else:
        if 'UNDERGRADUATE ADMISSIONS' not in driver.find_element(
                'xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04']/div[@class='tabconstraint']/div").text:
            noadmit = driver.find_element(
                'xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04']/div[@class='tabconstraint']/div").text
            totalapplicants = noadmit
            percentadmitted = noadmit
            admittedandenrolled = noadmit
            secondaryschoolgpa = noadmit
            secondaryschoolrank = noadmit
            secondarschoolrecord = noadmit
            collegeprepprogram = noadmit
            recommendations = noadmit
            admissiontestscores = noadmit
            toefl = noadmit
        else:
            # TODO fix this secntion
            totalapplicants = findElement(
                admissiondataset, 'Number of applicants', 'Percent admitted', 1)
            percentadmitted = findElement(
                admissiondataset, 'Percent admitted', '%', 1)
            admittedandenrolled = findElement(
                admissiondataset, 'Percent admitted who enrolled', 'Secondary school GPA', 1)
            secondaryschoolgpa = determineRequirement(elementSlice(
                admissiondataset, 'Secondary school GPA', 'Secondary school rank'))
            secondaryschoolrank = determineRequirement(elementSlice(
                admissiondataset, 'Secondary school rank', 'Secondary school record'))
            secondarschoolrecord = determineRequirement(elementSlice(
                admissiondataset, 'Secondary school record', 'Completion of college-preparatory program'))
            collegeprepprogram = determineRequirement(elementSlice(
                admissiondataset, 'Completion of college-preparatory program', 'Recommendations'))
            recommendations = determineRequirement(elementSlice(
                admissiondataset, 'Recommendations', 'Admission test scores (SAT/ACT)'))
            admissiontestscores = determineRequirement(elementSlice(
                admissiondataset, 'Admission test scores (SAT/ACT)', 'TOEFL (Test of English as a Foreign language)'))
            toefl = determineRequirement(elementSlice(
                admissiondataset, 'TOEFL (Test of English as a Foreign language)', 'SAT'))
    #----------------------------------------------------------------------------------------------#
    if 'SAT' in admissiondataset:
        submittingsat = findElement(admissiondataset, 'SAT', None, 2, True)
        submittingact = findElement(admissiondataset, 'ACT', None, 2, True)
        sat_en_lowpercentile = findElement(
            admissiondataset, 'SAT Evidence-Based Reading and Writing', 'SAT Math', 1)
        sat_en_highpercentile = findElement(
            admissiondataset, 'SAT Evidence-Based Reading and Writing', 'SAT Math', 2)
        sat_math_lowpercentile = findElement(
            admissiondataset, 'SAT Math', None, 1)
        sat_math_highpercentile = findElement(
            admissiondataset, 'SAT Math', None, 2)
        act_composite_lowpercentile = findElement(
            admissiondataset, 'ACT Composite', 'ACT English', 1)
        act_composite_highpercentile = findElement(
            admissiondataset, 'ACT Composite', 'ACT English', 2)
        act_english_lowpercentile = findElement(
            admissiondataset, 'ACT English', 'ACT Math', 1)
        act_english_highpercentile = findElement(
            admissiondataset, 'ACT English', 'ACT Math', 2)
        act_math_lowpercentile = findElement(
            admissiondataset, 'ACT Math', None, 1)
        act_math_highpercentile = findElement(
            admissiondataset, 'ACT Math', None, 2)
    else:
        submittingsat = 'n/a'
        submittingact = 'n/a'
        sat_en_lowpercentile = 'n/a'
        sat_en_highpercentile = 'n/a'
        sat_math_lowpercentile = 'n/a'
        sat_math_highpercentile = 'n/a'
        act_composite_lowpercentile = 'n/a'
        act_composite_highpercentile = 'n/a'
        act_english_lowpercentile = 'n/a'
        act_english_highpercentile = 'n/a'
        act_math_lowpercentile = 'n/a'
        act_math_highpercentile = 'n/a'
    #----------------------------------------------------------------------------------------------#

    if 'RETENTION' in driver.find_element('xpath', "//div[@id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl05']/div[@class='tabconstraint']/div[1]").text:
        retentionrate = findElement(elementSplit(
            findElementInGraph(graphdataset, 'retention'), ':\n', ': ', '\n'), 'Student retention', '%', 2)
        graduationrate = findElement(elementSplit(
            findElementInGraph(graphdataset, 'graduation rate'), ':\n', ': ', '\n'), 'Overall graduation rate', '%', 1, False, True)
        transferrate = findElement(elementSplit(
            findElementInGraph(graphdataset, 'Transfer-out rate'), ':\n', ': ', '\n'), 'Transfer-out rate', '%', 1)
        gradratemale = findElement(elementSplit(
            findElementInGraph(graphdataset, 'Graduation Rate by Gender'), ':\n', ': ', '\n'), 'Male', '%', 1)
        gradratefemale = findElement(elementSplit(
            findElementInGraph(graphdataset, 'Graduation Rate by Gender'), ':\n', ': ', '\n'), 'Female', '%', 1)
        gradrate = elementSplit(
            findElementInGraph(graphdataset, 'Graduation Rate by Race/Ethnicity'), ':\n', ': ', '\n')
        gradrateindiannative = findElement(
            gradrate, 'American Indian', '%', 1)
        gradrateasian = findElement(gradrate, 'Asian', '%', 1)
        gradrateblack = findElement(gradrate, 'Black', '%', 1)
        gradratehispanic = findElement(gradrate, 'Hispanic', '%', 1)
        gradratehawaiian = findElement(gradrate, 'Native Hawaiian', '%', 1)
        gradratewhite = findElement(gradrate, 'White', '%', 1)
        gradratetwoormore = findElement(gradrate, 'Two or more', '%', 1)
        gradrateunknown = findElement(gradrate, 'unknown', '%', 1)
        gradratealien = findElement(gradrate, 'alien', '%', 1)
    else:
        retentionrate = ''
        graduationrate = ''
        transferrate = ''
        gradratemale = ''
        gradratefemale = ''
        gradrateindiannative = ''
        gradrateasian = ''
        gradrateblack = ''
        gradratehispanic = ''
        gradratehawaiian = ''
        gradratewhite = ''
        gradratetwoormore = ''
        gradrateunknown = ''
        gradratealien = ''

        #-----------------------------------Crime Statistics----------------------------------------------#
    murders = findElement(
        crimedataset, 'a. Murder/Non-negligent manslaughter', 'b. Negligent manslaughter', 3)
    manslaughter = findElement(
        crimedataset, 'b. Negligent manslaughter', 'c. Rape', 3)
    rape = findElement(
        crimedataset, 'c. Rape', 'd. Fondling', 3)
    fondling = findElement(
        crimedataset, 'd. Fondling', 'e. Incest', 3)
    incest = findElement(
        crimedataset, 'e. Incest', 'f. Statutory Rape', 3)
    statutoryrape = findElement(
        crimedataset, 'f. Statutory Rape', 'g. Robbery', 3)
    robbery = findElement(crimedataset, 'g. Robbery',
                          'h. Aggravated assault', 3)
    aggravatedassault = findElement(
        crimedataset, 'h. Aggravated assault', 'i. Burglary', 3)
    burglary = findElement(
        crimedataset, 'i. Burglary', 'j. Motor vehicle theft', 3)
    cartheft = findElement(
        crimedataset, 'j. Motor vehicle theft', 'k. Arson', 3)
    arson = findElement(
        crimedataset, 'k. Arson', 'VAWA Offenses', 3)
    domesticviolence = findElement(
        crimedataset, 'a. Domestic violence', 'b. Dating violence', 3)
    datingviolence = findElement(
        crimedataset, 'b. Dating violence', 'c. Stalking', 3)
    stalking = findElement(crimedataset, 'c. Stalking', 'Arrests', 3)
    weaponarrests = findElement(
        crimedataset, 'a. Weapons: carrying, possessing, etc.', 'b. Drug abuse violations', 3)
    drugarrests = findElement(
        crimedataset, 'b. Drug abuse violations', 'c. Liquor law violations', 3)
    liquorarrests = findElement(
        crimedataset, 'c. Liquor law violations', 'Disciplinary Actions', 3)
    weaponsdisciplinaryactions = findElement(
        crimedataset, 'Disciplinary Actions', 'b. Drug abuse violations', 7)
    drugsdisciplinaryactions = findElement(
        crimedataset, 'Disciplinary Actions', 'c. Liquor law violations', 11)
    liquordisciplinaryactions = findAfterString(
        crimedataset, 'c. Liquor law violations', 3, True)

    #-----------------------------Programs--------------------------------------------#
    programslist = "//table[@class='pmtabular']/tbody/tr[@class='subrow nb']"
    #----------------------------------------------------------------------------------------------#

    csvinfo = [college, address, phonenum, website, type,
               awardsoffered, campussetting, campushousing, studentpop, studenttofaculty, missionstatement, array_toString(
                   classification), array_toString(slo), array_toString(religion), array_toString(creditsaccepted), ftfaculty, ptfaculty,
               gradassistants, tuition, booksandsupplies, roomandboard, totalexpenses, instatetuition, outofstatetuition, g_instatetuition, g_outofstatetuition, avgtuition, avg_aid, maledemographic, femaledemographic, ethnic1, ethnic2, ethnic3, ethnic4, ethnic5, ethnic6, ethnic7,
               ethnic8, ethnic9, underage, overage, instateresidence, outofstateresidence, foreigncountriesresidence, fulltimegraduate, parttimegraduate, u_remotelearning, u_inpersonlearning, g_remotelearning, g_inpersonlearning, applicationfee, totalapplicants,
               percentadmitted, admittedandenrolled, secondaryschoolgpa, secondaryschoolrank, secondarschoolrecord, collegeprepprogram, recommendations, admissiontestscores, toefl, submittingsat, submittingact, sat_en_lowpercentile, sat_en_highpercentile,
               sat_math_lowpercentile, sat_math_highpercentile, act_composite_lowpercentile, act_composite_highpercentile, act_english_lowpercentile, act_english_highpercentile, act_math_lowpercentile, act_math_highpercentile, retentionrate, graduationrate,
               transferrate, gradratemale, gradratefemale, gradrateindiannative, gradrateasian, gradrateblack, gradratehispanic, gradratehawaiian, gradratewhite, gradratetwoormore, gradrateunknown, gradratealien,
               murders, manslaughter, rape, fondling, incest, statutoryrape, robbery, aggravatedassault, burglary, cartheft, arson, domesticviolence, datingviolence, stalking, weaponarrests, drugarrests, liquorarrests, weaponsdisciplinaryactions,
               drugsdisciplinaryactions, liquordisciplinaryactions]

    for i in range(len(csvinfo)):
        if csvinfo[i] == False or csvinfo[i] == '' or csvinfo[i] == '�':
            csvinfo[i] = 'n/a'

    writer.writerow(csvinfo)

    # Clean up
    file.close()
    # driver.quit()
    return True


def main():
    navigateToSite()
    driver.quit()


main()
