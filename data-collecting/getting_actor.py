import urllib
from bs4 import BeautifulSoup

filename = 'notabled_actors.csv'
outputFile = open(filename, 'w')
outputFile.write('name,url,gender,role,event\n')

wikiRoot = 'http://en.wikipedia.org'
awardPageActors = wikiRoot + '/wiki/Screen_Actors_Guild_Award'
awardSoupActors = BeautifulSoup(urllib.request.urlopen(awardPageActors))

winners_For_YearsHeader = awardSoupActors.find('span', {'id': 'List_of_nominees_and_winners'}).parent
winners_For_Years = winners_For_YearsHeader.find_next_sibling('ul')
winners_For_YearsATags = winners_For_Years.find_all('a')
winners_For_YearsURLs = []
for item in winners_For_YearsATags:
    if item.has_attr('href'):
        winners_For_YearsURLs.append(wikiRoot + item['href'])

for winners_For_AYearPage in winners_For_YearsURLs:

    winners_For_AYearSoup = BeautifulSoup(urllib.request.urlopen(winners_For_AYearPage))
    winners_For_AYearTitle = winners_For_AYearSoup.title.contents[0]
    winners_For_AYearTitle = winners_For_AYearTitle.replace(' - Wikipedia, the free encyclopedia', '')
    filmwinners_For_AYearTable = winners_For_AYearSoup.find('table', {'class': 'wikitable'})

    if filmwinners_For_AYearTable is not None:
        filmwinners_For_AYearRows = filmwinners_For_AYearTable.find_all('tr')
        columnsLeadActors = filmwinners_For_AYearRows[1].find_all('td')
        aTagleadMaleActor = columnsLeadActors[0].find_next('a')
        leadFemaleActorATag = columnsLeadActors[1].find_next('a')
        supportActorsColumns = filmwinners_For_AYearRows[3].find_all('td')
        supportMaleActorATag = supportActorsColumns[0].find_next('a')
        supportFemaleActorATag = supportActorsColumns[1].find_next('a')

    else:
        leadMaleActorHeader = winners_For_AYearSoup.find('span', {
            'id': 'Outstanding_Performance_by_a_Male_Actor_in_a_Leading_Role'})
        leadFemaleActorHeader = winners_For_AYearSoup.find('span', {
            'id': 'Outstanding_Performance_by_a_Female_Actor_in_a_Leading_Role'})
        supportMaleActorHeader = winners_For_AYearSoup.find('span', {
            'id': 'Outstanding_Performance_by_a_Male_Actor_in_a_Supporting_Role'})
        supportFemaleActorHeader = winners_For_AYearSoup.find('span', {
            'id': 'Outstanding_Performance_by_a_Female_Actor_in_a_Supporting_Role'})

        aTagleadMaleActor = leadMaleActorHeader.find_next('b').find_next('a')
        leadFemaleActorATag = leadFemaleActorHeader.find_next('b').find_next('a')
        supportMaleActorATag = supportMaleActorHeader.find_next('b').find_next('a')
        supportFemaleActorATag = supportFemaleActorHeader.find_next('b').find_next('a')

    leadMaleActor = aTagleadMaleActor['title'].replace('\'', '').replace(',', '').replace('.', '')
    leadMaleActorURL = wikiRoot + aTagleadMaleActor['href'].replace(',', '')
    outputFile.write(
        '\'' + leadMaleActor + '\'' + ',' + leadMaleActorURL + ',male,lead,' + '\'' + winners_For_AYearTitle + '\'' + '\n')

    leadFemaleActor = leadFemaleActorATag['title'].replace('\'', '').replace(',', '').replace('.', '')
    leadFemaleActorURL = wikiRoot + leadFemaleActorATag['href'].replace(',', '')
    outputFile.write(
        '\'' + leadFemaleActor + '\'' + ',' + leadFemaleActorURL + ',female,lead,' + '\'' + winners_For_AYearTitle + '\'' + '\n')

    supportMaleActor = supportMaleActorATag['title'].replace('\'', '').replace(',', '').replace('.', '')
    supportMaleActorURL = wikiRoot + supportMaleActorATag['href'].replace(',', '')
    outputFile.write(
        '\'' + supportMaleActor + '\'' + ',' + supportMaleActorURL + ',male,support,' + '\'' + winners_For_AYearTitle + '\'' + '\n')

    supportFemaleActor = supportFemaleActorATag['title'].replace('\'', '').replace(',', '').replace('.', '')
    supportFemaleActorURL = wikiRoot + supportFemaleActorATag['href'].replace(',', '')
    outputFile.write(
        '\'' + supportFemaleActor + '\'' + ',' + supportFemaleActorURL + ',female,support,' + '\'' + winners_For_AYearTitle + '\'' + '\n')

outputFile.close()
