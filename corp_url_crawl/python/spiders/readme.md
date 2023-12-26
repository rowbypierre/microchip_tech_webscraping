# Description
This Python code is a script for a web crawler using the Scrapy framework.This script was created using the [Microchip Technology](https://www.microchip.com/) Internship to scrape data from thier Corporate static websties in order to ingest into ChatGPT to produce sets of frequently asked questions and answers. The script defines two classes, CrawlingSpider and CrawlingSpiderMain, both of which inherit from CrawlSpider, a class provided by Scrapy for creating crawling spiders.

# Functionality
1. **Import Statements:** 
    * `CrawlSpider` class is a spider for crawling sites and following links.
        ```python 
        from scrapy.spiders import CrawlSpider
        ```
    * `Rule` class is used to define the patterns for URLs that the spider should follow.
        ```python 
        from scrapy.spiders import Rule
        ```
    * `LinkExtractor` class is used to extract links from webpages.
        ```python 
        from scrapy.linkextractors import LinkExtractor
        ```

2. **Crawling Spider Classes**
    * Newly defined classes inherit properties from `CrawlingSpider` Class previouly imported.
        ```python
        class CrawlingSpider(CrawlSpider):
        ```
        &
        ```python
        class CrawlingSpiderMain(CrawlSpider):
        ``` 
    * `name` identifies spider.
        ```python
        name = "team4"
        ```
        &
        ```python
        name = "ayah" 
        ``` 
    * `allowed_domains` restricts spider crawling to listed domains.
        ```python
        allowed_domains = ["microchip.com"]  
        ```
    * `start_url` specifies crawling starting point.
        ```python
        start_urls = ["https://www.microchip.com/"] 
        ```
    * `rules` using `LinkExtractor` directs crawler to follow links that match a specific pattern.`callback="parse_item"` specifies that the parse_item method should be called for each link that matches the rule.
        ```python
        rules = (
        Rule(LinkExtractor(allow="en-us/solutions/data-centers-and-computing"), callback="parse_item"),     
        )
        ```
        &
        ```python
        rules = (
        Rule(LinkExtractor(allow="en-us/solutions/low-power"), callback="parse_item"),                      
        )
        ```
3. **parse_item Method in CrawlingSpider:**
    * This method is called for each response obtained from the links followed by the spider. Various elements are extracted from each page, such as the title, text paragraphs, and headings, and yields them as a dictionary.
        ```python
        def parse_item(self, response):
        list_items = [item.strip() for item in response.css("li::text").extract() if item.strip() ]

        yield{      
            "*******Webpage Title*******": response.css("h1::text").get(),                            
            "*******Webpage Text*******": response.css("p::text").getall(),                            
            "*******Sub Heading Mid*******": response.css("h2::text").getall(),                            
            "*******Sub Headings Low*******": response.css("h3::text").getall(),                            
            "*******Sub Heading Text (List)*******": list_items                     
        }
        ```

4. **Execution:**
    * Crawling
        ```   
        terminal >> scrapy crawl [crawler `name`]
        ```
    * Crawling & Scape 
        ```   
        terminal >> scrapy crawl [crawler `name`] -o file_name.extension
        ```




