from panda3d.core import loadPrcFileData, AmbientLight, DirectionalLight, Vec4
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties, ClockObject


class Py5GLEngine(ShowBase):
    def __init__(self, window_title="Py5GL Engine"):
        loadPrcFileData('', f'window-title {window_title}')
        super().__init__()

        self.set_frame_rate(60)
        self.setup_window()
        self.setup_scene()
        self.setup_input()
        self.setup_lights()

        self.taskMgr.add(self.display_fps, "DisplayFPS")

    def set_frame_rate(self, fps):
        globalClock = ClockObject.getGlobalClock()
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(fps)

    def setup_window(self):
        props = WindowProperties()
        props.setSize(1280, 720)
        self.win.requestProperties(props)

    def setup_scene(self):
        try:
            self.model = self.loader.loadModel("models/teapot")
            self.model.reparentTo(self.render)
            self.model.setScale(0.5)
            self.model.setPos(0, 10, 0)
        except Exception as e:
            print(f"[Py5GL Error] Failed to load model: {e}")

    def setup_input(self):
        self.accept("escape", self.quit)
        self.accept("arrow_left", self.move_model, [-0.5, 0])
        self.accept("arrow_right", self.move_model, [0.5, 0])
        self.accept("arrow_up", self.move_model, [0, 0.5])
        self.accept("arrow_down", self.move_model, [0, -0.5])

    def move_model(self, dx, dy):
        if hasattr(self, 'model'):
            pos = self.model.getPos()
            self.model.setPos(pos.getX() + dx, pos.getY() + dy, pos.getZ())

    def setup_lights(self):
        ambient_light = AmbientLight("ambient")
        ambient_light.setColor(Vec4(0.3, 0.3, 0.3, 1))
        ambient_node = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_node)

        directional_light = DirectionalLight("directional")
        directional_light.setColor(Vec4(0.7, 0.7, 0.7, 1))
        directional_node = self.render.attachNewNode(directional_light)
        directional_node.setHpr(0, -60, 0)
        self.render.setLight(directional_node)

    def display_fps(self, task):
        fps = globalClock.getAverageFrameRate()
        self.win.setTitle(f"Py5GL Engine - FPS: {fps:.2f}")
        return Task.cont

    def quit(self):
        print("[Py5GL] Exiting engine...")
        self.userExit()