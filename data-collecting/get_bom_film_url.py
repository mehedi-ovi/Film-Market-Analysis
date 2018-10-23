import urllib
from bs4 import BeautifulSoup
index_base_url = 'http://www.boxofficemojo.com'
initial_url_data = 'http://www.boxofficemojo.com/movies/'



def parse_index_alphabetical(initial_url_data):
    url_indexes = []
    initial_url_data_soup = BeautifulSoup(urllib.request.urlopen(initial_url_data))
    all_tables_index = initial_url_data_soup.find_all('table')
    indexed_table = all_tables_index[1]
    indexed_table_row = indexed_table.find_all('tr')
    targeted_row = indexed_table_row[1]
    targeted_columns = targeted_row.find_all('td')
    for column in targeted_columns:
        index_url = column.find('a').get('href')
        final_index_url = initial_url_data + index_url
        url_indexes.append(final_index_url)
    return url_indexes


def parse_index_pages(url_indexes):
    secondary_indexes = []
    index_url_base = 'http://www.boxofficemojo.com'
    for item in url_indexes:
        secondary_indexes.append(item)
        primary_index_soup = BeautifulSoup(urllib.request.urlopen(item))
        targeted_table = primary_index_soup.find('div', {'class': 'alpha-nav-holder'})
        targeted_table_tags = targeted_table.find_all('a')
        for tag in targeted_table_tags:
            secondary_index_url = tag.get('href')
            secondary_index_url = index_url_base + secondary_index_url
            secondary_indexes.append(secondary_index_url)
    return secondary_indexes


def build_filmpage_list(secondary_indexes):
    URL_Of_Film_list = []

    for item in secondary_indexes:
        secondary_index_soup = BeautifulSoup(urllib.request.urlopen(item))
        page_urls = secondary_index_soup.find_all('a')
        for url in page_urls:
            url = url.get('href')
            url_split = url.split('=')
            if url_split[0] == '/movies/?id':
                if url == '/movies/?id=fast7.htm':
                    pass
                else:
                    url = url.replace(',', '')
                    URL_Of_Film_list.append(url)
    URL_Of_Film_list.append(
        '/movies/?id=fast7.htm')
    return URL_Of_Film_list


if __name__ == "__main__":

    filename = './data/bom_URL_Of_Films_data.csv'
    outputFile = open(filename, 'w')

    url_indexes = parse_index_alphabetical(initial_url_data)
    secondary_indexes = parse_index_pages(url_indexes)
    URL_Of_Film_list = build_filmpage_list(secondary_indexes)

    for URL_Of_Film in URL_Of_Film_list:
        final_url = index_base_url + URL_Of_Film
        outputFile.write(final_url + '\n')

    outputFile.close()
