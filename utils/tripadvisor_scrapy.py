import scrapy

class TripAdvisorSpider(scrapy.Spider):
     
    # Spider name
    name = 'restaurant_reviews'
          
    # Base URL for the restaurant reviews on TripAdvisor
    url_head = "https://www.tripadvisor.co.uk/RestaurantSearch?Action=PAGE&geo=187454&ajax=1&itags=10591&sortOrder=relevance&o=a"
    url_tail = "&availSearchEnabled=true&eaterydate=2019_08_23&date=2019-08-23&time=20%3A00%3A00&people=2"
    start_urls=[]
    
    # Creating list of urls to be scraped by appending page number in the middle of base url
    
    for i in range(0,100): # loop through the number of pages
        start_urls.append(url_head + str(i*30) + url_tail)
    
    # Defining a Scrapy parser
    def parse(self, response):
             
            # Collecting restaurants reviews
            data = response.css('.restaurants-list-ListCell__cellContainer--2mpJS')
            rest_name = data.css('.restaurants-list-ListCell__titleRow--3rRCX .restaurants-list-ListCell__restaurantName--2aSdo')
            rest_info = data.css('.restaurants-list-ListCell__topInfoWrapper--1Tmxl')
            no_of_reviews = data.css('.restaurants-list-ListCell__userReviewCount--2a61M')
            rest_status = data.xpath('.//div[@class="restaurants-list-ListCell__infoRow--31xBt restaurants-list-ListCell__hideLeftDivider--3vXbe"]/span[2]')
            rest_type = data.xpath('.//div[@class="restaurants-list-ListCell__infoRow--31xBt restaurants-list-ListCell__hideLeftDivider--3vXbe restaurants-list-ListCell__cuisinePriceMenu--r4-Re"]/span[1]')
            
            count = 0
             
            # Combining the results
            for rests in rest_name:
                yield{
                    'rest_name': ''.join(rests.xpath('.//text()').extract()),
                    'status': ''.join(rest_status[count].xpath(".//text()").extract()),
                    'no_of_reviews': ''.join(no_of_reviews[count].xpath(".//text()").extract()),
                    'type': ''.join(rest_type[count].xpath('.//text()').extract()),
                    'info': ' '.join(rest_info[count].xpath(".//text()").extract())
                     }
                count=count+1
