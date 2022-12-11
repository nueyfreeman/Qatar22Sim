"""
QatarSquadScraper.py

A program to scrape the squad roster of all teams for 2022 Qatar World Cup from Wikipedia and their recent statistics
from Transfermarkt.us. All data is written to a csv file which should be subsequently cleaned before being used in
main.py to avoid errors. Errors are recorded in a separate file to use in data cleaning/verification.
"""

import requests
from requests_html import HTMLSession
import bs4

WIKI = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'


# queries Transfermarkt.us for a given player and finds their statistic page
def get_stats(catch_error, player_name, keeper=False):  # includes flag for goalkeeper to be passed to scraping method
    name = player_name.replace(' ', '+')
    print(name)  # for troubleshooting/debugging
    url = 'https://www.transfermarkt.us/schnellsuche/ergebnis/schnellsuche?query=' + name  # queries site
    session = HTMLSession()
    r = session.get(url)

    try:
        soup = bs4.BeautifulSoup(r.content, 'html.parser').find('div', 'large-12 columns').find('div', 'box')

        # find link to statistic page on the query result page
        link = soup.find('tbody').find('td', 'hauptlink').find('a')['href'].replace('profil', 'leistungsdaten')

    # if player statistic page not found add zeros for all data and show error in console
    except AttributeError:
        print(f'{player_name}: Not found.')
        catch_error.write(f'{player_name}\n')  # records error to error file
        return '0,0,0,0,0'

    home_link = 'https://www.transfermarkt.us'
    stat_link = home_link + link

    return scrape_stats(catch_error, stat_link, session, player_name, keeper)


# scrapes player stats from player statistic page and returns an appropriate string to add them to csv file
def scrape_stats(oops, link, session, player, keeper=False):
    stat_page = session.get(link)
    soup = bs4.BeautifulSoup(stat_page.content, 'html.parser').body

    # scrapes player statistic page
    try:
        content = soup.find('div', 'large-8 columns').find_all('div', 'box')
        table = content[1].find('tfoot').find_all('td')
        if not keeper:  # scrape stats for an outfield player
            minutes = table[8].text.replace('\'', '').replace('.', '')  # cleans value
            return f'{table[2].text},{table[3].text},{table[4].text},{minutes},0'  # returns values for non-keeper
        else:  # scrapes stats for goalkeeper
            return f'{table[2].text},0,0,0,{table[8].text}'  # returns values as arranged for keeper

    # returns zeros and reports error if page found isn't a player page
    except (IndexError, AttributeError):
        print(f'For {player} found non-player')
        oops.write(f'{player}\n')  # record errors to error file
        return '0,0,0,0,0'


# scrapes Wikipedia page for all squad rosters and then gets match statistics for each player
# saves player data in csv file and records errors in a second file
def main():
    # opens a file to write player data and a file to record errors for later cleaning and verification of data
    with open('QatarSquadsv2.csv', 'w') as output, open('errors.csv', 'w') as errors:
        out_string = ''  # initializes string which will be written to file

        r = requests.get(WIKI)
        body = bs4.BeautifulSoup(r.content, 'html.parser').body
        meat = body.find('div', 'mw-body-content mw-content-ltr').find('div', 'mw-parser-output')
        group = ''
        country = ''
        for tag in meat:
            if tag.name == 'h2':  # get group
                print(f'\n\n{tag.string}\n')
                group = tag.string
            if tag.name == 'h3':  # get country
                print(f'\n{tag.string}')
                country = tag.string
            if tag.name == 'table':  # player table
                players = tag.find_all('tr', 'nat-fs-player')  # row tag
                for each in players:  # collects player data on Wiki page
                    p = each.contents
                    position = p[3].find('a').text.strip()
                    name = p[5].find('a').text.strip()
                    club = p[13]
                    c = club.text.strip()
                    c_country = club.find('img')['alt']

                    # scrapes Transfermarkt.us for match statistics for each player
                    if position == 'GK':
                        stats = get_stats(errors, name, True)  # flag for finding keeper data
                    else:
                        stats = get_stats(errors, name)

                    # adds player data from Wiki and Transfermarkt.us to string
                    out_string += f'{group},{country},{position},{name},{c},{c_country},{stats}\n'

        # write string to file
        output.write(out_string)


# used this function to retrieve data for Korean players - family name order impeded their queries at first attempt
def get_koreans():
    # same method for saving data and errors
    with open('koreans.csv', 'w') as data, open('kerrors.csv', 'w') as kerrors:
        # manually input names for this solution (copied and pasted from original error file)
        koreans = 'Yoon Jong-gyu,Kim Jin-su,Kim Min-jae,Jung Woo-young,Hwang In-beom,Son Heung-min,' \
                  'Paik Seung-ho,Cho Gue-sung,Lee Jae-sung,Hwang Hee-chan,Son Jun-ho,Kim Moon-hwan,' \
                  'Hwang Ui-jo,Na Sang-ho,Lee Kang-in,Kim Young-gwon,Kwon Kyung-won,Kwon Chang-hoon,' \
                  'Kim Tae-hwan,Cho Yu-min,Jeong Woo-yeong,Song Min-kyu'
        klist = koreans.split(',')
        out_string = ''
        for k in klist:  # Transfermarkt.us required swapping the order of names to query successfully
            name = k.split(' ')
            rename = name[1] + ' ' + name[0]  # only the order of names in the query needed to be changed
            stats = get_stats(kerrors, rename)  # used same method to scrape Transfermarkt.us
            out_string += f'{rename},{stats}\n'
        data.write(out_string)


if __name__ == '__main__':
    get_koreans()
