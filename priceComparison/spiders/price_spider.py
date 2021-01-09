import scrapy
import re

class CENEO_spider(scrapy.Spider):
    name = "prices"
    start_urls = [
        'https://www.ceneo.pl/Laptopy'
    ]

    custom_settings = {
        "AUTOTHROTTLE_ENABLED" : True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def create_params(name):
        regex = r' ([0-9]+(?:[,.][0-9])?)(?:\"\/|''\/| )([^ \/]+)\/([0-9]+GB)\/(.+?)\/(.+?) '
        params = re.search(regex, name)
        if params is not None:
            return params.groups()        
        else:
            return ('', '', '', '', '')


    def parse(self, response):
        laptops = response.css('div.category-list-body .cat-prod-row')
        
        for laptop in laptops:
            shop_button = laptop.css('div.cat-prod-row__content .cat-prod-row__price .btn-compare-outer a::text').get()
            if shop_button is None:
                continue 
            if shop_button.lower() == 'idź do sklepu':
                name = laptop.css('div.cat-prod-row__content .cat-prod-row__name a::text').get()
                value = laptop.css('div.cat-prod-row__content .cat-prod-row__price .price .value::text').get()
                penny = response.css('div.cat-prod-row__content .cat-prod-row__price .price .penny::text').get()

                if name is not None and value is not None and penny is not None:
                    name = name.strip()
                    value = value.strip()
                    penny = penny.strip()
                    params = CENEO_spider.create_params(name)

                    yield {
                        'producer': name.split(' ')[0],
                        'name': name,
                        'screen': params[0],
                        'cpu': params[1],
                        'memory': params[2],
                        'storage': params[3],
                        'os': params[4],
                        'price': float(value + penny.replace(',', '.')) 
                    }
            
            elif shop_button.lower() == "porównaj ceny":
                name = laptop.css('div.cat-prod-row__content .cat-prod-row__name a::text').get()
                link = laptop.css('div.cat-prod-row__content .cat-prod-row__price .btn-compare-outer a::attr(href)').get()
                if link:
                    link = response.urljoin(link)
                    yield response.follow(link, callback=self.parse_product, meta={'name': name.strip()})    

        next_page = response.css('.category-list-footer .pagination a.pagination__next::attr(href)').get()
        print('-------------*************next page available', next_page is not None)
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_product(self, response):
        products = response.css('div.product-offer-2020')
        print('----------------- products:', len(products))
        shop_prices = {}
        params = CENEO_spider.create_params(response.meta['name'])
        for product in products:
            logo = product.css('div.product-offer-2020__store .store-logo img::attr(alt)').get()
            value = product.css('div.product-offer-2020__product__price .product-price .price .value::text').get() 
            penny = product.css('div.product-offer-2020__product__price .product-price .price .penny::text').get()   

            shop_prices[logo] = float(value + penny.replace(',', '.'))
             
        
        yield {
            'producer': response.meta['name'].split(' ')[0],
            'name': response.meta['name'],
            'screen': params[0],
            'cpu': params[1],
            'memory': params[2],
            'storage': params[3],
            'os': params[4],
            'prices': shop_prices
        }


