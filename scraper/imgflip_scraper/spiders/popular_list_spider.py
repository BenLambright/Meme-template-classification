import scrapy
import csv
from pathlib import Path
from functools import reduce
import os

class GenerateSpider(scrapy.Spider):
    name = "popular-memes"
    save_path = os.getcwd()

    def start_requests(self):
        # there are 59 pages of memes
        self.page_number = 1
        self.url = 'https://imgflip.com/memetemplates?sort=top-all-time'
        self.output_path = "all_templates.csv"

        with open(self.output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'meme_page_url', 'image_url'])

        urls = [
            # 'https://api.imgflip.com/popular_meme_ids',
            'https://imgflip.com/memetemplates?sort=top-all-time'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Select all the boxes
        boxes = response.css('div.mt-box')
        rows = []
        
        # scrape the templates from this webpage
        for box in boxes:
            row = [
                box.css('h3.mt-title a::attr(title)').get(), # 'title': 
                response.urljoin(box.css('h3.mt-title a::attr(href)').get()), # 'meme_page_url': 
                response.urljoin(box.css('div.mt-img-wrap img::attr(src)').get()), # 'image_url': 
                # 'caption_generator_url': response.urljoin(box.css('a.mt-caption::attr(href)').get()),
                ]
            rows.append(row)
            print(box.css('h3.mt-title a::attr(title)').get())
        
        # add it to the csv
        with open(self.output_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        # Increment page number and construct the next URL
        self.page_number += 1
        next_page = self.url + f'&page={self.page_number}'

        # Check if there are items on the next page, recursive step
        if boxes:  # Stop if no more items are found
            yield scrapy.Request(next_page, callback=self.parse)

    # def get_memes(self, response, fieldnames):
    #     rows = response.css('#page table tr')[1:]
    #     self.log('rows %s' % rows)
    #     for row in rows:
    #         self.log('row %s' % row)
    #         _row = row.css('td::text').extract()
    #         self.log('_row %s' % _row)
    #         meme = {
    #             fieldnames[0]: _row[0],
    #             fieldnames[1]: _row[1]
    #         }
    #         if len(_row) > 2:
    #             meme[fieldnames[2]] = _row[2]
    #         yield meme

    # def parse(self, response):
    #     # ['ID', 'Name', 'Alternate Text']
    #     print("example resonse hereeeeeeee")
    #     print(response.css('#page mt'))
    #     fieldnames = response.css('#page table tr th::text').extract()

    #     filename = reduce(os.path.join, [self.save_path, "dataset", 'popular_100_memes.csv'])
    #     Path(os.path.dirname(filename)).mkdir(mode=0o655, parents=True, exist_ok=True)

    #     with open(filename, 'w', newline='') as file:
    #         self.log('Created File %s' % filename)
    #         writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    #         writer.writeheader()

    #         for meme in self.get_memes(response, fieldnames):
    #             writer.writerow(meme)
