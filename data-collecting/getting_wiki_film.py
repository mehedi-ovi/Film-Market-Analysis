# description: Pull important data from Wikipedia film pages stored locally.
# authors: Paul Prae, Daniel Joensen
# since: 3/08/2015
# tested with Python 3.3 on CentOS 7 and Windows 8
# TODO: Create reducer function
# TODO: Add in command line parameters
# --mapper	turns this into a script that acts as just the mapper function.
# --reducer	turns this into a script that acts as just the reducer function.
# --stdio	uses STDIN as the input and STDOUT as the output for the map reduce functions. may need to always assume this if a map or reduce flag is present this is true.
# otherwise run this locally with a loop over a list of directory names.

import os
import sys
import re
from bs4 import BeautifulSoup
import wikipedia
import csv
import ntpath
# custom
import wiki_feature_extractors


def tuples_to_column_value(notableData):
    pipesAndTuples = "";
    for notableTuple in notableData:
        notableName = notableTuple['name'];
        notableURL = notableTuple['url'];
        pipesAndTuples += notableName + ';' + notableURL + '|';
    # Removing last pipe
    finalValue = pipesAndTuples[:-1]
    if not finalValue:
        finalValue = 'null';
    return finalValue;


def list_to_column_value(dataList):
    columnValue = "";
    for item in dataList:
        columnValue += item + '|';
    columnValue = columnValue[:-1];
    if not columnValue:
        columnValue = 'null';
    return columnValue;


def build_film_index():
    filmIndex = {};
    filmFilename = './data/URL_Of_Films.csv';
    filmReader = csv.reader(open(filmFilename, encoding="utf8"));
    filmReader.__next__();
    count = 0;
    for filmsData in filmReader:
        count += 1;
        filmIndex[filmsData[0]] = {'title': filmsData[1], 'year': filmsData[2]};
    return filmIndex;


def mapper(fullFilmFilePath, filmIndex, stdIO):
    try:
        filmPage = open(fullFilmFilePath, encoding="utf8");
    except IsADirectoryError:
        return "";
    filmPageSoup = BeautifulSoup(filmPage.read());
    filmFileName = ntpath.basename(fullFilmFilePath);
    URL_Of_FilmName = os.path.splitext(filmFileName)[0];
    URL_Of_Film = 'http://en.wikipedia.org/wiki/' + URL_Of_FilmName;

    filmDate = wiki_feature_extractors.find_date_of_release(filmPageSoup);

    budgetValue = wiki_feature_extractors.find_budget(filmPageSoup);
    if not budgetValue:
        budgetValue = 'null';
    budgetValue = budgetValue.replace(',', '');

    revenueValue = wiki_feature_extractors.find_revenue(filmPageSoup);

    directorData = wiki_feature_extractors.find_director(filmPageSoup);
    directorValue = tuples_to_column_value(directorData);

    actorData = wiki_feature_extractors.find_actor(filmPageSoup);
    actorValue = tuples_to_column_value(actorData);

    distributionData = wiki_feature_extractors.find_distribution_company(filmPageSoup);
    distributionValue = tuples_to_column_value(distributionData);

    genreData = wiki_feature_extractors.find_genre(filmPageSoup);
    genreValue = list_to_column_value(genreData);

    try:
        filmsData = filmIndex.get(URL_Of_Film);
        if filmsData:
            title_of_film = filmsData.get('title');
            if not title_of_film:
                title_of_film = URL_Of_FilmName;
            filmsYear = filmsData.get('year');
            # TODO: filmsYear still ends up blank sometimes. whitespace?
            if not filmsYear:
                filmsYear = 'null';
        else:
            title_of_film = 'null';
            filmsYear = 'null';
        return [title_of_film, URL_Of_Film, filmDate, filmsYear, budgetValue, revenueValue, directorValue, actorValue,
                distributionValue, genreValue];
    except KeyError:
        return "";


def loopLocal(stdIO, inputDirectory, outputFile):
    filmWriter = csv.writer(open(outputFile, 'w', newline=''));
    filmIndex = build_film_index();
    filmWriter.writerow(
        ['title', 'url', 'release date', 'release year', 'budget', 'revenue', 'director', 'actor', 'distributor',
         'genre']);

    filmFiles = os.listdir(inputDirectory);
    count = 0;
    for filmFileName in filmFiles:
        count += 1;
        print(str(count) + ' - ' + filmFileName);
        fullFilmFilePath = inputDirectory + filmFileName;
        filmRow = mapper(fullFilmFilePath, filmIndex, stdIO);
        filmWriter.writerow(filmRow);


if __name__ == "__main__":

    # assume we are not in stdIO mode
    stdIO = False;

    if not stdIO:
        inputDirectory = './data/films/test/';
        outputFile = './data/test_film_data.csv';
        loopLocal(stdIO, inputDirectory, outputFile);
