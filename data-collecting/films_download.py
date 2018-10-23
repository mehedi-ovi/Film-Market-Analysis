import csv
import requests

trackFile = open('C:/Users/Public/film_storage/tracking_progress.csv', 'w')
filmFilename = 'C:/Users/Public/bom_URL_Of_Films_data.csv';
filmReader = csv.reader(open(filmFilename, encoding="utf8"))
filmReader.__next__()
count = 0
for filmsData in filmReader:
    count += 1

    url = filmsData[0]
    urlPiece = url.split('=')
    pagesName = urlPiece[len(urlPiece) - 1]
    pagesFile = open('C:/Users/Public/film_storage/' + pagesName, 'w')
    try:
        response = requests.get(url)
        response = str(response).encode('ascii', 'ignore')
        response = response.decode('ascii', 'ignore').strip()
        print(str(count) + '. Writing ' + pagesName)
        pagesFile.write(response)
        trackFile.write(url + '\n')
    except requests.exceptions.RequestException:
        print('Exception: Bad Request for ' + pagesName + ' -> ' + url)
        pagesFile.close()
trackFile.close()