from ui.view import View


class Device:
    def __init__(self, name):
        self.is_on = False
        self.running = False
        self.progress = 0
        self.product = None
        self.name = name
        self.ui = View(name)

    def get_status(self):
        return "On" if self.is_on else "Off"
