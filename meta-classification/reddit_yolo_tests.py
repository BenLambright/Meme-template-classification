from ultralytics import YOLO
import torch
import os
from sklearn.metrics import confusion_matrix, accuracy_score
# import matplotlib.pyplot as plt


model = YOLO("/mnt/ssd/home/blambright/meta-classification/runs/classify/train4/weights/best.pt")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

label_dir = 'data/reddit_val'

INCLUDING_NAN = False

### EXAMPLE ####
# # predict for the model
# results = model(["data/reddit_val/Escalating-Progression/7zhbpr5f0vy41.jpg"])

# # example of how to get results
# for result in results:
#     print(f"pred: {result.names[result.probs.top1]}")




### ACTUAL START ###

# get all of the different meta-categories from the data
labels = os.listdir(label_dir)

if INCLUDING_NAN is False:
    labels.remove('nan')

# loop through each meta-category to see what the prediction says
gold_dict = {label : labels.index(label) for label in labels}
print(f'gold_dict: {gold_dict}')
golds = []
preds = []
for label in labels:
    print(f"processing {label}")

    label_path = os.path.join(label_dir, label)
    images = os.listdir(label_path)

    # getting image paths
    image_paths = []
    for image in images:
        image_path = os.path.join(label_path, image)
        if os.path.exists(image_path) and os.path.isfile(image_path) and os.path.getsize(image_path) != 0:
            image_paths.append(image_path)
        else:
            print(f"error in processing {image_path}")
    
    # getting results
    results = model(image_paths)
    for result in results:
        preds.append(result.probs.top1)
        golds.append(gold_dict[label])

# calculate the confusion matrix
heat_map = confusion_matrix(golds, preds)

# Save confusion matrix to a text file
output_file = "confusion_matrix.txt"
with open(output_file, "w") as f:
    for row in heat_map:
        f.write(" ".join(map(str, row)) + "\n")

print(f"Confusion matrix saved to {output_file}")

# calculate the accuracy
print(f"accuracy of the model on our annotated data: {accuracy_score(golds, preds)}")