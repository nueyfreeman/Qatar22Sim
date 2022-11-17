"""
QatarSquadScraper.py

A program to scrape the squad roster of all teams for 2022 Qatar World Cup from Wikipedia.
"""

import requests
from requests_html import HTMLSession
import bs4

WIKI = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'


def get_stats(player_name, keeper=False):
    name = player_name.replace(' ', '+')
    url = 'https://www.transfermarkt.us/schnellsuche/ergebnis/schnellsuche?query=' + name
    session = HTMLSession()
    r = session.get(url)
    try:
        soup = bs4.BeautifulSoup(r.content, 'html.parser').find('div', 'large-12 columns').find('div', 'box')
        link = soup.find('tbody').find('td', 'hauptlink').find('a')['href'].replace('profil', 'leistungsdaten')
    except AttributeError:
        print(f'{player_name}: Not found.')
        return '0,0,0,0,0'
    home_link = 'https://www.transfermarkt.us'
    stat_link = home_link + link

    return scrape_stats(stat_link, session, keeper)


def scrape_stats(link, session, keeper=False):
    stat_page = session.get(link)
    soup = bs4.BeautifulSoup(stat_page.content, 'html.parser').body
    content = soup.find('div', 'large-8 columns').find_all('div', 'box')
    table = content[1].find('tfoot').find_all('td')
    if not keeper:
        minutes = table[8].text.replace('\'', '').replace('.', '')
        #print(f'Matches - {table[2].text}, Goals - {table[3].text}, '
        #      f'Assists - {table[4].text}, Minutes - {minutes}')
        return f'{table[2].text},{table[3].text},{table[4].text},{minutes},0'
    else:
        #print(f'Matches = {table[2].text}, Clean Sheets - {table[8].text}')
        return f'{table[2].text},0,0,0,{table[8].text}'


def main():
    output = open('QatarSquadsv2.csv', 'w')
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
                c_assoc = club.find('span').find('a')['title']
                c_country = club.find('img')['alt']
                #print(f'{position}, {name}, {c}, {c_country}')
                stats = '0,0,0,0,0'
                if position == 'GK':
                    stats = get_stats(name, True)
                else:
                    stats = get_stats(name)
                out_string += f'{group},{country},{position},{name},{c},{c_country},{stats}\n'
    output.write(out_string)
    output.close()


if __name__ == '__main__':
    main()
