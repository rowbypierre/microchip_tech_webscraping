from scrapy.spiders import CrawlSpider, Rule                                                                #importing CrawlSpider class, Rule class (specify rules)
from scrapy.linkextractors import LinkExtractor                                                             #import LinkExtractor to extract links

                                                                                                            #create CrawlingSpider class inherit from CrawlSpider class (imported above)
class CrawlingSpider(CrawlSpider):
    name = "team4"                                                                                          #assign "team4" name/identifier to spider
    allowed_domains = ["microchip.com"]                                                                     #assign allowed domain name(s)
    start_urls = ["https://www.microchip.com/"]                                                             #page to begin scrapping 
    
    rules = (
        Rule(LinkExtractor(allow="en-us/solutions/data-centers-and-computing"), callback="parse_item"),     #pattern after start url - accepted & denied, push links to function
    )
    
    def parse_item(self, response):
        list_items = [item.strip() for item in response.css("li::text").extract() if item.strip() ]         #strip list elements before extracting
        
        yield{                                                                                              #get generated objects to values
            "*******Webpage Title*******": response.css("h1::text").get(),                                  #get headings
            "*******Webpage Text*******": response.css("p::text").getall(),                                 #get paragraph text 
            "*******Sub Heading Mid*******": response.css("h2::text").getall(),                             #get level 2/sub headings 
            "*******Sub Headings Low*******": response.css("h3::text").getall(),                            #get level 3/sub headings 
            "*******Sub Heading Text (List)*******": list_items                                             #striped list elements to be parsed
        }
        
class CrawlingSpiderMain(CrawlSpider):
    name = "ayah"                                                                                           #assign "team4" name/identifier to spider
    allowed_domains = ["microchip.com"]                                                                     #assign allowed domain name(s)
    start_urls = ["https://www.microchip.com/"]                                                             #page to begin scrapping 
    
    rules = (
        Rule(LinkExtractor(allow="en-us/solutions/low-power"), callback="parse_item"),                      #pattern after start url - accepted & denied, push links to function
    )
    
    def parse_item(self, response):
        list_items = [item.strip() for item in response.css("li::text").extract() if item.strip() ]         #strip list elements before extracting
        
        yield{                                                                                              #set generated objects to values
            "*******Webpage Title*******": response.css("h1::text").get(),                                  #get headings 
            "*******Webpage Text*******": response.css("p::text").getall(),                                 #get paragraph text 
            "*******Sub Heading Mid*******": response.css("h2::text").getall(),                             #get level 2/sub headings 
            "*******Sub Headings Low*******": response.css("h3::text").getall(),                            #get level 3/sub headings 
            "*******Sub Heading Text (List)*******": list_items                                             #striped list elements to be parsed
        }
        
