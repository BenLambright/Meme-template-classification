import os
from functools import reduce
import json
from os import listdir
from os.path import isfile, join
from collections import defaultdict

# if __name__ == '__main__':
#     memes = defaultdict(int)

#     memes_path = reduce(os.path.join, [os.getcwd(), "dataset", 'memes'])
#     files = (f for f in listdir(memes_path) if isfile(join(memes_path, f)))

#     for file in files:
#         file_path = reduce(os.path.join, [memes_path, file])
#         with open(file_path) as json_file:
#             data = json.load(json_file)
#             memes[file] = len(data)
#     statistics_path = reduce(os.path.join, [os.getcwd(), "dataset", 'statistics.json'])

#     with open(statistics_path, 'w+') as result_file:
#         json.dump({
#             'total': reduce(lambda x, value: value + x, memes.values(), 0),
#             'memes': memes
#         }, result_file, indent=2)

dir_path = "dataset/memes"

if __name__ == '__main__':
    meme_pages = os.listdir(dir_path)

    total_count = 0
    templates = []  # store the names of all the templates
    
    for meme in meme_pages:
        templates.append(meme)
        with open(os.path.join(dir_path, meme), "r") as file:
            data = json.load(file)
            total_count += len(data)

    print(f"We've scraped {total_count} memes")

    # creating the txt file of our classes
    with open("templates.txt", "w") as file:
        file.writelines(template + "\n" for template in templates)

    # ensuring that our test dataset has files for each template
    # for template in templates:
    #     template_path = os.path.join("dataset/images", template)
    #     os.makedirs(template_path, exist_ok=True)