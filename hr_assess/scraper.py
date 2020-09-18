import requests

from bs4 import BeautifulSoup, NavigableString
from xlwt import Workbook


BASE_URL = 'https://www.state.gov/reports/{}-country-reports-on-human-rights-practices/{}/'
YEARS = ['2016']


def get_links(year):
    r = requests.get(BASE_URL.format(year, 'afghanistan'))
    assert r.status_code == 200

    soup = BeautifulSoup(r.text, features="lxml")
    links = soup.find_all("select")[1]

    return [x['value'] for x in links if (x != '\n' and x['value'] != "")]


# get links for all countries and store in list

def clean_country_name(name):
    chars = ["'", "(", ")", ",", "’"]
    name = name.replace(' ', '-')
    for char in chars:
        name = name.replace(char, "")
    return name


def get_page_content():

    book = Workbook()
    sheet = book.add_sheet('hr_reports_fl')
    count = 0

    for year in YEARS:
        links = get_links(year)

        print("Starting {} reports\n".format(year))
        for link in links:

            r = requests.get(link)
            assert r.status_code == 200
            soup = BeautifulSoup(r.text, features="lxml")

            paras = soup.body.find_all(id="report-toc__section-7__subsection-2")[0].next_siblings
            text = ' '.join([x.text for x in paras if type(x) != NavigableString])
            country = link[77:].strip('/')

            sheet.write(count, 0, "{} {}".format(country, year))
            sheet.write(count, 1, text)
            count += 1
            print("Data downloaded for {} {}".format(country, year))

    book.save('hr_reports_fl.xls')
    print("Writing complete - workbook saved")


get_page_content()