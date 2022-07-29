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


def findElement(element: list, before: str, after: str, index: int):
    """Finds the requested element within a list of elements given an index

    Args:
        element (list): list of elements (dataset)
        before (str): string before the element
        after (str): string after the element
        index (int): index of the element to be found
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
        if element[i] == start:
            found = True
            array = []
            array.append(element[i])
        elif element[i] == end:
            if found == True:
                break
        else:
            array.append(element[i])
    return array


def elementSplit(element: str, condition1: str, condition2: str, condition3: str):
    """Splits the element based on condition1, condition2 and condition3, returns false if none of the conditions are met

    Args:
        element (str): WebElement str
        condition1 (str): a condition to split the text by
        condition2 (str): a condition to split the text by
    """
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


# ----------------------------------------------------------------------------------------------------------------------
def scrapper(college: str):
    """Goes to the CollegeNavigator from the National Center for Education Statistics website and scrapes the data for each college in the list (listOfColleges.txt) and writes it to a csv file(collegeinfo.csv)

    Args:
        college (str): The college to be scraped

    Returns:
        bool: Returns True if the college was successfully scraped
    """
    driver = webdriver.Chrome()
    driver.get("https://nces.ed.gov/collegenavigator/")

    file = open('collegeInfo.csv', 'w')
    writer = csv.writer(file)

    # Write header rows
    writer.writerow(['College Name', 'Phone#', 'Website', 'Type', 'Degrees', 'Campus Type', 'Campus Housing',
                    'Student Pop', 'StudentsToTeachers', 'Classification', 'SLOs', 'Religious Affiliation',  'Credits Accepted', 'Faculty(full-time)', 'Faculty(part-time)', 'Graduate Assistants', 'Tuition', 'Books/Supplies', 'Room/Board',
                     'Total Expenses', 'Avg Tuition', 'Avg Aid(grants)', 'Gender Demographic(Male)', 'Gender Demographic(Female)', 'Ethnic Demographic (American Indian or Alaska Native)', 'Ethnic Demographic (Asian)', 'Ethnic Demographic(Black or African American)',
                     'Ethnic Demographic(Hispanic/Latino)', 'Ethnic Demographic(Native Hawaiian or other Pacific Islander)', 'Ethnic Demographic(White)', 'Ethnic Demographic(Two or more races)', 'Ethnic Demographic(Unknown)',
                     'Ethnic Demographic(Non-resident alien)', 'Avg Student Age (24 and Under)', 'Avg Student Age(25 and Over)', 'Avg Student Residence (In-State)', 'Avg Student Residence(Out-of-State)', 'Avg Student Residence(Foreign Countries)',
                     'Graduate Attendance Status(Full-time)', 'Graduate Attendance Status(Part-time)', 'Undergraduate Education Status (Remote)', 'Undergraduate Education Status (In-Person)', 'Graduate Education Status (Remote)', 'Graduate Education Status (In-Person)',
                     'Application Fee', 'Total Applicants', 'Percent Admitted', 'Percent Admitted Enrolled', 'Secondary School GPA', 'Secondary School Rank', 'Secondary School Record', 'Completion of College-Prep Program', 'Recommendation', 'SAT/ACT', 'TOEFL',
                     'Students Submitting Scores (SAT)',
                     'Students Submitting Scores (ACT)', 'SAT English 25th Percentile', 'SAT English 75th Percentile', 'SAT Math 25th percentile', 'SAT Math 75th Percentile', 'ACT Composite 25th Percentile', 'ACT Composite 75th Percentile', 'ACT English 25th Percentile',
                     'ACT English 75th Percentile', 'ACT Math 25th Percentile', 'ACT Math 75th Percentile', 'First-to-Second Year Retention Rate', 'Graduation Rate', 'Transfer Rate', 'Graduation Rate (Male)', 'Graduation Rate (Female)',
                     'Graduation Rate by Race/Ethnicity(American Indian or Alaska Native)', 'Graduation Rate by Race/Ethnicity(Asian)', 'Graduation Rate by Race/Ethnicity(Black or African American)', 'Graduation Rate by Race/Ethnicity(Hispanic/Latino)',
                     'Graduation Rate by Race/Ethnicity(Native Hawaiian or other Pacific Islander)', 'Graduation Rate by Race/Ethnicity(White)', 'Graduation Rate by Race/Ethnicity(Two or more Races)', 'Graduation Rate by Race/Ethnicity(Race/Ethnicity Unknown)',
                     'Graduation Rate by Race/Ethnicity(Non-resident Alien)', 'Area,Ethnic,Cultural,Gender, and Group Studies',
                     'Biological and Biomedical Sciences', 'Computer and Information Sciences and Support Services', 'Education', 'English Languages, Literatures, and Linguistics', 'Foreign Languages, Literatures and Linguistics', 'History', 'Liberal Arts and Sciences, General Studies and Humanities',
                     'Mathematics and Statistics', 'Multi/Interdisciplinary Studies', 'Natural Resources and Conservation', 'Philosophy and Religious Studies', 'Physical Sciences', 'Psychology', 'Social Sciences', 'Visual and Performing Arts',
                     'Murder/Non-negligent Manslaughter', 'Negligent Manslaughter', 'Rape', 'Fondling', 'Incest', 'Statutory Rape', 'Aggravated Assault', 'Burglary', 'Motor Vehicle Theft', 'Arson', 'Domestic Violence', 'Dating Violence', 'Stalking', 'Weapons Arrests',
                     'Drug Abuse Arrests', 'Liquor Law Violation Arrests', 'Weapons Disciplinary Action', 'Drug Abuse Disciplinary Action', 'Liquor Law Violation Disciplinary Action'])

    # Inputs each college from a list of colleges and goes to their respective pages
    collegeinput = driver.find_element(
        "xpath", "//input[@name='ctl00$cphCollegeNavBody$ucSearchMain$txtName']")
    collegeinput.send_keys(college)
    driver.find_element(
        'xpath', "//input[@name='ctl00$cphCollegeNavBody$ucSearchMain$btnSearch']").click()
    driver.find_element('xpath', '//a[strong]').click()
    driver.find_element(
        'xpath', '// a[@onclick="dall(true);return(false);"]').click()

    # Datasets -----------------------------------------------------------------------------------
    generalinfo = driver.find_element(
        'xpath', '//div[@id="ctl00_cphCollegeNavBody_ucInstitutionMain_divNPC"]').text
    tuitiondataset = elementToList(driver.find_elements(
        'xpath', '//div[@class="tabconstraint"]//table/tbody/tr/td'))
    admissiondataset = elementToList(driver.find_elements(
        'xpath', '//div[@id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04"]/div/table/tbody/tr/td'))
    graphdataset = driver.find_elements(
        'xpath', '//table[@class="graphtabs"]/tbody/tr/td/img')
    majorsdataset = elementToList(driver.find_elements(
        'xpath', '//tr[@class="pmsubtotal odd"]/td'))
    crimedataset = elementToList(driver.find_elements(
        'xpath', '//div[@id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl11"]/div/table/tbody/tr/td'))

    # --------------------------------------------------Data----------------------------------------------------------------
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
    maledemographic = elementSplit(
        graphdataset[1].get_attribute('alt'), ':\n', ': ', '\n')[-3]
    femaledemographic = elementSplit(
        graphdataset[1].get_attribute('alt'), ':\n', ': ', '\n')[-1]
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
    #--------------------------------------Student Avg Residence--------------------------------------------------------#
    instateresidence = elementSplit(
        graphdataset[4].get_attribute('alt'), ':\n', ': ', '\n')[2]
    outofstateresidence = elementSplit(
        graphdataset[4].get_attribute('alt'), ':\n', ': ', '\n')[4]
    foreigncountriesresidence = elementSplit(
        graphdataset[4].get_attribute('alt'), ':\n', ': ', '\n')[6]
    #--------------------------------------Graduate Attendance Status--------------------------------------------------------#
    fulltimegraduate = elementSplit(
        graphdataset[5].get_attribute('alt'), ':\n', ': ', '\n')[2]
    parttimegraduate = elementSplit(
        graphdataset[5].get_attribute('alt'), ':\n', ': ', '\n')[4]
    #--------------------------------------Undergraduate Remote Status--------------------------------------------------------#
    u_remotelearning = stataddition(
        elementSplit(graphdataset[6].get_attribute(
            'alt'), ':\n', ': ', '\n')[2],
        elementSplit(graphdataset[6].get_attribute('alt'), ':\n', ': ', '\n')[4])
    u_inpersonlearning = elementSplit(
        graphdataset[6].get_attribute('alt'), ':\n', ': ', '\n')[6]
    #--------------------------------------Graduate Remote Status--------------------------------------------------------#
    g_remotelearning = stataddition(
        elementSplit(graphdataset[7].get_attribute(
            'alt'), ':\n', ': ', '\n')[2],
        elementSplit(graphdataset[7].get_attribute('alt'), ':\n', ': ', '\n')[4])
    g_inpersonlearning = elementSplit(
        graphdataset[7].get_attribute('alt'), ':\n', ': ', '\n')[6]
    #----------------------------------------------------------------------------------------------#
    applicationfee = elementSplit(driver.find_element(
        'xpath', '//div[@id="divctl00_cphCollegeNavBody_ucInstitutionMain_ctl04"]/div/table/tbody/tr').text, ': ', None, None)[1]
    totalapplicants = findElement(
        admissiondataset, 'Number of applicants', 'Percent admitted', 1)
    percentadmitted = findElement(
        admissiondataset, 'Percent admitted', 'Percent admitted who enrolled', 1)
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
    submittingsat = findElement(admissiondataset, 'SAT', 'ACT', 2)
    submittingact = findElement(admissiondataset, 'ACT',
                                'SAT Evidence-Based Reading and Writing', 2)
    sat_en_lowpercentile = findElement(
        admissiondataset, 'SAT Evidence-Based Reading and Writing', 'SAT Math', 1)
    sat_en_highpercentile = findElement(
        admissiondataset, 'SAT Evidence-Based Reading and Writing', 'SAT Math', 2)
    sat_math_lowpercentile = findElement(
        admissiondataset, 'SAT Math', 'ACT Composite', 1)
    sat_math_highpercentile = findElement(
        admissiondataset, 'SAT Math', 'ACT Composite', 2)
    act_composite_lowpercentile = findElement(
        admissiondataset, 'ACT Composite', 'ACT English', 1)
    act_composite_highpercentile = findElement(
        admissiondataset, 'ACT Composite', 'ACT English', 2)
    act_english_lowpercentile = findElement(
        admissiondataset, 'ACT English', 'ACT Math', 1)
    act_english_highpercentile = findElement(
        admissiondataset, 'ACT English', 'ACT Math', 2)
    act_math_lowpercentile = findElement(
        admissiondataset, 'ACT Math', '', 1)
    act_math_highpercentile = findElement(
        admissiondataset, 'ACT Math', '', 2)
    #----------------------------------------------------------------------------------------------#
    retentionrate = elementSplit(
        graphdataset[8].get_attribute('alt'), ':\n', ': ', '\n')[2]
    graduationrate = elementSplit(
        graphdataset[9].get_attribute('alt'), ':\n', ': ', '\n')[2]
    transferrate = elementSplit(
        graphdataset[9].get_attribute('alt'), ':\n', ': ', '\n')[4]
    gradratemale = elementSplit(
        graphdataset[11].get_attribute('alt'), ':\n', ': ', '\n')[2]
    gradratefemale = elementSplit(
        graphdataset[11].get_attribute('alt'), ':\n', ': ', '\n')[4]
    gradrateindiannative = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[2]
    gradrateasian = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[4]
    gradrateblack = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[6]
    gradratehispanic = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[8]
    # TODO: Account for the fact that the graphs will sometimes not include naive hawaiian data
    if (elementSplit(graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[10] == 'White'):
        gradratehawaiian = 'n/a'
    else:
        gradratehawaiian = elementSplit(
            graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[10]
    gradratewhite = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[12]
    gradratetwoormore = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[14]
    gradrateunknown = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[16]
    gradratealien = elementSplit(
        graphdataset[12].get_attribute('alt'), ':\n', ': ', '\n')[18]
    #-----------------------------Programs--------------------------------------------#
    culturalstudies = (majorsdataset)[1]
    biostudies = (majorsdataset)[4]
    csstuidies = (majorsdataset)[7]
    educationstudies = (majorsdataset)[10]
    englishstudies = (majorsdataset)[13]
    foreignlanguagestudies = (majorsdataset)[16]
    historystudies = (majorsdataset)[19]
    humanitiesstudies = (majorsdataset)[22]
    mathstudies = (majorsdataset)[25]
    interdisciplinarystudies = (majorsdataset)[28]
    conservationstudies = (majorsdataset)[31]
    philosphystudies = (majorsdataset)[34]
    physicalsciencestudies = (majorsdataset)[37]
    psychologystudies = (majorsdataset)[40]
    socialsciencesstudies = (majorsdataset)[43]
    visualartsstudies = (majorsdataset)[46]
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
    liquordisciplinaryactions = findElement(
        crimedataset, 'Disciplinary Actions', 'Criminal Offenses', 15)

    # TODO
    writer.writerow([college, '999-999-9999', 'tobeimplemented.com', '4-year',
                    "Bachelor's Degree , Master's degree", 'Town: Distant', 'Yes', '3421', '9 to 1', missionstatement.text, array_toString(
                        classification), array_toString(slo), array_toString(religion), array_toString(creditsaccepted), ftfaculty, ptfaculty,
                     gradassistants, tuition, booksandsupplies, roomandboard, totalexpenses, avgtuition, avg_aid, maledemographic, femaledemographic, ethnic1, ethnic2, ethnic3, ethnic4, ethnic5, ethnic6, ethnic7,
                     ethnic8, ethnic9, underage, overage, instateresidence, outofstateresidence, foreigncountriesresidence, fulltimegraduate, parttimegraduate, u_remotelearning, u_inpersonlearning, g_remotelearning, g_inpersonlearning, applicationfee, totalapplicants,
                     percentadmitted, admittedandenrolled, secondaryschoolgpa, secondaryschoolrank, secondarschoolrecord, collegeprepprogram, recommendations, admissiontestscores, toefl, submittingsat, submittingact, sat_en_lowpercentile, sat_en_highpercentile,
                     sat_math_lowpercentile, sat_math_highpercentile, act_composite_lowpercentile, act_composite_highpercentile, act_english_lowpercentile, act_english_highpercentile, act_math_lowpercentile, act_math_highpercentile, retentionrate, graduationrate,
                     transferrate, gradratemale, gradratefemale, gradrateindiannative, gradrateasian, gradrateblack, gradratehispanic, gradratehawaiian, gradratewhite, gradratetwoormore, gradrateunknown, gradratealien, culturalstudies, biostudies, csstuidies,
                     educationstudies, englishstudies, foreignlanguagestudies, historystudies, humanitiesstudies, mathstudies, interdisciplinarystudies, conservationstudies, philosphystudies, physicalsciencestudies, psychologystudies, socialsciencesstudies,
                     visualartsstudies, murders, manslaughter, rape, fondling, incest, statutoryrape, aggravatedassault, burglary, cartheft, arson, domesticviolence, datingviolence, stalking, weaponarrests, drugarrests, liquorarrests, weaponsdisciplinaryactions,
                     drugsdisciplinaryactions, liquordisciplinaryactions])

    # Testing

    # Clean up
    file.close()
    driver.quit()
    return True


collegelist = open('testListColleges.txt', 'r')


while True:
    college = collegelist.readline()
    if not college:

        break
    scrapper(college)

collegelist.close()
