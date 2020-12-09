class Device:
    def __init__(self, name):
        self.is_on = False
        self.running = False
        self.progress = 0
        self.product = None
        self.name = name
