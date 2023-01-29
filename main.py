import tifffile
from PIL import Image
import os
from tqdm import tqdm

if not os.path.exists("output"):
   os.makedirs("output")

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
        # split image into 512x512 tiles, row by row
        # and save them to "output" directory
        # with name "row_column.jpg"
        for r in tqdm(range(0, h, 512)):
            for c in tqdm(range(0, w, 512), leave=False):
                im1 = image.crop((c, r, c + 512, r + 512))
                im1.save("output/" + image_name + "_" + str(r) + "_" + str(c) + ".jpg",'JPEG', quality=100)
