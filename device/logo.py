from PIL import Image

class Logo:
    def __init__(self, paper):
        self.paper = paper


    def show(self):
        self.paper.print(Image.open("./template/logo.png"))
    