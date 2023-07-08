
class FrameInfo:

    hummidity_x = None
    hummidity_y = None

    ambient_temp_x = None
    ambient_temp_y = None

    scale_x = None
    scale_y = None

    def __init__(self):
        pass

    @classmethod
    def find_blue_bounding(cls, frame):
        