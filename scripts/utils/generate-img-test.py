from PIL import Image, ImageDraw

# create an img with 4 colors for better visualization of cut images

img = Image.new('RGB', (600, 1200))

draw = ImageDraw.Draw(img)

draw.rectangle([0, 0, 300, 600], fill='black')
draw.rectangle([300, 0, 600, 600], fill='red')
draw.rectangle([0, 600, 300, 1200], fill='green')
draw.rectangle([300, 600, 600, 1200], fill='blue')

img.save('images/rec.jpg')
