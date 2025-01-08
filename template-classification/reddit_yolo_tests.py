from ultralytics import YOLO
import torch
import os
from sklearn.metrics import confusion_matrix, accuracy_score
# import matplotlib.pyplot as plt

# parameters for whether you're using this for meta or template classification
meta_params = {"model": "/mnt/ssd/home/blambright/meta-classification/runs/classify/train4/weights/best.pt",
                   "label_dir": 'data/reddit_val'}
template_params = {"model": "runs/classify/train35/weights/best.pt",
                   "label_dir": "/mnt/ssd/home/blambright/scraper_tests/dataset/final_dataset/template_training_data_reddit/reddit_val"}
meta_semi_supervised = {"model": "runs/classify/train10/weights/best.pt",
                        "label_dir": ""}


model = YOLO(template_params["model"])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

label_dir = template_params["label_dir"]

INCLUDING_NAN = False

### EXAMPLE ####
def example():
    # predict for the model
    results = model(["dataset/final_dataset/template_training_data_reddit/reddit_val/ron-swanson-mental-illness/bovmw1pglyvd1.png"])

    # example of how to get results
    for result in results:
        print(f"pred: {result.names[result.probs.top1]}")

# example()




### ACTUAL START ###

def getting_best():
    ...

def run():
    # get all of the different meta-categories from the data
    labels = os.listdir(label_dir)

    if INCLUDING_NAN is False:
        labels.remove('nan')

    # loop through each meta-category to see what the prediction says
    gold_dict = {label : labels.index(label) for label in labels}  # might not need this anymore, using strings instead now
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
        if len(image_paths) != 0:
            results = model(image_paths)
        else:
            print(f"{label_path} is empty, likely due to image processing errors")
        for result in results:
            # changed from doing the index, now we're doing the strings
            preds.append(result.names[result.probs.top1]) 
            golds.append(label)

    # calculate the confusion matrix
    heat_map = confusion_matrix(golds, preds)

    # Save confusion matrix to a text file
    output_file = "confusion_matrix.txt"
    with open(output_file, "w") as f:
        for row in heat_map:
            f.write(" ".join(map(str, row)) + "\n")

    print(f"Confusion matrix saved to {output_file}")

    print(golds)
    print(preds)

    # calculate the accuracy
    print(f"accuracy of the model on our annotated data: {accuracy_score(golds, preds)}")

run()