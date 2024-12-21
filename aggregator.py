import json
import requests
from datetime import datetime
import pytz
from bs4 import BeautifulSoup

from util import random_agent, contains_any, create_name_list


def canucksarmy():
    """ Scrape front-page articles from CanucksArmy """
    url = "https://canucksarmy.com"
    response = requests.get(url, headers=random_agent())
    if response.status_code != 200: return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles_tag = soup.find(id='__NEXT_DATA__')
    articles = []
    if articles_tag:
        data = json.loads(articles_tag.contents[0])
        for post in data['props']['pageProps']['frontPagePosts']:
            post_node = post['node']
            
            title = post_node['title']
            published = post_node['dateGmt']
            link = url + '/news/' + post_node['slug']
            author = post_node['author']['node']['name']
            source = 'CanucksArmy'

            articles.append({
                'title': title,
                'published': published,
                'link': link,
                'author': author,
                'source': source
            })
    return articles

def espn(canucks_names):
    """ Collect ESPN articles from RSS feed """
    def convert_time(time):
        """ Convert EST to GMT """
        date_obj = datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")
        est_timezone = pytz.timezone('US/Eastern')
        date_obj = est_timezone.localize(date_obj)
        gmt_obj = date_obj.astimezone(pytz.utc)
        iso_date_gmt = gmt_obj.isoformat()
        return iso_date_gmt

    feed = 'https://www.espn.com/espn/rss/nhl/news'
    response = requests.get(feed, headers=random_agent())
    if response.status_code != 200: return []
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')
    articles = []
    for item in items:
        title = item.find('title').get_text(strip=True)
        description = item.find('description').text
        if not contains_any(title.lower(), canucks_names) and not contains_any(description.lower(), canucks_names):
            continue
        published = convert_time(item.find('pubDate').get_text(strip=True))
        link = item.find('link').get_text(strip=True) 
        author = item.find('dc:creator').get_text(strip=True) if item.find('dc:creator') else 'ESPN'
        source = 'ESPN'

        articles.append({
                'title': title,
                'published': published,
                'link': link,
                'author': author,
                'source': source
            })
    return articles

def nhl():
    """ Use RSS feed; will need to replace with scraper """
    def convert_time(time):
        """ Convert pubDate to ISO time"""
        date_obj = datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")
        iso_date_gmt = date_obj.isoformat()
        return iso_date_gmt
    feed = 'https://rss.app/feeds/tnUOanvGGDBWhhuW.xml'
    response = requests.get(feed, headers=random_agent())
    if response.status_code != 200: return []
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')
    articles = []
    for item in items:
        title = item.find('title').get_text(strip=True)
        published = convert_time(item.find('pubDate').get_text(strip=True))
        link = item.find('link').get_text(strip=True) 
        author = item.find('dc:creator').get_text(strip=True) if item.find('dc:creator') else 'ESPN'
        source = 'NHL'

        articles.append({
                'title': title,
                'published': published,
                'link': link,
                'author': author,
                'source': source
            })
    return articles

def province():
    """ Scrape 5 most recent articles from The Province """
    url = 'https://theprovince.com/category/sports/hockey/nhl/vancouver-canucks/?more=vancouver-canucks'
    response = requests.get(url, headers=random_agent())
    if response.status_code != 200: return []

    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', type='application/ld+json')
    articles = []
    if script:
        data = json.loads(script.string)['hasPart']
        for article in data:
            title = article['headline']
            published = article['datePublished']
            link = article['url']
            author = article['author']['name']
            source = 'The Province'

            articles.append({
                'title': title,
                'published': published,
                'link': link,
                'author': author,
                'source': source
            })
        # print(json.dumps(data, indent=4))
    return articles

def sportsnet():
    """ Scrape teamArticles from Canucks Sportsnet page"""
    def convert_time(time):
        """ Convert post_date_gmt to ISO time"""
        dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        iso_date = dt.isoformat()
        return iso_date
    
    url = 'https://www.sportsnet.ca/hockey/nhl/teams/vancouver-canucks/'
    response = requests.get(url, headers=random_agent())
    if response.status_code != 200: return []
    soup = BeautifulSoup(response.text, 'html.parser')

    json_data = soup.find(id='__NEXT_DATA__')
    team_articles = json.loads(json_data.contents[0])['props']['pageProps']['teamArticles']

    articles = []
    for article in team_articles:
        title = article['post_title']
        published = convert_time(article['post_date_gmt'])
        link = article['link']
        author = article['author_name']
        source = 'Sportsnet'
        
        articles.append({
                'title': title,
                'published': published,
                'link': link,
                'author': author,
                'source': source
            })
        
    return articles


def aggregate_news():
    """ Aggregate news from all sources, and sort by most recent """
    canucks_list = create_name_list()
    news = []

    sources = [
        (canucksarmy, "CanucksArmy"),
        (espn, "ESPN"),
        (nhl, "NHL.com"),
        (province, "The Province"),
        (sportsnet, "Sportsnet")
    ]

    for func, source in sources:
        try:
            news += func(canucks_list) if source == "ESPN" else func()
        except Exception as e:
            print(f"Unable to collect news from {source}: {str(e)}")

    news = sorted(news, key=lambda x: x["published"], reverse=True)
    return news