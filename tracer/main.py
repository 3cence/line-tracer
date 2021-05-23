import glob
from Path_Mapping import prepare, map_image as mi
import time

images = glob.glob("training_images_in/*")
for image in images:
    name = image.split("\\")
    prepare.ready_for_training(name[1], 28)
time_prepared = time.thread_time()
print(f"Prepared in {time_prepared} seconds")

images = glob.glob("training_images_out/*.png")
for image in images:
    name = image.split("\\")
    mi.PathMapping(name[1])
print(f"Plotted in {time.thread_time() - time_prepared} seconds")
