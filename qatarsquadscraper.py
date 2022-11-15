"""
QatarSquadScraper.py

A program to scrape the squad roster of all teams for 2022 Qatar World Cup from Wikipedia.
"""

import requests
from requests_html import HTMLSession
import bs4

WIKI = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads'


def get_stats():
    url = 'https://www.transfermarkt.us/heung-min-son/leistungsdaten/spieler/91845'
    session = HTMLSession()
    r = session.get(url)
    runit = bs4.BeautifulSoup(r.content, 'html.parser')
    words = runit.prettify
    test_file = open('testhtml.txt', 'w')
    test_file.write(str(words))
    test_file.close()


def main():
    output = open('QatarSquads.csv', 'w')
    out_string = ''#'Group,Country,Position,Player,Club,ClubCountry,ClubAssoc\n'

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
                print(f'{position}, {name}, {c}, {c_country}, {c_assoc}')
                out_string += f'{group},{country},{position},{name},{c},{c_country},{c_assoc}\n'
    output.write(out_string)
    output.close()


if __name__ == '__main__':
    main()
