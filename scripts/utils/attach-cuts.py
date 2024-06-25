from PIL import Image
import os

dir_path = '../cut-images/images/'

# Get the list of directories
dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

for d in dirs:
    # Get the list of images in the directory
    imgs = [i for i in os.listdir(os.path.join(dir_path, d)) if i.endswith('.jpg')]

    # Sort the images by their names (assuming they're named in the format 'cut_{i}_{j}.jpg')
    imgs.sort(key=lambda x: (int(x.split('_')[2].split('.')[0]), int(x.split('_')[1])))

    # Open the images and add them to a 2D list
    img_matrix = []
    row = []
    current_j = 0
    for img in imgs:
        j = int(img.split('_')[2].split('.')[0])
        if j != current_j:
            img_matrix.append(row)
            row = []
            current_j = j
        row.append(Image.open(os.path.join(dir_path, d, img)))

    img_matrix.append(row)  # Add the last row

    # Calculate the total size of the final image
    total_width = max(len(row) for row in img_matrix) * img_matrix[0][0].width
    total_height = len(img_matrix) * img_matrix[0][0].height

    # Create a new image of the right size
    final_img = Image.new('RGB', (total_width, total_height))

    # Paste each image into the final image
    x_offset = 0
    for row in img_matrix:
        y_offset = 0
        for img in row:
            final_img.paste(img, (x_offset, y_offset))
            y_offset += img.height
        x_offset += img_matrix[0][0].width

    # Save the final image
    final_img.save(os.path.join(dir_path, f'{d}_final.jpg'))