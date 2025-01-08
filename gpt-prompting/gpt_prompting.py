from openai import OpenAI
import pandas as pd

imgflip_data = 'adjudicated_all_trunc.csv'
template_data = 'adjudicated_templates_trunc.csv'

def prompt_just_text(url, gold):
  client = OpenAI()

  response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
          # I got all of these images from the top rated example of each type that I could find on imgflip
          {
            "type": "text", "text": "You will be given a list explanations for image macro, reacion, escalating preogression, duality, and exploitable memes, and afterwards you will have to classify them"
          },
          {
              "type": "text", "text": "Image macros can be thought of as memes for which the setup of the joke is given by the image, and the text fills in the details and punchline. For our purposes, we consider image macros as consisting of a single image. The most typical presentation of these memes involves a picture of some kind of entity (often an animal or person) with white text in impact font on the top and bottom of the image.",
          },
          {
              "type": "text", "text": "Reaction images are in a sense an inversion of image macros. Instead of the image setting up the joke and the text filling in the punchline, the joke is set up by a text caption (almost always separated from the image portion) and then the punchline is the image. The images in these memes are usually of people emoting or reacting in some fashion, and the humor often derives in part from the fact that the text caption completely recontextualizes the image from its origin.",
          },
          {
              "type": "text", "text": "Escalating progression memes are those that express a reaction to points sampled along a continuum of context. Unlike in duality where the situations are related in terms of opposing each other (e.g good thing vs. bad thing), with escalating progression there is an intensification between each state (e.g good thing vs. better thing vs. best thing). Typically these memes have at least 3 sets of image-context pairs, but it's not required as long as there is an obvious sense of continuity between the contexts. It doesn't have to be 3+ images, like it can still be one, the difference is that it represents something escalating, rather than a good or bad. It has a continuum moving in a consistent intensifyingly humorous direction.",
          },
          {
              "type": "text", "text": "A meme exhibiting duality is one that compares two (or more) situations or contexts that are related across some dimension, usually in opposition to each other. The typical components of a duality meme are a set of discrete contexts and a set of images (most often variations on the same image) that visualize the relationship between the contexts. A common format is a '4-panel' layout in which two pairs of contexts and and images are stacked vertically.",
          },
          {
              "type": "text", "text": "An exploitable is a meme in which an existing image (such as a comic, or one or more scenes from a movie) of some sort is augmented by adding and/or replacing some set of things (like dialogue, characters, labels etc.) to tell a joke. The idea is that there is some extant structure inside an image that is 'exploited' using text or additional pictures within the bounds of the original image (unlike a caption in a reaction image, which is typically outside it).",
          },
        # {"type": "text", "text": "Given the desriptions of memes from before, how would you describe the following meme? Select a response for the following list and only use the words from this list: image macro, reacion, escalating preogression, duality, exploitable, or none."},
        {"type": "text", "text": "Given the desriptions of memes from before, how would you describe the following meme? Select a response for the following list and only use the words from this list: image macro, reacion, escalating preogression, duality, or exploitable."},
        {"type": "text", "text": "Only output the template class you decided"},
        {
          "type": "image_url",
          "image_url": {
            "url": url,
          },
        },
      ],
    }
  ],
  max_tokens=20,
  )

  pred = response.choices[0].message.content
  print(f'predicted: {pred} vs gold: {gold}')
  if pred == gold:
    return True
  else:
    return False


def prompt_just_images(url, gold):
  client = OpenAI()

  response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
          # I got all of these images from the top rated example of each type that I could find on imgflip
          {
            "type": "text", "text": "You will be given a list of example images for image macro, reacion, escalating preogression, duality, and exploitable memes, and afterwards you will have to classify them"
          },
          {
              "type": "text", "text": "You will be given a list explanations for image macro, reacion, escalating preogression, duality, and exploitable memes, and afterwards you will have to classify them",
              "image_url": {
                  "url": "https://imgflip.com/i/3yhgyo",
          },
          },
          {
              "type": "text", "text": "Here is an example of an reaction: ",
              "image_url": {
                  "url": "https://i.imgflip.com/4zv2v9.jpg",
          },
          },
          {
              "type": "text", "text": "Here is an example of an escalating progression: ",
              "image_url": {
                  "url": "https://i.imgflip.com/4iyi3q.jpg",
          },
          },
          {
              "type": "text", "text": "Here is an example of an duality: ",
              "image_url": {
                  "url": "https://i.imgflip.com/4izfsm.jpg",
          },
          },
          {
              "type": "text", "text": "Here is an example of an exploitable: ",
              "image_url": {
                  "url": "https://i.imgflip.com/3fys88.jpg",
          },
          },
        # {"type": "text", "text": "Given the desriptions of memes from before, how would you describe the following meme? Select a response for the following list and only use the words from this list: image macro, reacion, escalating preogression, duality, exploitable, or none."},
        {"type": "text", "text": "Given the desriptions of memes from before, how would you describe the following meme? Select a response for the following list and only use the words from this list: image macro, reacion, escalating preogression, duality, or exploitable."},
        {"type": "text", "text": "Only output the template class you decided"},
        {
          "type": "image_url",
          "image_url": {
            "url": url,
          },
        },
      ],
    }
  ],
  max_tokens=20,
  )

  pred = response.choices[0].message.content
  print(f'predicted: {pred} vs gold: {gold}')
  if pred == gold:
    return True
  else:
    return False


def prompt_images_and_text(url, gold):
  client = OpenAI()

  response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
          # I got all of these images from the top rated example of each type that I could find on imgflip
          {
            "type": "text", "text": "You will be given a list of example images for image macro, reacion, escalating preogression, duality, and exploitable memes, and afterwards you will have to classify them"
          },
          {
              "type": "text", "text": "Image macros can be thought of as memes for which the setup of the joke is given by the image, and the text fills in the details and punchline. For our purposes, we consider image macros as consisting of a single image. The most typical presentation of these memes involves a picture of some kind of entity (often an animal or person) with white text in impact font on the top and bottom of the image.",
              "type": "text", "text": "Here is an example of an image macro, where you have the classic text on top and below, where the entire joke could be understood without the image: ",
              "image_url": {
                  "url": "https://imgflip.com/i/3yhgyo",
          },
          },
          {
              "type": "text", "text": "Reaction images are in a sense an inversion of image macros. Instead of the image setting up the joke and the text filling in the punchline, the joke is set up by a text caption (almost always separated from the image portion) and then the punchline is the image. The images in these memes are usually of people emoting or reacting in some fashion, and the humor often derives in part from the fact that the text caption completely recontextualizes the image from its origin.",
              "type": "text", "text": "Here is an example of an reaction, where the monkey looks awkwardly in reaction to the text which follows a 'me-when' style: ",
              "image_url": {
                  "url": "https://i.imgflip.com/4zv2v9.jpg",
          },
          },
          {
              "type": "text", "text": "Escalating progression memes are those that express a reaction to points sampled along a continuum of context. Unlike in duality where the situations are related in terms of opposing each other (e.g good thing vs. bad thing), with escalating progression there is an intensification between each state (e.g good thing vs. better thing vs. best thing). Typically these memes have at least 3 sets of image-context pairs, but it's not required as long as there is an obvious sense of continuity between the contexts. It doesn't have to be 3+ images, like it can still be one, the difference is that it represents something escalating, rather than a good or bad. It has a continuum moving in a consistent intensifyingly humorous direction.",
              "type": "text", "text": "Here is an example of an escalating progression, where the brain gets bigger and bigger as the text describes something smarter and smarter: ",
              "image_url": {
                  "url": "https://i.imgflip.com/4iyi3q.jpg",
          },
          },
          {
              "type": "text", "text": "A meme exhibiting duality is one that compares two (or more) situations or contexts that are related across some dimension, usually in opposition to each other. The typical components of a duality meme are a set of discrete contexts and a set of images (most often variations on the same image) that visualize the relationship between the contexts. A common format is a '4-panel' layout in which two pairs of contexts and and images are stacked vertically.",
              "type": "text", "text": "Here is an example of an duality, where drake at first thinks it's bad, but then thinks it's good: ",
              "image_url": {
                  "url": "https://i.imgflip.com/4izfsm.jpg",
          },
          },
          {
              "type": "text", "text": "An exploitable is a meme in which an existing image (such as a comic, or one or more scenes from a movie) of some sort is augmented by adding and/or replacing some set of things (like dialogue, characters, labels etc.) to tell a joke. The idea is that there is some extant structure inside an image that is 'exploited' using text or additional pictures within the bounds of the original image (unlike a caption in a reaction image, which is typically outside it).",
              "type": "text", "text": "Here is an example of an exploitable, where the text is overlayed over all of the people, representing who they are in the context of the joke: ",
              "image_url": {
                  "url": "https://i.imgflip.com/3fys88.jpg",
          },
          },
        # {"type": "text", "text": "Given the desriptions of memes from before, how would you describe the following meme? Select a response for the following list and only use the words from this list: image macro, reacion, escalating preogression, duality, exploitable, or none."},
        {"type": "text", "text": "Given the desriptions of memes from before, how would you describe the following meme? Select a response for the following list and only use the words from this list: image macro, reacion, escalating preogression, duality, or exploitable."},
        {"type": "text", "text": "Only output the template class you decided"},
        {
          "type": "image_url",
          "image_url": {
            "url": url,
          },
        },
      ],
    }
  ],
  max_tokens=20,
  )

  pred = response.choices[0].message.content
  print(f'predicted: {pred} vs gold: {gold}')
  if pred == gold:
    return True
  else:
    return False

def prompt(prompter, data):
  score = []

  for index, row in data.iterrows():
    # processing gold
    if pd.isnull(row['Ontology']):
      gold = 'none'
    else:
      gold = row['Ontology']
    gold = gold.lower()

    # processing url
    url = row['image_url']
    if url.endswith(('png', 'jpeg', 'jpg')):
      # calcing
      if prompter(url, gold):
        score.append(1)
      else:
        score.append(0)
  
  return score

def train():
  imgflip = pd.read_csv(imgflip_data)
  templates = pd.read_csv(template_data)

  print('testing imgflip data')
  imgflip_score = prompt(prompt_just_text, imgflip)
  print('testing template data')
  template_score = prompt(prompt_just_text, templates)

  total = len(imgflip_score) + len(template_score)
  correct = sum(imgflip_score) + sum(template_score)

  print(f"accuracy: {correct/total} across {total} runs")

  return correct/total

text_accuracy = train()
print("this is text!")

# print(prompt_images_and_text('https://i.imgflip.com/3fys88.jpg', 'exploitable'))
# print(prompt_just_text('https://i.imgflip.com/3fys88.jpg', 'exploitable'))
# print(prompt_just_images('https://i.imgflip.com/3fys88.jpg', 'exploitable'))
