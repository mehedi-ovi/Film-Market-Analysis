import urllib
from bs4 import BeautifulSoup


def filmIndexParse(startURL_data):
    FilmsURLsList = []
    FilmsURLsList.append(startURL_data)
    FilmsSoupList = BeautifulSoup(urllib.request.urlopen(startURL_data))
    filmTableIndex = FilmsSoupList.find('table', {'class': 'wikitable'})
    filmTableRowsIndex = filmTableIndex.findAll('tr')
    for filmTableRowIndex in filmTableRowsIndex:
        filmTableColsIndex = filmTableRowIndex.findAll('td')
        for filmTableColIndex in filmTableColsIndex:
            filmTableColATagIndex = filmTableColIndex.find('a')
            if filmTableColATagIndex:
                filmHrefIndex = filmTableColIndex.find('a').get('href')
                if FilmedPathList in filmHrefIndex:
                    FilmsURLsList.append(wikiRoot + filmHrefIndex)
    return FilmsURLsList


def allFilmPagesParse(FilmsURLsList):
    filmsDataURL = {}

    for FilmsURLlist in FilmsURLsList:
        FilmsSoupList = BeautifulSoup(urllib.request.urlopen(FilmsURLlist))
        listOfITagsFilms = FilmsSoupList.findAll('i')
        for listOfITagsFilms in listOfITagsFilms:
            if listOfITagsFilms.a:
                filmsData = iTagParsing(listOfITagsFilms)
                filmsDataURL[filmsData['url']] = filmsData
    return filmsDataURL


def iTagParsing(iTag):
    listOfITagsFilms = iTag
    title_of_film = listOfITagsFilms.a.get('title')
    title_of_film = title_of_film.replace(',', '').replace('\'', '').replace('"', '')
    filmsYear = ''
    iTagOFParentContents = listOfITagsFilms.parent.contents
    if len(iTagOFParentContents) > 1:
        filmsYear = iTagOFParentContents[1]
        filmsYear = ''.join(filter(lambda char: char.isdigit(), filmsYear))
    if not filmsYear and len(iTagOFParentContents) > 2:
        filmsYear = iTagOFParentContents[2].contents[0]
        filmsYear = ''.join(filter(lambda char: char.isdigit(), filmsYear))
    if not filmsYear:
        filmsYear = 'null'
    URL_Of_Film = wikiRoot + listOfITagsFilms.a.get('href')
    URL_Of_Film = URL_Of_Film.replace(',', '')
    filmsData = {'url': URL_Of_Film, 'title': title_of_film, 'year': filmsYear}
    return filmsData


if __name__ == "__main__":

    filename = './data/URL_Of_Films.csv'
    outputFile = open(filename, 'w')
    outputFile.write('url,title,year\n')
    wikiRoot = 'http://en.wikipedia.org'
    FilmedPathList = '/wiki/List_of_films:'
    startListOfFilmsHref = FilmedPathList + '_numbers'
    startFilmsURLlist = wikiRoot + startListOfFilmsHref
    FilmsURLsList = filmIndexParse(startFilmsURLlist)
    filmsDataURL = allFilmPagesParse(FilmsURLsList)

    for URL_Of_Film, filmsData in filmsDataURL.items():
        title_of_film = filmsData['title']
        filmsYear = filmsData['year']
        outputFile.write(URL_Of_Film + ',' + '\'' + title_of_film + '\'' + ',' + filmsYear + '\n')

    outputFile.close()
