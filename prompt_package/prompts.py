from openai import OpenAI
# from data import data_dict
client = OpenAI()

prompt_images = {
    "image_macro": "https://i.kym-cdn.com/photos/images/newsfeed/000/341/941/576.jpg",
    "reaction": "https://i.redd.it/djw0xedkm8z81.gif",
    "exploitable": "https://i.kym-cdn.com/photos/images/newsfeed/001/289/193/ff0.jpg",
    "duality": "https://imgflip.com/s/meme/Drake-Hotline-Bling.jpg",
    "escalating_progression": "https://i.imgflip.com/524q9o.png",
}

allowed_words = ["image macro", "reaction", "exploitable", "duality", "escalating", "progression"]

def find_template(test_image):
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "I will give you an example of a meme template described as 'image_macro'",
          },
          {
            "type": "image_url",
            "image_url": {
              "url": prompt_images["image_macro"],
            },
          },
          {
            "type": "text",
            "text": "I will give you an example of a meme template described as 'reaction'",
          },
          {
            "type": "image_url",
            "image_url": {
              "url": prompt_images["reaction"],
            },
          },
          {
            "type": "text",
            "text": "I will give you an example of a meme template described as 'duality'",
          },
          {
            "type": "image_url",
            "image_url": {
              "url": prompt_images["duality"],
            },
          },
          {
            "type": "text",
            "text": "I will give you an example of a meme template described as 'exploitable'",
          },
          {
            "type": "image_url",
            "image_url": {
              "url": prompt_images["exploitable"],
            },
          },
          {
            "type": "text",
            "text": "I will give you an example of a meme template described as 'escalating progression'",
          },
          {
            "type": "image_url",
            "image_url": {
              "url": prompt_images["escalating_progression"],
            },
          },
          {
            "type": "text",
            "text": "Given the example above, in one word, does the template fall under the category of image macro, reaction, exploitable, duality, or escalating progression? Respond with only the category type",
          },
          {
            "type": "image_url",
            "image_url": {
              "url": test_image,
            },
          },
        ],
      }
    ],
    max_tokens=300,
  )

  return response.choices[0].message.content

def check_equal(pred, gold):
  filtered_output = " ".join(
    word for word in pred.split() if word.lower() in allowed_words
  )

  print(f"pred: {filtered_output}, gold: {gold}")

  try: 
    if filtered_output.lower() == gold.lower():
      return 1
    return 0
  except AttributeError:  # fixing another error where the gold was a float, it's because Jordan didn't label it
    # Handle the case where either filtered_output or gold isn't a string
    print("Error: One of the variables is not a string.")
    return 0

# example = data_dict['A short story'][0],  # expected: escalating progression
# output  = find_template(example[0])
# gold = data_dict['A short story'][1]
# check_equal(output, gold)