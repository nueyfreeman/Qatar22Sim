"""
QatarSquadScraper.py

A program to scrape the squad roster of all teams for 2022 Qatar World Cup from Wikipedia.
"""

import requests
from requests_html import HTMLSession
import bs4

WIKI = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'


def get_stats(catch_error, player_name, keeper=False):
    name = player_name.replace(' ', '+')
    print(name)
    url = 'https://www.transfermarkt.us/schnellsuche/ergebnis/schnellsuche?query=' + name
    session = HTMLSession()
    r = session.get(url)
    try:
        soup = bs4.BeautifulSoup(r.content, 'html.parser').find('div', 'large-12 columns').find('div', 'box')
        link = soup.find('tbody').find('td', 'hauptlink').find('a')['href'].replace('profil', 'leistungsdaten')
    except AttributeError:
        print(f'{player_name}: Not found.')
        catch_error.write(f'{player_name}\n')
        return '0,0,0,0,0'
    home_link = 'https://www.transfermarkt.us'
    stat_link = home_link + link

    return scrape_stats(catch_error, stat_link, session, player_name, keeper)


def scrape_stats(oops, link, session, player, keeper=False):
    stat_page = session.get(link)
    soup = bs4.BeautifulSoup(stat_page.content, 'html.parser').body
    try:
        content = soup.find('div', 'large-8 columns').find_all('div', 'box')
        table = content[1].find('tfoot').find_all('td')
        if not keeper:
            minutes = table[8].text.replace('\'', '').replace('.', '')
            # print(f'Matches - {table[2].text}, Goals - {table[3].text}, '
            #      f'Assists - {table[4].text}, Minutes - {minutes}')
            return f'{table[2].text},{table[3].text},{table[4].text},{minutes},0'
        else:
            # print(f'Matches = {table[2].text}, Clean Sheets - {table[8].text}')
            return f'{table[2].text},0,0,0,{table[8].text}'
    except (IndexError, AttributeError):
        print(f'For {player} found non-player')
        oops.write(f'{player}\n')
        return '0,0,0,0,0'


def main():
    with open('QatarSquadsv2.csv', 'w') as output, open('errors.csv', 'w') as errors:
        out_string = ''

        r = requests.get(WIKI)
        body = bs4.BeautifulSoup(r.content, 'html.parser').body
        meat = body.find('div', 'mw-body-content mw-content-ltr')
        choice_cut = meat.find('div', 'mw-parser-output')
        group = ''
        country = ''
        for tag in choice_cut:
            if tag.name == 'h2':  # get group
                print(f'\n\n{tag.string}\n')
                group = tag.string
            if tag.name == 'h3':  # get country
                print(f'\n{tag.string}')
                country = tag.string
            if tag.name == 'table':  # player table
                players = tag.find_all('tr', 'nat-fs-player')  # row tag
                for each in players:
                    p = each.contents
                    position = p[3].find('a').text.strip()
                    name = p[5].find('a').text.strip()
                    club = p[13]
                    c = club.text.strip()
                    c_country = club.find('img')['alt']
                    if position == 'GK':
                        stats = get_stats(errors, name, True)
                    else:
                        stats = get_stats(errors, name)
                    out_string += f'{group},{country},{position},{name},{c},{c_country},{stats}\n'
        output.write(out_string)


def get_koreans():
    with open('koreans.csv', 'w') as data, open('kerrors.csv', 'w') as kerrors:
        koreans = 'Yoon Jong-gyu,Kim Jin-su,Kim Min-jae,Jung Woo-young,Hwang In-beom,Son Heung-min,' \
                  'Paik Seung-ho,Cho Gue-sung,Lee Jae-sung,Hwang Hee-chan,Son Jun-ho,Kim Moon-hwan,' \
                  'Hwang Ui-jo,Na Sang-ho,Lee Kang-in,Kim Young-gwon,Kwon Kyung-won,Kwon Chang-hoon,' \
                  'Kim Tae-hwan,Cho Yu-min,Jeong Woo-yeong,Song Min-kyu'
        klist = koreans.split(',')
        out_string = ''
        for k in klist:
            name = k.split(' ')
            rename = name[1] + ' ' + name[0]
            stats = get_stats(kerrors, rename)
            out_string += f'{rename},{stats}\n'
        data.write(out_string)


if __name__ == '__main__':
    xget_koreans()
