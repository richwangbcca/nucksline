from aggregator import aggregate_news

print("Collecting news...")

articles = aggregate_news()
for article in articles:
    title, published, link, author, _ = article
    print(article['title'])
    print(article['author'])
    print(article['published'])
    print(article['link'])
    print(article['source'])
    print('\n')