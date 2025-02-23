import pyray

BASE_IMG_PATH = 'assets/images/'
COLOR_KEY = (255, 174, 201, 255)

def load_image_to_texture(path):
    img = pyray.load_image(BASE_IMG_PATH + path)  # Loads an image
    pyray.image_color_replace(img, COLOR_KEY, pyray.BLANK)  # Sets colorkey
    texture = pyray.load_texture_from_image(img)  # Creates a texture from the image
    pyray.unload_image(img)  # Unloads the image
    return texture