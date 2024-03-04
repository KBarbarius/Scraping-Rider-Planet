#Scraping_Rider_Planet_USA (SCRAPY FRAMEWORK)

The aim of  this project was to scrape 'RiderPlanet USA'. With its copy-paste disabling and Robox.txt features RiderPlanet USA brings unique challenges to any scraping Expert. Fortunately, I was able to utilize my expertise and successfully scraped the entire website. For this project I have used scrapy framework to carry out all activities.

The First step challenge was to Figure out how to inspect the pages in Face of the website anti right or leFt click features. Using 'CNRL+SHIFT+I' I was able to overcome the challenge.

The second step was to identify the correct CSS selectors for scraping, which I did select as seen in MXspider.py file. The CSS selector I selected were speciFic to the data content I needed to scrape, this specification allowed me to avoid mixing contents. For instance, "track_item['Last_Known_Status'] = response.css('td.clsp:contains("Last Known Status") + td *::text').getall()" was used to collect 'last known Status' data contents in the webpages on the website. My specification that the data to be collected must come rom a named named 'clsp' and contains the words 'Last Known Status' enabled collection of right inormation in a well organised manner seen in the son file.

The third step was to integrated rotating proxies and web browsers so that the website does not block us, which I successfully did and integrated all the needed proxies and fake browser headers into the settings and middlewares of my scrapper. Please see the middlewares and setting for this implementation. I used about 500 rotating proxies for this project. 

After successfully implementating my scrapper code, the scrapper was able to sucessully scrape all 1756 motocrross tracks infomation from the website in a systematcally arranged format shown in 'RiderPlanet4.json'

I then converted the json to excel file excel, to faciliatate further processing of the data. I used the this website to convert it to excel file: https://cdkm.com/json-to-xlsx

