# -*- coding: utf-8 -*-
import scrapy

class MovieReviewSpider(scrapy.Spider):
    name = 'movie_review'
    allowed_domains = ['www.adorocinema.com']
    start_urls = ['http://www.adorocinema.com/filmes/criticas-filmes/?page=2']
    
    def parse(self, response):
        movies = response.xpath('//*[@id="content-layout"]/section[3]/div/ul/li[(contains(@class, "hred"))]')
        for movie in movies:
            links = 'http://www.adorocinema.com' + str(movie.xpath('./div/div[1]/h2/a/@href').get())
            yield scrapy.Request(url=links,callback=self.cb)
            #yield scrapy.Request(links + '/criticas-adorocinema/', callback=self.cbb)

        page = int(response.xpath('/html/head/title/text()').get().split('Página ')[-1]) + 1
        next_page = ('http://www.adorocinema.com/filmes/criticas-filmes/?page='+ str(page))
        self.log(f"===========PÁGINA========== {page}")
        yield scrapy.Request(next_page, callback=self.parse)

    #def cbb(self,response):
    #    review_content = response.xpath('string(//*[contains(@class, "editorial-content cf")])').get()
    #    return review_content

    def cb(self,response):

        movie_id = response.xpath('//*[@id="content-layout"]/@data-seance-geoloc-redir').get()
        title = response.xpath('//*[@id="content-layout"]/div[2]/div[1]/text()').get()      
        original_title = response.xpath('//*[contains(text()," Título original ")]/../h2/text()').get()
        publisher = response.xpath('//*[contains(text(),"Distribuidor")]/../span[2]/text()').get()
        director = response.xpath('//*[contains(text(),"Direção:")]/../span[2]/text()').get()
        casting_1 = response.xpath('//*[contains(text(),"Elenco:")]/../span[2]/text()').get()
        casting_2 = response.xpath('//*[contains(text(),"Elenco:")]/../span[3]/text()').get()
        casting_3 = response.xpath('//*[contains(text(),"Elenco:")]/../span[4]/text()').get()
        location = response.xpath('//*[contains(text(),"Nacionalidade")]/../span[2]/text()').get()
        year = response.xpath('//*[contains(text(),"Ano de produção")]/../span[2]/text()').get()
        date = response.xpath('string(//*[contains(@class,"date")]/text())').get()
        runtime = response.xpath('string(//*[@id="content-layout"]/section/div/div[2]/div[1]/div/div[1])').get().split('\n')[19].split('                                            ')[1]
        movie_type = response.xpath('//*[contains(text(),"Tipo de filme")]/../span[2]/text()').get()
        budget = response.xpath('//*[contains(text(),"Orçamento")]/../span[2]/text()').get()
        language = response.xpath('//*[contains(text(),"Idiomas")]/../span[2]/text()').get()
        review_title = response.xpath('//*[contains(@class,"editorial-header-title")]/p/text()').get()
        review_expert = response.xpath('//*[contains(@class,"editorial-header")]/div[2]/span/text()').get()
        expert_rating = response.xpath('//*[@id="content-layout"]/section/div/div[2]/div[3]/div/div/div/span/text()').get()
        user_rating = response.xpath('//*[contains(@class, "stareval-note")]/text()').get()

        synopsis = response.xpath('string(//*[contains(@class,"content-txt")])').get().split('\n                      ')[1].split('\n        \n            ')[0]

        genre_1 = response.xpath('string(//*[@id="content-layout"]/section/div/div[2]/div[1]/div/div[1])').get().split('\n                                                ')[7]
        genre_2 = response.xpath('string(//*[@id="content-layout"]/section/div/div[2]/div[1]/div/div[1])').get().split('\n                                                ')[9].split('\n                                        \n                    \n                ')[0]



        content_json = { 'movie_id':movie_id,
                         'title': title,
                         'original_title':original_title,
                         'publisher':publisher,
                         'director':director,
                         'casting_1':casting_1,
                         'casting_2':casting_2,
                         'casting_3':casting_3,
                         'location':location,
                         'year':year,
                         'date':date,
                         'genre_1':genre_1,
                         'genre_2':genre_2,
                         'runtime':runtime,
                         'movie_type':movie_type,
                         'budget':budget,
                         'language':language,
                         'review_title':review_title,
                         'review_expert':review_expert,
                         'expert_rating':expert_rating,
                         'user_rating':user_rating,
                         'synopsis':synopsis
                         }

        return content_json