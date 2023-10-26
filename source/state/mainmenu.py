import pygame as pg
from .. import tool
from .. import constants as c

class Menu(tool.State):
    def __init__(self):
        tool.State.__init__(self)

    # khởi tạo màn hình menu chính và thiết lập nền và các tùy chọn trong menu.
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        
        self.setupBackground()
        self.setupOption()

    # thiết lập hình ảnh nền cho menu chính.
    def setupBackground(self):
        frame_rect = [80, 0, 800, 600]
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

    # thiết lập các tùy chọn trong menu chính, bao gồm các khung hình ảnh và vị trí của chúng trên màn hình.
    def setupOption(self):
        self.option_frames = []
        frame_names = [c.OPTION_ADVENTURE + '_0', c.OPTION_ADVENTURE + '_1']
        frame_rect = [0, 0, 165, 77]
        
        for name in frame_names:
            self.option_frames.append(tool.get_image(tool.GFX[name], *frame_rect, c.BLACK, 1.7))
        
        self.option_frame_index = 0
        self.option_image = self.option_frames[self.option_frame_index]
        self.option_rect = self.option_image.get_rect()
        self.option_rect.x = 435
        self.option_rect.y = 75
        
        self.option_start = 0
        self.option_timer = 0
        self.option_clicked = False
    #  kiểm tra xem người dùng đã nhấp vào tùy chọn trên menu chưa.
    def checkOptionClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.option_rect.x and x <= self.option_rect.right and
           y >= self.option_rect.y and y <= self.option_rect.bottom):
            self.option_clicked = True
            self.option_timer = self.option_start = self.current_time
        return False

    # cập nhật trạng thái của menu, bao gồm việc kiểm tra xem người dùng có nhấp vào tùy chọn không
    # và thực hiện các hành động tương ứng.
    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if not self.option_clicked:
            if mouse_pos:
                self.checkOptionClick(mouse_pos)
        else:
            if(self.current_time - self.option_timer) > 200:
                self.option_frame_index += 1
                if self.option_frame_index >= 2:
                    self.option_frame_index = 0
                self.option_timer = self.current_time
                self.option_image = self.option_frames[self.option_frame_index]
            if(self.current_time - self.option_start) > 1300:
                self.done = True

        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.option_image, self.option_rect)