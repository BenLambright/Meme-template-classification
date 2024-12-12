from PIL import Image
import imagehash
import requests
import pandas as pd
import json

# Example of generating a hash for two images that are basically the same
disloyal_boyfriend = imagehash.phash(Image.open('disloyal_boyfriend.jpg'))
distracted_boyfriend = imagehash.phash(Image.open('distracted_boyfriend.jpg'))
similing_jesus = imagehash.phash(Image.open('smiling_jesus.jpg'))

# Compute the similarity
print(f"two images that should be seen as the same: {disloyal_boyfriend - distracted_boyfriend}")  # A distance of 0 means the images are identical
print(f"images that should be seen as different: {disloyal_boyfriend - similing_jesus}")


# trying it but with a pretrained ResNet
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50

# Load pre-trained model
model = resnet50(pretrained=True)
model.eval()

# Preprocess and extract features
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
disloyal_boyfriend_tensor = transform(Image.open('disloyal_boyfriend.jpg')).unsqueeze(0)
disloyal_boyfriend_features = model(disloyal_boyfriend_tensor)
distracted_boyfriend_tensor = transform(Image.open('distracted_boyfriend.jpg')).unsqueeze(0)
distracted_boyfriend_features = model(distracted_boyfriend_tensor)
similing_jesus_tensor = transform(Image.open('smiling_jesus.jpg')).unsqueeze(0)
smiling_jesus_features = model(similing_jesus_tensor)

# Compute similarity using cosine similarity
cos_sim1 = torch.nn.functional.cosine_similarity(disloyal_boyfriend_features, distracted_boyfriend_features)
print(f"cosine sim between the two same templates: {cos_sim1}")
cos_sim2 = torch.nn.functional.cosine_similarity(disloyal_boyfriend_features, smiling_jesus_features)
print(f"cosine sim between the two different templates: {cos_sim2}")

template_df = pd.read_csv('all_templates.csv')
# threshold of similarity:
SIM_THRESHOLD = 0.75
similar_pairs = {}
for ind in range(len(template_df)):
    curr_image = template_df.loc[ind]['meme_page_url'].split('/')[-1] + '.jpg'
    # make tuple of information for easier manual comparison later
    curr_tuple = (ind, curr_image, template_df.loc[ind]['image_url'])
    # embed first image
    curr_image_features = model(transform(Image.open(curr_image)).unsqueeze(0))
    # create list to populate w memes similar to current meme
    current_similar = []
    for next_ind in range(ind + 1, len(template_df)):
        next_image = template_df.loc[next_ind]['meme_page_url'].split('/')[-1] + '.jpg'
        # tuple for next_image
        next_tuple = (next_ind, next_image, template_df.loc[next_ind]['image_url'])
        # embed next image
        next_image_features = model(transform(Image.open(next_image)).unsqueeze(0))
        # calculate similarity and compare to threshold
        similarity = torch.nn.functional.cosine_similarity(curr_image_features, next_image_features)
        print(similarity)
        if similarity >= SIM_THRESHOLD:
            current_similar.append(next_tuple)
    # add similarities to dictionary
    similar_pairs[curr_tuple] = current_similar

# output to text file for human readability

with open('similar_pairs.txt', 'w') as file:
    for key in similar_pairs:
        if len(similar_pairs[key]) > 0:
            file.write(str(key) + '\n')
            for tuple in similar_pairs[key]:
                file.write('\t' + str(tuple) + '\n')
print(similar_pairs)

