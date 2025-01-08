from ultralytics import YOLO
import torch
import splitfolders


# WARNING: THERE IS SOMETHING WRONG WITH THIS THAT IS NOT LETTING IT ACCEPT DIRS FOR DATA PATHS WHEN TRAINING
# For now, run test.py instead

def load_model(pretrain_path):
    # Load a model and device
    # for metas: "/mnt/ssd/home/blambright/meta-classification/runs/classify/train4/weights/best.pt"
    # for templates: "runs/classify/train35/weights/best.pt"
    model = YOLO(pretrain_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return model

def val(model):
    # validate the model
    model.val()

def predict(model, data_path):
    # predict for the model
    # example: "/mnt/ssd/home/blambright/scraper_tests/dataset/final_dataset/template_training_data_reddit/val/naruto-thumbs-up/tsqn8y36s3xd1.png"
    results = model([data_path])
    return results

def train(model, dataset_path):
    # Fine-tune the model
    # imgsz=640 downsizes all images to this size, which I think is reasonable for our data
    results = model.train(data=dataset_path, 
                         epochs=15, 
                         patience=2, 
                         imgsz=640,
                         optimizer="AdamW",
                         lr0=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, box=7.5, cls=0.5, dfl=1.5
    , hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, bgr=0.0, mosaic=1.0, mixup=0.0, 
    copy_paste=0.0)
    return results

def split_folders(input_folder, output_folder, ratio):
    # # example:
    # input_folder = "dataset/images"
    # output_folder = "dataset/template_training_data_reddit"  # Where the split data will be saved

    # If you want train (80%), val (10%), and test (10%), then ratio = (.9, .05, .05)
    splitfolders.ratio(input_folder, output=output_folder, seed=42, ratio=ratio, group_prefix=None)


split_folders('dataset/reddit_images', 'dataset/final_reddit_test', (.85, .15))

# model = load_model('runs/classify/train10/weights/best.pt')
# # train(model, 'reddit_data')
# val(model)

