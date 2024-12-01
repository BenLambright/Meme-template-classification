from data import data_dict
import prompts

memes_names = [meme for meme in data_dict]
correct_labels = 0
total_possible = 0

# testing just a few of the memes
# memes_names = memes_names[:10]

for meme in memes_names:
    image = data_dict[meme][0]
    # had some errors with processing gifv, this his how I handle it:
    if image.endswith("png") or image.endswith("jpg"):  # image.endswith("gif") I might actually be able to do gifs but not now
        print(f"processing {image}")
        gold = data_dict[meme][1]
        pred = prompts.find_template(image)

        correct_labels += prompts.check_equal(pred, gold)
        total_possible += 1
    else:
        print(f"error processing image {image} due to image type")
    
    print(f"accuracy: {correct_labels/total_possible}")


print(correct_labels)
# currently producing an accuracy of 50%

