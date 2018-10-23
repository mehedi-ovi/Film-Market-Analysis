import urllib
import csv
from datetime import datetime
from bs4 import BeautifulSoup


# Finishing integrating the urls from excel file

def movie_name_finder(movie_data):
    tables_list = movie_data.find_all('table')
    targeted_table = tables_list[2]
    table_row = targeted_table.find_all('tr')
    targeted_row = table_row[0]
    targeted_columns = targeted_row.find_all('td', {'align': 'center'})
    targeted_column = targeted_columns[1]
    targeted_column = targeted_column.find('b')
    mov_title = targeted_column.text
    mov_title = mov_title.replace(',', '')
    return mov_title


def domestic_total_finder(movie_data):
    try:
        revenues_table = movie_data.find('div', {'class': 'mp_box_content'})
        revenues_table_row = revenues_table.find_all('tr')
        dom_total = 'null'
        for row in revenues_table_row:
            if 'Domestic' in row.text:
                dom_total = row.text
                dom_total = dom_total.split()[1]
                dom_total = dom_total.replace('$', '').replace(',', '')
    except (IndexError, AttributeError):
        dom_total = 'null'
    return dom_total


def find_total_foreign(movie_data):
    try:
        revenues_table = movie_data.find('div', {'class': 'mp_box_content'})
        revenues_table_row = revenues_table.find_all('tr')
        total_foreign = 'null'
        for row in revenues_table_row:
            if 'Foreign' in row.text:
                total_foreign = row.text
                total_foreign = total_foreign.split()[2]
                total_foreign = total_foreign.replace('$', '').replace(',', '')
    except (IndexError, AttributeError):
        total_foreign = 'null'
    return total_foreign


def find_total_global(movie_data):
    try:
        revenues_table = movie_data.find('div', {'class': 'mp_box_content'})
        revenues_table_row = revenues_table.find_all('tr')
        total_global = 'null'
        for row in revenues_table_row:
            if 'Worldwide' in row.text:
                total_global = row.text
                total_global = total_global.split()[2]
                total_global = total_global.replace('$', '').replace(',', '')
    except (IndexError, AttributeError):
        total_global = 'null'
    return total_global


def find_opening_weekend_totals(movie_data):
    try:
        revenues_table = movie_data.find_all('div', {'class': 'mp_box_content'})
        targeted_table = revenues_table[1]
        targeted_table_row = targeted_table.find_all('tr')
        opening_weekend_totals = 'null'
        for row in targeted_table_row:
            if 'Weekend' in row.text:
                if 'Limited' in row.text:
                    pass
                else:
                    final_row = row.text.split()
                    for item in final_row:
                        if '$' in item:
                            opening_weekend_totals = item
                            opening_weekend_totals = opening_weekend_totals.replace('$', '').replace(',', '')
    except (IndexError, AttributeError):
        opening_weekend_totals = 'null'
    return opening_weekend_totals

def find_theater_count(movie_data):
    try:
        revenues_table = movie_data.find_all('div', {'class': 'mp_box_content'})
        targeted_table = revenues_table[1]
        targeted_table_row = targeted_table.find_all('tr')
        theater_count = 'null'
        if len(targeted_table_row) == 0:
            theater_count = 'null'
        else:
            for row in targeted_table_row:
                if 'Widest' in row.text:
                    row_list = row.text.split()
                    theater_count = row_list[2]
                    theater_count = theater_count.replace(',', '')
    except (IndexError, AttributeError):
        theater_count = 'null'
    return theater_count

def find_film_mpaa_rating(movie_data):
    centerd_table = movie_data.findChildren('center')[0]
    centerd_table_data = centerd_table.findChildren('tr')  # [5]
    for row in centerd_table_data:
        if 'MPAA' in row.text:
            film_mpaa_rating = row.find('b')
            film_mpaa_rating = film_mpaa_rating.text
    return film_mpaa_rating

def find_date_of_release(movie_data):
    centerd_table = movie_data.findChildren('center')[0]
    centerd_table_data = centerd_table.findChildren('tr')
    for row in centerd_table_data:
        if 'Distributor' in row.text:
            if 'Release' in row.text:
                date_of_release = row.find_all('b')
                date_of_release = date_of_release[1].text
        else:
            if 'Release' in row.text:
                date_of_release = row.find('b')
                date_of_release = date_of_release.text

    try:
        date_of_release = datetime.strptime(date_of_release, "%B %d, %Y")
        date_of_release = datetime.strftime(date_of_release, "%m/%d/%Y")
    except ValueError:
        date_of_release = date_of_release

    return date_of_release


def find_running_time(movie_data):
    try:
        centerd_table = movie_data.findChildren('center')[0]
        centerd_table_data = centerd_table.findChildren('tr')
        for row in centerd_table_data:
            if 'Genre' in row.text:
                if 'Runtime' in row.text:
                    running_time = row.find_all('b')
                    running_time = running_time[1].text
            else:
                if 'Runtime' in row.text:
                    running_time = row.find('b')
                    running_time = running_time.text
        if running_time == 'N/A':
            pass
        else:
            running_time = running_time.replace('hrs.', '').replace('min.', '')
            running_time = running_time.split()
            running_time = (int(running_time[0]) * 60) + (int(running_time[1]))
            running_time = str(running_time)
    except IndexError:
        running_time = 'null'
    return running_time

filename = 'C:/Users/Public/bom_film_edited_urls.csv'
URL_Of_Film_list = []
URL_Of_Film_reader = csv.reader(open(filename))
for row in URL_Of_Film_reader:
    for item in row:
        URL_Of_Film_list.append(item)

if __name__ == "__main__":

    filename = './data/bom_film_data.csv'
    outputFile = open(filename, 'w')
    outputFile.write('Movie name, URL, Release Date, MPAA Rating, Run Time,  Opening Weekend Total, Number of Theaters, Domestic Total Sales, Foreign Total Sales, Global Total Sales\n')
    count = 0
    for URL_Of_Film in URL_Of_Film_list:
        count += 1
        print(str(count) + ":" + URL_Of_Film)
        try:
            movie_data = BeautifulSoup(urllib.request.urlopen(URL_Of_Film))
            movie_name = movie_name_finder(movie_data)
            date_of_release = find_date_of_release(movie_data)
            film_mpaa_rating = find_film_mpaa_rating(movie_data)
            running_time = find_running_time(movie_data)
            opening_weekend_totals = find_opening_weekend_totals(movie_data)
            theater_count = find_theater_count(movie_data)
            domestic_total = domestic_total_finder(movie_data)
            total_foreign = find_total_foreign(movie_data)
            total_global = find_total_global(movie_data)
        except urllib.error.HTTPError:
            pass
        outputFile.write(
            movie_name + ',' + URL_Of_Film + ',' + date_of_release + ',' + film_mpaa_rating + ',' + running_time + ',' + opening_weekend_totals + ',' + theater_count + ',' + domestic_total + ',' + total_foreign + ',' + total_global + '\n')

    outputFile.close()