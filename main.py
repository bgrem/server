from PIL import Image, ImageShow
import os
from services.image import ImageService

if __name__ == "__main__":
    input_folder = './input'

    # visualize all images
    image_names = os.listdir(input_folder)
    for image_name in image_names:
        matte_name = image_name.split('.')[0] + '.png'
        image = Image.open(os.path.join(input_folder, image_name))
        matte = ImageService.get_matte(image)
        foreground = ImageService.get_foreground(image, matte)
        ImageShow.show(foreground)
        print(image_name, '\n')
