import scrapy
from RiderPlanetScrapper.items import RiderplanetscrapperItem
import time
import re

class MxspiderSpider(scrapy.Spider):
    name = "MXspider"
    allowed_domains = ["www.riderplanet-usa.com"]
    state_names = [ "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New-Hampshire", 
    "New-Jersey", "New-Mexico", "New-York", "North-Carolina", "North-Dakota", "Ohio", "Oklahoma", 
    "Oregon", "Pennsylvania", "Rhode-Island", "South-Carolina", "South-Dakota", "Tennessee", 
    "Texas", "Utah", "Vermont", "Virginia", "Washington", "West-Virginia", "Wisconsin", "Wyoming"
]
    def start_requests(self):
        for state in self.state_names:
            url = "https://www.riderplanet-usa.com/atv/trails/{}_list.htm".format(state)
            yield scrapy.Request(url, self.parse)
    
    
    def parse(self, response):
        tracks = response.css('.clsblockbody.clsrasbody')

        for track in tracks:
            urle = track.css('a.clsrastitle::attr(href)').get()
            track_url = "https://www.riderplanet-usa.com/atv/trails/{}".format(urle)
            yield response.follow(track_url, callback=self.parse_track_page)
            
           

        next_page = response.css('a:contains("Next")::attr(href)').get()
        if next_page is not None:
            next_page_url = "https://www.riderplanet-usa.com/atv/trails/" + next_page
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.log("No next page found.")
        
            

    def parse_track_page(self, response):
        track_item = RiderplanetscrapperItem()

        track_item['Name'] = response.css('div.clsblock.clsmainblock h1::text').get()
        track_item['Other_Names']   = response.css('td.clsp:contains("Other Names") + td p.clsaltnamestext::text').get()
        track_item['Last_Known_Status'] = response.css('td.clsp:contains("Last Known Status") + td *::text').getall()
        track_item['Description'] =  [''.join(response.css(f'p.clsdescript{i}:not(a) ::text').getall()) or "" for i in range(1, 4)]
        track_item['Youtube_Video_Link'] = response.css('iframe.clsyoutubevideo::attr(src)').get()
        track_item['Permit_Required']    = response.css('td.clsp:contains("Permit Required") + td.clsv::text').get()
        track_item['Dates_Open']         = response.css('td.clsp:contains("Dates Open") + td.clsv::text').get()
        track_item['Track_Categories'] = ', '.join(response.css('td.clsv.clsvemp:contains("Permitted"), td.clsv.clsvemp:contains("No Restriction"), td.clsv.clsvemp:contains("Some Areas")').xpath('preceding-sibling::td[@class="clsp"]/text()').getall()) if response.css('td.clsv.clsvemp:contains("Permitted"), td.clsv.clsvemp:contains("No Restriction"), td.clsv.clsvemp:contains("Some Areas")') else 'No amenities with "Permitted," "No Restriction," or "Some Areas" found.'
        track_item['Parking'] = response.css('td.clsp:contains("Parking") + td.clsv::text').get()
        track_item['Entry'] = response.css('td.clsp:contains("Entry") + td.clsv::text').get()
        track_item['Riding'] = response.css('td.clsp:contains("Riding") + td.clsv::text').getall()
        track_item['Camping'] = response.css('td.clsp:contains("Camping") + td.clsv::text').getall()
        track_item['Amenities'] = ', '.join(response.css('td.clsv.clsvemp:contains("On Site")').xpath('preceding-sibling::td[@class="clsp"]/text()').getall()) if response.css('td.clsv.clsvemp:contains("On Site")') else 'No amenities found On Site.'
        track_item['Phone'] = response.css('div.clsblock.clscontactsblock table.clscontacttable td.clsp:contains("Contact Info") + td.clsv::text').re(r'\(\d+\) \d+-\d+')
        track_item['Street']= response.css('td.clsp:contains("Address") + td.clsv::text').get()
        track_item['adress2'] = (re.sub(r'(?<=\S)\s+(?=\S)', ' ', response.css('td.clsv ::text').re_first(r'Take (\S+ \S+)').strip()) if response.css('td.clsv ::text').re_first(r'Take (\S+ \S+)') else '') + ("," if response.css('td.clsv ::text').re_first(r'Take (\S+ \S+)') and response.css('table.clsptable.clscontacttable td.clsv:nth-child(2)::text').re_first(r'(\b\w+,\s\w+\s\d{5}\b)') else "") + (response.css('table.clsptable.clscontacttable td.clsv:nth-child(2)::text').re_first(r'(\b\w+,\s\w+\s\d{5}\b)') if response.css('table.clsptable.clscontacttable td.clsv:nth-child(2)::text').re_first(r'(\b\w+,\s\w+\s\d{5}\b)') else '')
        track_item['Email']     = ', '.join(response.css('div.clsblock.clscontactsblock td.clsv::text').re(r'\S+@\S+')) if response.css('div.clsblock.clscontactsblock td.clsv::text').re(r'\S+@\S+') else 'No emails found.'
        track_item['Website'] = response.css('.clscontacttable a::attr(href)').extract()
        track_item['Photos'] = response.css('img.clsradetailphoto::attr(src)').getall()
        yield(track_item)
        







