import numpy as np
from scipy.spatial.transform import Rotation as R 

class Camera:
    """
    defines a camera where its center looks at +z
    """
    def __init__(self, center, roll, pitch, yaw, height, width, x_angle, y_angle):
        self.r = np.array(center)
        self.e = np.array([roll, pitch, yaw]) * np.pi / 180.
        self.get_orientation() 
        self.tx = x_angle * np.pi / 180.
        self.ty = y_angle * np.pi / 180.
        self.h = height
        self.w = width

    def get_orientation(self):
        self.c = R.from_euler('xyz', self.e)
        self.x = self.c.as_matrix()[:,0]
        self.y = self.c.as_matrix()[:,1]
        self.n = self.c.as_matrix()[:,2]

    def canvas_size(self, distance):
        self.get_orientation()
        self.image_center = self.r + self.n * distance
        self.dx = np.tan(self.tx) * distance * self.x
        self.dy = np.tan(self.ty) * distance * self.y
        self.upper_left_corner = self.image_center - self.dx - self.dy
        self.lower_right_corner = self.image_center + self.dx + self.dy
        self.pixel_x = 2 * self.dx / self.w
        self.pixel_y = 2 * self.dy / self.h

    def get_pixel_ray(self, x_idx, y_idx):
        base = (
            self.pixel_x * x_idx + self.pixel_y * y_idx
            + self.upper_left_corner 
            + self.pixel_x * 0.5 + self.pixel_y * 0.5
            )
        return base, self.n

if __name__ == "__main__":

    # test the camera model
    c = Camera((0,0,0), 90, 0, 0, 800, 600, 45, 45)
    c.canvas_size(1)
    print(c.get_pixel_ray(1,1))
    
