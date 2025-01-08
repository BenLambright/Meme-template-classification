import os
import json
import requests
import csv

def open_image_link(image_url, file_path):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open the file in binary write mode and save the content
            with open(file_path, 'wb') as file:
                file.write(response.content)
            # print(f"Image downloaded successfully and saved to {file_path}")
        else:
            print(f"Failed to download image. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_memes(template_path, image_dir):
    with open(template_path, "r") as file:
        memes = json.load(file)
        # memes = memes[:5]
        for meme in memes:
            # image_name = meme['metadata']['title'].replace(" ", "_")
            image_name = meme['url'].split("/")[-1]  # getting the last part of the url as the jpg, i.e. 9bdpc9.jpg
            output_path = os.path.join(image_dir, image_name)
            open_image_link(meme['url'], output_path)

def download_model_data():
    data_dir = "dataset/missing_templates"
    output_dir = "dataset/reddit_images"

    templates = os.listdir(data_dir)

    for template in templates:
        print(f"uploading {template} memes")
        template_path = os.path.join(data_dir, template)  # input
        with open(template_path, 'r') as file:
            memes = json.load(file)
            if len(memes) != 0:
                image_dir = os.path.join(output_dir, template)  # output
                if os.path.exists(image_dir) is False:
                    os.mkdir(image_dir)

                download_memes(template_path, image_dir)
            else:
                print(f'{template} was empty')

download_model_data()

# def download_template_data():
#     template_path = 'dataset/all_templates.csv'
#     template_dir = 'templates'
#     if os.path.exists(template_dir) is False:
#             os.mkdir(template_dir)

#     # accessing the image link
#     links = {}
#     with open(template_path, mode='r', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)

#         # Skip the header row (if there is one)
#         next(csv_reader, None)

#         # loop through each row to get the image link
#         for row in csv_reader:
#             meme_name = row[0].replace(" ", "-")  # replacing spaces
#             meme_name = meme_name.replace("/", "")  # removing / so that it doens't get confused when producing the output
#             links[meme_name] = row[2]

#     for name, link in links.items():
#         open_image_link(link, os.path.join(template_dir, f"{name}.jpg"))
#     # open_image_link(links['Two-Buttons-Meme'], os.path.join(template_dir, 'Two-Buttons-Meme.jpg'))
#     print("finished")

# download_template_data()


# print(os.path.exists(image_dir))