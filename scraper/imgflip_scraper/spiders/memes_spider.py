from pathlib import Path
import scrapy
import csv
import string
import os
from functools import reduce
import logging
from collections import defaultdict
import json

output_dir = "dataset/missing_templates"
template_path = "missing_templates.csv"


class MemesSpider(scrapy.Spider):
    save_path = os.getcwd()
    name = "memes"
    template_ids = dict()
    memes = defaultdict(list)

    # def get_template_urls(self):
    #     csv_filename = reduce(os.path.join, [self.save_path, "dataset", 'popular_100_memes.csv'])
    #     Path(os.path.dirname(csv_filename)).mkdir(mode=0o655, parents=True, exist_ok=True)
    #     with open(csv_filename) as csv_file:
    #         reader = csv.reader(csv_file, delimiter=',')
    #         line = 0
    #         for row in reader:
    #             line += 1
    #             if line == 1:
    #                 self.log('HEADERS\n%s %s %s' % (row[0], row[1], row[2]))
    #             else:
    #                 # self.log('%s %s %s' % (row[0], row[1], row[2]))
    #                 # delete punctuations
    #                 table = str.maketrans(dict.fromkeys(string.punctuation))
    #                 title = row[1].translate(table)
    #                 title = "-".join(title.split())
    #                 self.template_ids[title] = row[0]
    #                 yield 'https://imgflip.com/meme/' + title  # join words with -
    #                 #     'https://imgflip.com/meme/Distracted-Boyfriend',

    def get_template_urls(self):
        csv_filename = reduce(os.path.join, [self.save_path, template_path])
        Path(os.path.dirname(csv_filename)).mkdir(mode=0o655, parents=True, exist_ok=True)
        with open(csv_filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            line = 0
            for row in reader:
                line += 1
                if line == 1:
                    self.log('HEADERS\n%s %s %s' % (row[0], row[1], row[2]))
                else:
                    # self.log('%s %s %s' % (row[0], row[1], row[2]))
                    # delete punctuations
                    # table = str.maketrans(dict.fromkeys(string.punctuation))
                    # title = row[1].translate(table)
                    # title = "-".join(title.split())
                    # self.template_ids[title] = row[0]
                    # yield 'https://imgflip.com/meme/' + title  # join words with -
                    # #     'https://imgflip.com/meme/Distracted-Boyfriend',
                    yield row[1]  # the meme page url

    def start_requests(self):
        # count = 0
        urls = self.get_template_urls()
        for url in urls:
            # count += 1
            # if count > 1:
            #     break
            self.log(f"Parsing meme: {url}", level=logging.INFO)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1].split('?')[0]
        # id = self.template_ids[page]
        urls = response.css('#base-left .base-unit-title a::attr(href)').extract()
        print(f"{page} and {urls}")
        for i in urls:
            url = 'https://imgflip.com' + i
            yield scrapy.Request(url=url, callback=self.parse_meme)

        # this is the stuff to save memes from multiple pages
        try:
            if len(self.memes[page]) < 100:
                next_page = 'https://imgflip.com' + response.css('.pager .pager-next::attr(href)').extract()[0]
                yield scrapy.Request(url=next_page, callback=self.parse)
        except:
            pass

        if len(self.memes[page]) >= 100:
            print(f"{page} now has {len(self.memes[page])} memes stored")

        self.save_meme(page)
        return

    def parse_meme(self, response):
        # self.log(f"Processing meme page: {response.url}", level=logging.INFO)
        if response.css('.img-added-imgs-msg'):
            return
        title = response.css('#img-secondary .recaption::attr(href)').extract()[0].split('/')[-1]

        meme = dict()
        try:
            img_votes = response.css('.img-info .img-votes::text').extract()[0].split()[0]
        except:
            img_votes = 0
        if len(response.css('#im::attr(src)').extract()) == 0:
            meme['url'] = 'https:' + response.css('div#img-wrap video::attr(data-src)').get()
        else:
            meme['url'] = 'https:' + response.css('#im::attr(src)').extract()[0]
        meme['post'] = response.url
        meme['metadata'] = {
            'views': response.css('.img-info .img-views::text').extract()[0].split()[0],
            'img-votes': img_votes,
            'title': response.css('#img-title::text').extract()[0],
            'author': next(iter(response.css('.img-info .u-username::text').extract() or ''), None)
        }
        meme_title = response.css('.img-title::text').extract()
        if meme_title:
            meme['metadata']['title'] = response.css('.img-title::text').extract()[0]
        meme_author = response.css('.img-title::text').extract()
        if meme_author:
            meme['metadata']['author'] = next(iter(response.css('.img-info .u-username::text').extract() or ''), None)
        try:
            meme['boxes'] = [s.strip() for s in response.css('.img-desc::text').extract()[1].split(';')]
            self.memes[title].append(meme)
        except:
            self.log('Empty meme')

    def save_memes(self):
        for meme_name, lst in self.memes.items():
            filename = meme_name + '.json'
            path = reduce(os.path.join, [self.save_path, "dataset", "memes", filename])
            Path(os.path.dirname(path)).mkdir(mode=0o655, parents=True, exist_ok=True)

            self.log(meme_name + ' - ' + str(len(lst)), level=logging.INFO)

            with open(path, 'w+') as file:
                json.dump(lst, file, indent=2)

    # def save_meme(self, meme_name):
    #     print("saving meme")
    #     lst = self.memes[meme_name]
    #     filename = meme_name + '.json'
    #     path = reduce(os.path.join, [self.save_path, "dataset", "memes", filename])
    #     Path(os.path.dirname(path)).mkdir(mode=0o655, parents=True, exist_ok=True)

    #     self.log(meme_name + ' - ' + str(len(lst)), level=logging.INFO)

    #     with open(path, 'w+') as file:
    #         json.dump(lst, file, indent=2)
    #     del self.memes[meme_name]

    def save_meme(self, meme_name):
        # print("saving memes")

        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        for meme in self.memes:
            # print(f"saving meme {meme}")
            # Convert the defaultdict to a JSON string
            json_data = json.dumps(self.memes[meme], indent=2)

            # Save to a file
            output_path = os.path.join(output_dir, meme)

            with open(output_path, "w") as jsonfile:
                jsonfile.write(json_data)