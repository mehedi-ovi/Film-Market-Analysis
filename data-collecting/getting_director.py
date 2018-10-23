from bs4 import BeautifulSoup
import urllib

filename = 'directors_list.csv'
outputFile = open(filename, 'w')
outputFile.write('director name,url\n')
wikiRoot = 'http://en.wikipedia.org'
directorsPage = wikiRoot + '/wiki/Film_director'
directorsSoup = BeautifulSoup(urllib.request.urlopen(directorsPage))
directorsList = directorsSoup.find('div', {'class': 'div-col columns column-count column-count-2'})
directorsListItems = directorsList.find_all('li')

for item in directorsListItems:
    directorATagName = item.find_next('a')
    Name_of_director = directorATagName['title'].replace('\'', '').replace(',', '').replace('.', '').replace('\u015b',                                                                                                      's').replace(
        '\u014d', 's').replace('\u0159', 'r')
    Name_of_director = Name_of_director.replace(' (director)', '').replace(' (filmmaker', '')
    URL_of_director = wikiRoot + directorATagName['href'].replace(',', '')
    outputFile.write('\'' + Name_of_director + '\'' + ',' + URL_of_director + '\'' + '\n')
    
outputFile.close()
