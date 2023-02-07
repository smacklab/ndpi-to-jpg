import numpy
import numpy as np
import tifffile
from PIL import Image
import os
from tqdm import tqdm


# if fits criteria, put sample into qualifying folder
# if not, put sample into junk folder (only used for testing)
def save(avgrgb):
    if 170 > avgrgb[0] > 160:
        if 145 > avgrgb[1] > 135:
            if 192 > avgrgb[2] > 185:
                im.save(filename + "_qualified/" + np.array2string(avgrgb) + ".jpg", 'JPEG', quality=100)
                return True
    if 170 < avgrgb[0] or 145 < avgrgb[1] or 192 < avgrgb[2]:
        im.save(filename + "_junk(empty)/" + np.array2string(avgrgb) + ".jpg", 'JPEG', quality=100)
        return False
    im.save(filename + "_junk(crowded)/" + np.array2string(avgrgb) + ".jpg", 'JPEG', quality=100)
    return False

for filename in os.listdir("data"):
    f = os.path.join("data", filename)
    print(f)
    if not os.path.isfile(f) or not f.endswith(".ndpi"):
        continue

    with tifffile.TiffFile(f) as tif:
        image = tif.asarray()
        image = Image.fromarray(image)
        w, h = image.size
        print("Image size: {}x{}".format(w, h))
        image_name = os.path.splitext(filename)[0]

        if not os.path.exists(filename + "_qualified"):
            os.makedirs(filename + "_qualified")

        if not os.path.exists(filename + "_junk(crowded)"):
            os.makedirs(filename + "_junk(crowded)")

        if not os.path.exists(filename + "_junk(empty)"):
            os.makedirs(filename + "_junk(empty)")

        # split image into 512x512 tiles, column by column
        for c in tqdm(range(0, w, 512)):
            for r in tqdm(range(0, h, 512), leave=False):
                im = image.crop((c, r, c + 512, r + 512))

                # retrieve rgb values pixel by pixel
                pixel_values = list(im.getdata())
                pixel_values = numpy.array(pixel_values).reshape((512, 512, 3))
                # calculate mean of red, green, and blue values
                # by averaging each column
                rgb = np.average(np.average(pixel_values, axis=0), axis=0)

                save(rgb)
