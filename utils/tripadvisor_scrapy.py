import scrapy
class TripAdvisorsSpider(scrapy.Spider):
     
    # Spider name
    name = 'food_reviews'
     
    # Domain names to scrape
     
    # Base URL for the MacBook air reviews
    myBaseUrl = "https://www.tripadvisor.co.uk/RestaurantSearch?Action=PAGE&geo=187454&ajax=1&itags=10591&sortOrder=relevance&o=a"
    url = "&availSearchEnabled=true&eaterydate=2019_08_22&date=2019-08-22&time=20%3A00%3A00&people=2"
    start_urls=[]
    
    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(0,40):
        start_urls.append(myBaseUrl+str(i*30)+url)
    
    # Defining a Scrapy parser
    def parse(self, response):
            data = response.css('.restaurants-list-ListCell__cellContainer--2mpJS')
             
            # Collecting product star ratings
            rest_name = data.css('.restaurants-list-ListCell__titleRow--3rRCX .restaurants-list-ListCell__restaurantName--2aSdo')
             
            # Collecting user reviews
            rest_type = data.css('.restaurants-list-ListCell__infoRowElement--2E6E3')
            count = 0
             
            # Combining the results
            for rests in data:
                yield{'rest_name': ','.join(rests[:5].xpath('.//text()').extract())
                    #   'type': ','.join(rest_type[count].xpath(".//text()").extract())
                    #   'type': ''.join(rest_type[1].xpath(".//text()").extract()),
                    #   'type': ''.join(rest_type[2].xpath(".//text()").extract())
                     }
                count=count+1
