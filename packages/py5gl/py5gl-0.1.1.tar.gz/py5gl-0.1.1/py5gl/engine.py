from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase

class Py5GLEngine(ShowBase):
    def __init__(self):
        loadPrcFileData('', 'window-title Py5GL Engine')
        super().__init__()
        
        model = self.loader.loadModel("models/teapot")
        model.reparentTo(self.render)
        model.setScale(0.5)