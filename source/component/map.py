import random
import pygame as pg
from .. import tool
from .. import constants as c

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    #kiểm tra xem một vị trí trên bản đồ có hợp lệ không
    def isValid(self, map_x, map_y):
        if (map_x < 0 or map_x >= self.width or
            map_y < 0 or map_y >= self.height):
            return False
        return True

    #kiểm tra xem một ô trên bản đồ có thể di chuyển được không, dựa trên loại của ô đó
    def isMovable(self, map_x, map_y):
        return (self.map[map_y][map_x] == c.MAP_EMPTY)

    #tính toán vị trí của ô trên bản đồ dựa trên tọa độ pixel của màn hình
    def getMapIndex(self, x, y):
        x -= c.MAP_OFFSET_X
        y -= c.MAP_OFFSET_Y
        return (x // c.GRID_X_SIZE, y // c.GRID_Y_SIZE)

    #  tính toán tọa độ pixel trung tâm của ô trên bản đồ dựa trên vị trí của ô trên bản đồ.
    def getMapGridPos(self, map_x, map_y):
        return (map_x * c.GRID_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_OFFSET_X,
                map_y * c.GRID_Y_SIZE + c.GRID_Y_SIZE//5 * 3 + c.MAP_OFFSET_Y)

    #thiết lập loại của ô trên bản đồ tại vị trí cụ thể
    def setMapGridType(self, map_x, map_y, type):
        self.map[map_y][map_x] = type

    #trả về một vị trí ngẫu nhiên trên bản đồ.
    def getRandomMapIndex(self):
        map_x = random.randint(0, self.width-1)
        map_y = random.randint(0, self.height-1)
        return (map_x, map_y)

    # hiển thị một cây hoặc một loại cây nào đó tại một vị trí cụ thể trên màn hình.
    def showPlant(self, x, y):
        pos = None
        map_x, map_y = self.getMapIndex(x, y)
        if self.isValid(map_x, map_y) and self.isMovable(map_x, map_y):
            pos = self.getMapGridPos(map_x, map_y)
        return pos
