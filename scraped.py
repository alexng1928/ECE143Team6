from bs4 import BeautifulSoup
from requests import get
from collections import defaultdict
from sets import Set

dirtyDupedUnpairedCourseNameList = []  # list of only courseNames with dupes and no pairs
dirtyUnpairedCourseNameSet = []  # list of only courseNames with no dupes but no pairs
dirtyUnpairedCourseNameHash = {}  # boolean hash of courseNames 
scrapeCleanedUnpairedRows = []  # all rows of department without pairs
UnpairedRowsWithSeparateChainingDict = defaultdict(list)  # hash to pair the above
cleanedDepartmentalCourseList = []  # list of tuples with guaranteed summer and non-summer pairs

url = 'https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=cse'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = get(url, headers=headers)
html_soup = BeautifulSoup(response.text, 'html.parser')
table = html_soup.find('table')
table_body = table.find('tbody')
rows = table_body.find_all('tr')

 
def setLink(link):
    resetAllLists()
    global url 
    url = link
    global response 
    response = get(url, headers=headers)
    global html_soup 
    html_soup = BeautifulSoup(response.text, 'html.parser')
    global table 
    table = html_soup.find('table')
    global table_body
    table_body = table.find('tbody')
    global rows 
    rows = table_body.find_all('tr')


def convertHtmlToString(tag):
    readable = tag.text.strip().encode("utf-8") 
    if readable[-1] == '%':
        return readable[0:len(readable) - 2]
    return readable


def scrapeNameList(dirtyList):
    for row in rows:
        rowArray = row.find_all('td')
        if (convertHtmlToString(rowArray[2])[0:2] == 'S1' or convertHtmlToString(rowArray[2])[0:2] == 'S2' or convertHtmlToString(rowArray[2])[0:2] == 'S3' or convertHtmlToString(rowArray[2])[0:2] == 'SU') and convertHtmlToString(rowArray[1])[0:2] != 'No' :
            year = row.find_all('td')[1].text.strip().encode("utf-8")
            year = year.replace(" ", "")
            year = year.replace(",", "")
            year = year[0:len(year) - 3]
            dirtyList.append(year)  # Get rid of empty values\



def createSetList(duped):
    unduped = list(Set(duped))
    unduped.sort()
    return unduped


def booleanHashCourseName(courseNameSet):
    for i in courseNameSet:
        dirtyUnpairedCourseNameHash[i] = 1

        
def scrapeCapeRows():
    for row in rows:
        rowList = row.find_all('td')
        courseName = rowList[1].text.strip().encode("utf-8")
        courseName = courseName.replace(" ", "")
        courseName = courseName.replace(",", "")
        courseName = courseName[0:len(courseName) - 3]
        expectedGPA = convertHtmlToString(rowList[8])
        receivedGPA = convertHtmlToString(rowList[9])
        if expectedGPA != 'N/A':
            expectedGPA = rowList[8].text.strip().encode("utf-8")[len(expectedGPA) - 5:len(expectedGPA) - 1]
        if receivedGPA != 'N/A':
            receivedGPA = rowList[9].text.strip().encode("utf-8")[len(receivedGPA) - 5:len(receivedGPA) - 1]

        if receivedGPA == 'N/A':
            continue
        if courseName in dirtyUnpairedCourseNameHash:
            if (int)(convertHtmlToString(rowList[2])[2:4]) >=11: #ADDED LINE TO FILTER OUT EARLIER YEARS
                if (convertHtmlToString(rowList[2])[0:2] == 'S1' or convertHtmlToString(rowList[2])[0:2] == 'S2' or convertHtmlToString(rowList[2])[0:2] == 'S3' or convertHtmlToString(rowList[2])[0:2] == 'SU'):       
                    scrapeCleanedUnpairedRows.append((courseName, 'S', convertHtmlToString(rowList[2]), convertHtmlToString(rowList[3]), convertHtmlToString(rowList[4]), convertHtmlToString(rowList[5]), convertHtmlToString(rowList[6]), convertHtmlToString(rowList[7]), expectedGPA, receivedGPA)) 
                else:
                    scrapeCleanedUnpairedRows.append((courseName, 'NS', convertHtmlToString(rowList[2]), convertHtmlToString(rowList[3]), convertHtmlToString(rowList[4]), convertHtmlToString(rowList[5]), convertHtmlToString(rowList[6]), convertHtmlToString(rowList[7]), expectedGPA, receivedGPA)) 


def initializeDefaultDict():
    for i in scrapeCleanedUnpairedRows:
        UnpairedRowsWithSeparateChainingDict[i[0]].append(i)


def pairDefaultDict():
    for course in UnpairedRowsWithSeparateChainingDict.keys():
        summerCount = 0
        nonsummerCount = 0
        for tupe in UnpairedRowsWithSeparateChainingDict[course]:
            if tupe[1] == 'S':
                summerCount += 1
            else:
                nonsummerCount += 1
                
        if summerCount == 0:
            del UnpairedRowsWithSeparateChainingDict[course]
        
        if nonsummerCount == 0:
            del UnpairedRowsWithSeparateChainingDict[course]

            
def getListFromDictionary():
    for course in UnpairedRowsWithSeparateChainingDict.keys():
        for tupe in UnpairedRowsWithSeparateChainingDict[course]:
            cleanedDepartmentalCourseList.append(tupe)
    cleanedDepartmentalCourseList.sort()


def returnTupleListToStringList(tupleList):
    stringList = []
    for tupe in tupleList:
        stringList.append("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (tupe[0], tupe[1], tupe[2], tupe[3], tupe[4], tupe[5], tupe[6], tupe[7], tupe[8], tupe[9]))
    return stringList


def prettyPrintList(listOfStrings):
    for i in listOfStrings:
        print i

        
def resetAllLists():
    global dirtyDupedUnpairedCourseNameList
    global dirtyUnpairedCourseNameSet
    global dirtyUnpairedCourseNameHash
    global scrapeCleanedUnpairedRows
    global UnpairedRowsWithSeparateChainingDict
    global cleanedDepartmentalCourseList
    dirtyDupedUnpairedCourseNameList = []
    dirtyUnpairedCourseNameSet = []
    dirtyUnpairedCourseNameHash = {}  # boolean hash
    scrapeCleanedUnpairedRows = []
    UnpairedRowsWithSeparateChainingDict = defaultdict(list)
    cleanedDepartmentalCourseList = []


def scrapeAndInitializeList(link):
    '''Takes in a url for a department and returns a list of one-line strings for the department'''
    setLink(link)            
    scrapeNameList(dirtyDupedUnpairedCourseNameList)
    dirtyUnpairedCourseNameSet = createSetList(dirtyDupedUnpairedCourseNameList)
    booleanHashCourseName(dirtyUnpairedCourseNameSet)
    scrapeCapeRows()  # initializes scrapeCleanedUnpairedRows
    initializeDefaultDict()
    pairDefaultDict()
    getListFromDictionary()
    if link.lower() == 'https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=se'.lower():
        SElist = [x for x in cleanedDepartmentalCourseList if x[0][0:2] == 'SE']
        return returnTupleListToStringList(SElist)
        return SElist
    return returnTupleListToStringList(cleanedDepartmentalCourseList)

# IMPORTANT: Each list is exactly named after a department and contains string elements that quote the entire row
# format: courseName, term, enroll#, evals made, recommend class%, recommend prof%, hrs/wk, GPA expected, GPA received 
# sry i kept row as an entire string and didn't break each row up into different data-type, leaving it to you 
# instead of individual departments, we could analyze 3 area studies (engineering, humanities, socialSciences)
# each area study list is a concatenation of the 5 most popular departments within that area study


CSE = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=cse')
ECE = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=ece')
MAE = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=mae')
SE = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=se')
NANO = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=nano')
engineering = CSE + ECE + MAE + SE + NANO
 
PHIL = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=phil')
HIEA = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=hiea')
MUS = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=mus')
TD = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=td')
VIS = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=vis')
humanities = PHIL + HIEA + MUS + TD + VIS
  
ECON = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=econ')
POLI = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=poli')
COGS = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=cogs')
PSYC = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=psyc')
MGT = scrapeAndInitializeList('https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber=mgt')
socialSciences = ECON + POLI + COGS + PSYC + MGT

ucsd= engineering+humanities+socialSciences

# print engineering and create txt file
engineeringFile = open('engineering.txt', 'wb')
for item in engineering:
    engineeringFile.write("%s\n" % item)
# prettyPrintList(engineering)

# print humanitiesFile and create txt file
humanitiesFile = open('humanities.txt', 'wb')
for item in humanities:
    humanitiesFile.write("%s\n" % item)
# prettyPrintList(humanities)

# print socialSciences and create txt file
socialSciencesFile = open('socialSciences.txt', 'wb')
for item in socialSciences:
    socialSciencesFile.write("%s\n" % item)
# prettyPrintList(socialSciences)

# print ucsd and create txt file
ucsdFile = open('ucsd.txt', 'wb')
for item in ucsd:
    ucsdFile.write("%s\n" % item)
#prettyPrintList(ucsd)



# prettyPrintList(CSE)
# prettyPrintList(HIEA)
#prettyPrintList(MGT)
