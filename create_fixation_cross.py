from PIL import Image, ImageDraw

# Define the size of the image
image_size = (256, 256)

# Create a new image with white background
image = Image.new('RGB', image_size, 'white')
draw = ImageDraw.Draw(image)

# Define the size and position of the cross
cross_width = 10
center = (image_size[0] // 2, image_size[1] // 2)
left = (center[0] - cross_width // 2, 0)
right = (center[0] + cross_width // 2, image_size[1])
top = (0, center[1] - cross_width // 2)
bottom = (image_size[0], center[1] + cross_width // 2)

# Draw the vertical part of the cross
draw.rectangle([left, right], fill='black')

# Draw the horizontal part of the cross
draw.rectangle([top, bottom], fill='black')

# Save the image to a file
image.save('fixation_cross.png')
