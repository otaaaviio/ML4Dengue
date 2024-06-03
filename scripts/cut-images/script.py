from PIL import Image
import os

img_dir_path = './images/'

# define the size of the cuts and return size
width_cut = 300
height_cut = 600
return_cut = 100

entries = os.listdir(img_dir_path)

# verify if the files in the directory are images
imgs = [entry for entry in entries if os.path.isfile(os.path.join(img_dir_path, entry))]

# check if there are images in the directory
if len(imgs) == 0:
    print("No images found in the directory")
    exit()

for img in imgs:
    img_path = os.path.join(img_dir_path, img)
    with Image.open(img_path) as image:
        width, height = image.size

        # get the number of cuts in width and height and add 1 to guarantee that will have cuts for all the image
        num_cuts_width = (width // width_cut) + 1
        num_cuts_height = (height // height_cut) + 1

        #  make a new directory to save the cuts of the image
        new_dir_path = os.path.join(img_dir_path, img.split(".")[0])
        os.makedirs(new_dir_path, exist_ok=True)

        # init the cuts
        for i in range(num_cuts_width):
            for j in range(num_cuts_height):
                # only the cuts that started in the left lateral border were maintained, while the cuts showed a return
                if i == 0:
                    top_left = i * width_cut
                    top_right = (i + 1) * width_cut
                else:
                    top_left = (i * width_cut) - return_cut
                    top_right = ((i + 1) * width_cut) - return_cut

                # only the cuts that started in the top lateral border were maintained, while the cuts showed a return
                if j == 0:
                    bot_left = j * height_cut
                    bot_right = (j + 1) * height_cut
                else:
                    bot_left = (j * height_cut) - return_cut
                    bot_right = ((j + 1) * height_cut) - return_cut

                # keeps cuts in bounds of the image and returns the cut if it goes out of bounds
                if top_right > width:
                    top_right = width
                    top_left = top_right - width_cut
                if bot_right > height:
                    bot_right = height
                    bot_left = bot_right - height_cut

                # crop and save the cut in created directory of the image
                im_cropped = image.crop((top_left, bot_left, top_right, bot_right))
                im_cropped.save(os.path.join(new_dir_path, f"cut_{i}_{j}.jpg"))

        print('They were made', num_cuts_width * num_cuts_height, 'cuts in the image', img, 'and saved in the directory', new_dir_path)
