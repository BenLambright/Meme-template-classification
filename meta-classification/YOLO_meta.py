from ultralytics import YOLO
import torch

# Load a model and device
model = YOLO("yolo11n-cls.pt")
# model = YOLO("runs/classify/train35/weights/best.pt")  # load a pretrained model (recommended for training)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# validate the model
# model.val()

# predict for the model
# results = model(["/mnt/ssd/home/blambright/scraper_tests/dataset/final_dataset/template_training_data_reddit/val/naruto-thumbs-up/tsqn8y36s3xd1.png"])

# Fine-tune the model
# imgsz=640 downsizes all images to this size, which I think is reasonable for our data
results = model.train(data='data', 
                     epochs=15, 
                     patience=2, 
                     imgsz=640,
                     optimizer="AdamW",
                     lr0=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, box=7.5, cls=0.5, dfl=1.5
, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, bgr=0.0, mosaic=1.0, mixup=0.0, 
copy_paste=0.0)
