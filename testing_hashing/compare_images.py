from PIL import Image
import imagehash

# Example of generating a hash for two images that are basically the same
disloyal_boyfriend = imagehash.phash(Image.open('disloyal_boyfriend.jpg'))
distracted_boyfriend = imagehash.phash(Image.open('distracted_boyfriend.jpg'))
similing_jesus = imagehash.phash(Image.open('smiling_jesus.jpg'))

# Compute the similarity
print(f"two images that should be seen as the same: {disloyal_boyfriend - distracted_boyfriend}")  # A distance of 0 means the images are identical
print(f"images that should be seen as different: {disloyal_boyfriend - similing_jesus}")