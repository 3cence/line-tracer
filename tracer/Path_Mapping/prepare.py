from PIL import Image
import numpy as np


def highlight_dark(array, limit):
    output = array.copy()
    for y, item in enumerate(array):
        for x, obj in enumerate(item):
            arraylet = array[y][x]

            greyscale_value = (arraylet[0] * .3 + arraylet[1] * .59 + arraylet[2] * .11) / 3 + 30
            if greyscale_value > 255:
                greyscale_value = 255
            if greyscale_value < limit:
                greyscale_value = 255
            else:
                greyscale_value = 0
            for v, rgb_val in enumerate(output[y][x]):
                output[y][x][v] = greyscale_value
                if output[y][x].size == 4:
                    output[y][x][3] = 255
    return output


def generate_binary_text(fp, array):
    file = open(fp, "w")
    for x, x_array in enumerate(array):
        for y, y_array in enumerate(x_array):
            if array[x][y][0] > 128:
                file.write("1")
            else:
                file.write("0")
        file.write("\n")
    file.close()


def ready_for_training(name, resize_res=100):
    try:
        with Image.open(f"training_images_in/{name}") as i:
            i = i.resize((resize_res, resize_res))
            im = np.asarray(i)
            oimr = highlight_dark(im, 60)
            oim = Image.fromarray(oimr)
            generate_binary_text(f"training_images_out/{name.split('.')[0]}.txt", oimr)
            oim.save(f"training_images_out/{name.split('.')[0]}.png", "PNG")
    except FileNotFoundError:
        print(f"Invalid file path: {name}")
