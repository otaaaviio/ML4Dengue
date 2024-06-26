from PIL import Image
import os
import xml.etree.ElementTree as ET

WIDTH_CUT = 300
HEIGHT_CUT = 600
RETURN_CUT = 100


# Function to adjust the annotations of the images
def adjust_annotations(xml_file, cut_x, cut_y):
    # load the xml file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # iterate over the xml file and adjust the coordinates of the ellipses
    for image in root.iter('image'):
        for ellipse in image.iter('ellipse'):
            # adjust the coordinates of the ellipse
            cx = float(ellipse.get('cx')) - cut_x
            cy = float(ellipse.get('cy')) - cut_y
            ellipse.set('cx', str(cx))
            ellipse.set('cy', str(cy))

    # save the new xml file
    tree.write(xml_file)


# Function to cut the images and send cuts to adjust_annotations()
def cut_images(entries, img_dir_path):
    # define the size of the cuts and return size
    width_cut = WIDTH_CUT
    height_cut = HEIGHT_CUT
    return_cut = RETURN_CUT

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

                    # adjust the annotations of the image
                    xml_file = os.path.join(img_dir_path, img.split(".")[0] + ".xml")
                    adjust_annotations(xml_file, top_left, bot_left)

            print('They were made', num_cuts_width * num_cuts_height, 'cuts in the image', img, 'and saved in the directory', new_dir_path)


def main():
    # define the path of the directory of the images
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dir, 'images')

    images = [file for file in os.listdir(directory) if file.endswith('.jpg')]

    # get the prefix names of the images for the annotations
    prefix_names = [os.path.splitext(file)[0] for file in images]

    # Select only images with annotations
    selected = [name for name in prefix_names if os.path.exists(os.path.join(directory, name + '.xml'))]

    # cut the images and adjust the annotations
    cut_images(selected, directory)


if __name__ == "__main__":
    main()
