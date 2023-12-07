from inky.auto import auto

class Paper:
    def __init__(self):
        self.inky = auto(ask_user=True, verbose=True)


    def print(self, img):
        img = img.resize(self.inky.resolution)
        self.inky.set_image(img, saturation = 0.5)
        self.inky.show()
