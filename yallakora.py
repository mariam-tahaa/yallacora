import requests
from bs4 import BeautifulSoup
import csv

#call our page to extract information
date = input("Please enter a Date with following format MM/DD/YYYY: ")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#days")

#our main function 
def main(page):
    #return page content as byte code
    src = page.content
    match_details = []
    #extract HTML code of our page using lxml parser
    #convert byte code into HTML code
    soup = BeautifulSoup(src, "lxml")
    #use filter to trace all divs of championships
    #number of champions
    championships = soup.find_all("div", {'class': 'matchCard'})
    #print(championships)

    #function to extract names of championships 
    def champion_titles(championships):
        #find names of championships
        title = championships.contents[1].find("h2").text.strip()
        #print(title)
        #find number of matches in each championship
        all_matches = championships.contents[3].find_all("div", class_= ['item future liItem', 'item now liItem', 'item finish liItem'])
        #print(all_matches)
        num_of_matches = len(all_matches)
        #print(num_of_matches)

        #get datails of every match in the champion
        for i in range(num_of_matches):
            #teams names
            teamA =  all_matches[i].find("div", {'class': 'teams teamA'}).text.strip()
            teamB =  all_matches[i].find("div", {'class': 'teams teamB'}).text.strip()
            #print(teamA)

            #teams score
            result = all_matches[i].find("div", {'class':'MResult'}).find_all("span", {'class':'score'})
            score = f"'{result[0].text.strip()} - {result[1].text.strip()}'"
            #score = result[0]+' - '+result[4]
            #print(score)

            #time of the match
            match_time = all_matches[i].find("span", {'class':'time'}).text.strip()
            #print(match_time)

            #add match info to list of match_details
            match_details.append({"اسم البطولة":title, 'الفريق الاول':teamA, 'الفريق الثاني':teamB, 
                              'ميعاد المباراه':match_time, 'نتيجة المباراه':score})

    for i in range (len(championships)):
        champion_titles(championships[i])

    #**********create csv file***********
    #detect headers of file
    try:
        keys = match_details[0].keys()

        with open("D:\Data_Analysis\web_scarping\yallacora\yallacora.csv", 'w', newline='') as output:
            dict_writer = csv.DictWriter(output, keys)
            dict_writer.writeheader()
            dict_writer.writerows(match_details)
            print("File Created")
    except:
        print("No such data found")
    
main(page)