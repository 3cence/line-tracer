from PIL import Image
import numpy as np


class PathMapping:
    def __init__(self, fp):
        self.base = Image.open(f"training_images_out/{fp}", "r")
        self.base_array = np.asarray(self.base)
        self.path_map_image = Image.new("RGBA", self.base.size)
        self.path_map = []
        self.map_canadates = self.get_valid_pixels()
        self.path_array = np.asarray(self.path_map_image).copy()

        self.trim_valid_pixels()
        self.connect_map()
        self.paint_valid_to_array()
        self.print_order(fp)
        self.path_map_image = Image.fromarray(self.path_array)
        self.path_map_image.save(f"mappings/{fp.split('.')[0]}.png")

    def get_valid_pixels(self):
        valid_pixels = []
        for y, y_array in enumerate(self.base_array):
            for x, x_array in enumerate(y_array):
                if x_array[0] == 255:
                    valid_pixels.append([y, x])
        return valid_pixels

    def paint_valid_to_array(self):
        for pos in self.map_canadates:
            for loc, rgb_val in enumerate(self.path_array[pos[0]][pos[1]]):
                self.path_array[pos[0]][pos[1]][loc] = 1
                self.path_array[pos[0]][pos[1]][3] = 255

    def trim_valid_pixels(self):
        for canadate in self.map_canadates:
            self.remove_entry(canadate, 2, 2)
            self.remove_entry(canadate, 2, 1)
            self.remove_entry(canadate, 2, 0)
            self.remove_entry(canadate, 2, -1)
            self.remove_entry(canadate, 2, -2)
            self.remove_entry(canadate, 1, 2)
            self.remove_entry(canadate, 1, 1)
            self.remove_entry(canadate, 1, 0)
            self.remove_entry(canadate, 1, -1)
            self.remove_entry(canadate, 1, -2)
            self.remove_entry(canadate, 0, 2)
            self.remove_entry(canadate, 0, 1)
            self.remove_entry(canadate, 0, -1)
            self.remove_entry(canadate, 0, -2)
            self.remove_entry(canadate, -1, 2)
            self.remove_entry(canadate, -1, 1)
            self.remove_entry(canadate, -1, 0)
            self.remove_entry(canadate, -1, -1)
            self.remove_entry(canadate, -1, -2)
            self.remove_entry(canadate, -2, 2)
            self.remove_entry(canadate, -2, 1)
            self.remove_entry(canadate, -2, 0)
            self.remove_entry(canadate, -2, -1)
            self.remove_entry(canadate, -2, -2)

    def connect_map(self):
        self.path_map.append(self.map_canadates[0])
        stack = [self.path_map[0]]
        missing_pixels = len(self.map_canadates)
        backtracking = False
        scan_map = [[[4, -4],  [4, -3],  [4, -2],  [4, -1],  [4, 0],  [4, 1],  [4, 2],  [4, 3],  [4, 4]],
                    [[3, -4],  [3, -3],  [3, -2],  [3, -1],  [3, 0],  [3, 1],  [3, 2],  [3, 3],  [3, 4]],
                    [[2, -4],  [2, -3],  [2, -2],  [2, -1],  [2, 0],  [2, 1],  [2, 2],  [2, 3],  [2, 4]],
                    [[1, -4],  [1, -3],  [1, -2],  [1, -1],  [1, 0],  [1, 1],  [1, 2],  [1, 3],  [1, 4]],
                    [[0, -4],  [0, -3],  [0, -2],  [0, -1],  [0, 0],  [0, 1],  [0, 2],  [0, 3],  [0, 4]],
                    [[-1, -4], [-1, -3], [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3], [-1, 4]],
                    [[-2, -4], [-2, -3], [-2, -2], [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3], [-2, 4]],
                    [[-3, -4], [-3, -3], [-3, -2], [-3, -1], [-3, 0], [-3, 1], [-3, 2], [-3, 3], [-3, 4]],
                    [[-4, -4], [-4, -3], [-4, -2], [-4, -1], [-4, 0], [-4, 1], [-4, 2], [-4, 3], [-4, 4]]]

        while missing_pixels != 0:
            pixel = stack[-1]
            possible_pixels = []
            for modx in scan_map:
                for mody in modx:
                    if mody != [0, 0]:
                        index = [pixel[0] + mody[0], pixel[1] + mody[1]]
                        if index in self.map_canadates and index not in self.path_map:
                            index.append(np.sqrt(np.square(mody[0]) + np.square(mody[1])))
                            possible_pixels.append(index)
                            backtracking = False

            closest = [None, None, None]
            for x, y, dist in possible_pixels:
                if closest[0] is None or dist < closest[0]:
                    closest = [dist, x, y]

            if closest[0] is not None and not backtracking:
                stack.append([closest[1], closest[2]])
                self.path_map.append([closest[1], closest[2]])
            else:
                backtracking = True
            if backtracking and len(stack) > 1:
                stack.pop(-1)
                self.path_map.append(stack[-1])

            missing_pixels = 0
            for pix in self.map_canadates:
                if pix not in self.path_map:
                    missing_pixels += 1
            if missing_pixels == 0:
                break

    def print_order(self, fp):
        file = open(f"mappings/{fp.split('.')[0]}.txt", "w")
        referance = self.path_array
        for x, x_array in enumerate(referance):
            for y, y_array in enumerate(x_array):
                if [x, y] in self.path_map:
                    file.write(f"[{self.path_map.index([x, y])}, {self.path_map.count([x, y])}]")
                else:
                    file.write("0")
            file.write("\n")
        file.close()

    def remove_entry(self, canadate,  y, x):
        try:
            self.map_canadates.remove([canadate[0] + y, canadate[1] + x])
        except ValueError:
            pass
