from aggregator import aggregate_news
from stats import find_leaders

def print_leader(leaders, key):
    print(key)
    print(f"{leaders[key.lower()]['name']} #{leaders[key.lower()]['number']}")
    print(leaders[key.lower()]['headshot'])
    print(f"{leaders[key.lower()][key.lower()]} {key.lower()}\n")

print("Collecting news...")

leaders = find_leaders()
print_leader(leaders, 'Points')
print_leader(leaders, 'Goals')
print_leader(leaders, 'Assists')

articles = aggregate_news()
for article in articles:
    title, published, link, author, _ = article
    print(article['title'])
    print(article['author'])
    print(article['published'])
    print(article['link'])
    print(article['source'])
    print('\n')