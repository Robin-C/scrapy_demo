import scrapy


class pmuSpider(scrapy.Spider):
    name = "races"

    def start_requests(self):
        urls = [
             'https://horseraces.pmu.fr/racecards'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        meetings = response.css('div.meeting.clearfix')
        for meeting in meetings:
          yield {
              'meeting': meeting.css('h3.coursename::text').get(),
              'races': meeting.css('span.racename::text').getall(),
              'heures': meeting.css('span.race-time::text').getall()
          }

        races = response.css('ol.meeting li.result')
        for race in races:
              url = race.css('a::attr(href)').get()
              full_url = response.urljoin(url)
              race = race.css('span.racename::text').get()
              yield scrapy.Request(full_url, callback=self.parse_runners, meta={'race': race})

    def parse_runners(self, response):
        runners = response.css('a.horse-name')
        for runner in runners:
            yield {
                'race': response.meta['race'],
                'horse_name': runner.css('a.horse-name::text').getall()
            }

