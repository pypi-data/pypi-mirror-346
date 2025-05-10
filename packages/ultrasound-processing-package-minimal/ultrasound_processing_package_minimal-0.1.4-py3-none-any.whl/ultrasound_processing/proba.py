from transform_back import transform_back
from transform import transform_image
from masking import mask
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import PIL


### Ezeket a paramétereket kell megadni
path = "C:\\Users\\buvr_\\Documents\\Egyetem\\Scientific Python\\Project\\ScPytone_ultrasound_processing\\ultrasound_processing\\data\\cropped_frame_idx_150.png"
alpha_deg = 35
resolution = 50

img = Image.open(path)
plt.imshow(img, cmap="gray")
plt.show()

alpha_rad = alpha_deg/180*np.pi




transformed_image, depth, offset = transform_image(img, alpha_deg, resolution)
plt.imshow(transformed_image, cmap="gray")
plt.show()


masked_image = mask(transformed_image)
plt.imshow(masked_image, cmap="gray")
plt.show()


final_image = transform_back(masked_image, depth, alpha_rad, offset)
plt.imshow(final_image, cmap="gray")
plt.show()


Image.fromarray(transformed_image.astype(np.uint8)).save("transformed.png")
Image.fromarray(masked_image.astype(np.uint8)).save("masked.png")
Image.fromarray(final_image.astype(np.uint8)).save("final.png")
