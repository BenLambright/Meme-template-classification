from PIL import Image
import imagehash

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