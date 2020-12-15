import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse


class AmazonSpider(scrapy.Spider):
    name = 'amazon_comments'
    start_urls = [
        "https://www.amazon.com/Hands-Graph-Analytics-Neo4j-visualization-ebook/product-reviews/B08FBJ3B1S",
        "https://www.amazon.de/Hands-Graph-Analytics-Neo4j-visualization-ebook/product-reviews/B08FBJ3B1S?language=en_GB",
        "https://www.amazon.co.uk/Hands-Graph-Analytics-Neo4j-visualization-ebook/product-reviews/B08FBJ3B1S?language=en_GB",
        "https://www.amazon.fr/Hands-Graph-Analytics-Neo4j-visualization-ebook/product-reviews/B08FBJ3B1S?language=en_GB",
    ]

    def parse(self, response):
        country = response.css('div#cm_cr-review_list h3::text').get() or ""
        country = country .strip("\n ")
        url = urlparse(response.url).netloc
        # logging.warning("URL %s", response.url)
        for comment in response.css('div.review'):
            title = comment.css('a.review-title span::text').get()
            content = comment.css('span.review-text-content span::text').extract()
            content = " - ".join(c.strip("\n ") for c in content)
            path = comment.css('a.review-title::attr("href")').get()
            stars_text = comment.css('i.review-rating span::text').get()
            stars = None
            for i in range(1, 6):
                if str(i) in stars_text:
                    stars = i
                    break
            if stars:
                self.crawler.stats.inc_value('stars', stars)
                self.crawler.stats.inc_value('nb', 1)
            yield {
                'country': country,
                'title': title,
                'link': f"{url}{path}",
                'stars': stars,
                'content': content,
            }


if __name__ == '__main__':
    process = CrawlerProcess(settings={
        "FEEDS": {
            "comments.json": {"format": "json"},
        },
        'USER_AGENT': 'Defined'
    })

    process.crawl(AmazonSpider)
    process.start() # the script will block here until the crawling is finished
