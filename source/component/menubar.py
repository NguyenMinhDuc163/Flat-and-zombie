import random
import pygame as pg
from .. import tool
from .. import constants as c

PANEL_Y_START = 87
PANEL_X_START = 22
PANEL_Y_INTERNAL = 74
PANEL_X_INTERNAL = 53
CARD_LIST_NUM = 8

card_name_list = [c.CARD_SUNFLOWER, c.CARD_PEASHOOTER, c.CARD_SNOWPEASHOOTER, c.CARD_WALLNUT,
                  c.CARD_CHERRYBOMB, c.CARD_THREEPEASHOOTER, c.CARD_REPEATERPEA, c.CARD_CHOMPER,
                  c.CARD_PUFFSHROOM, c.CARD_POTATOMINE, c.CARD_SQUASH, c.CARD_SPIKEWEED,
                  c.CARD_JALAPENO, c.CARD_SCAREDYSHROOM, c.CARD_SUNSHROOM, c.CARD_ICESHROOM,
                  c.CARD_HYPNOSHROOM, c.CARD_WALLNUT, c.CARD_REDWALLNUT]
plant_name_list = [c.SUNFLOWER, c.PEASHOOTER, c.SNOWPEASHOOTER, c.WALLNUT,
                   c.CHERRYBOMB, c.THREEPEASHOOTER, c.REPEATERPEA, c.CHOMPER,
                   c.PUFFSHROOM, c.POTATOMINE, c.SQUASH, c.SPIKEWEED,
                   c.JALAPENO, c.SCAREDYSHROOM, c.SUNSHROOM, c.ICESHROOM,
                   c.HYPNOSHROOM, c.WALLNUTBOWLING, c.REDWALLNUTBOWLING]
plant_sun_list = [50, 100, 175, 50, 150, 325, 200, 150, 0, 25, 50, 100, 125, 25, 25, 75, 75, 0, 0]
plant_frozen_time_list = [7500, 7500, 7500, 30000, 50000, 7500, 7500, 7500, 7500, 30000,
                          30000, 7500, 50000, 7500, 7500, 50000, 30000, 0, 0]
all_card_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


def getSunValueImage(sun_value):
    font = pg.font.SysFont(None, 22)
    width = 32
    msg_image = font.render(str(sun_value), True, c.NAVYBLUE, c.LIGHTYELLOW)
    msg_rect = msg_image.get_rect()
    msg_w = msg_rect.width

    image = pg.Surface([width, 17])
    x = width - msg_w

    image.fill(c.LIGHTYELLOW)
    image.blit(msg_image, (x, 0), (0, 0, msg_rect.w, msg_rect.h))
    image.set_colorkey(c.BLACK)
    return image

def getCardPool(data):
    card_pool = []
    for card in data:
        tmp = card['name']
        for i,name in enumerate(plant_name_list):
            if name == tmp:
                card_pool.append(i)
                break
    return card_pool

class Card():
    def __init__(self, x, y, name_index, scale=0.78):
        self.loadFrame(card_name_list[name_index], scale)
        self.rect = self.orig_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.name_index = name_index
        self.sun_cost = plant_sun_list[name_index]
        self.frozen_time = plant_frozen_time_list[name_index]
        self.frozen_timer = -self.frozen_time
        self.refresh_timer = 0
        self.select = True

    # tải hình ảnh của thẻ cây từ tool.GFX
    def loadFrame(self, name, scale):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.orig_image = tool.get_image(frame, 0, 0, width, height, c.BLACK, scale)
        self.image = self.orig_image

    # kiểm tra xem chuột có được nhấp vào thẻ cây không.
    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    #kiểm tra xem có thể nhấp vào thẻ cây không, dựa trên giá trị sun_value và thời gian hiện tại.
    def canClick(self, sun_value, current_time):
        if self.sun_cost <= sun_value and (current_time - self.frozen_timer) > self.frozen_time:
            return True
        return False

    # kiểm tra xem thẻ cây có thể được chọn không.
    def canSelect(self):
        return self.select

    def setSelect(self, can_select):
        self.select = can_select
        if can_select:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(128)

    # đặt thời gian đóng băng của thẻ cây dựa trên thời gian hiện tại.
    def setFrozenTime(self, current_time):
        self.frozen_timer = current_time

    # tạo hình ảnh để hiển thị thẻ cây dựa trên giá trị sun_value và thời gian hiện tại.
    def createShowImage(self, sun_value, current_time):
        time = current_time - self.frozen_timer
        if time < self.frozen_time:  # card cool down status
            image = pg.Surface([self.rect.w, self.rect.h])
            frozen_image = self.orig_image.copy()
            frozen_image.set_alpha(128)
            frozen_height = (self.frozen_time - time)/self.frozen_time * self.rect.h
            
            image.blit(frozen_image, (0,0), (0, 0, self.rect.w, frozen_height))
            image.blit(self.orig_image, (0,frozen_height),
                       (0, frozen_height, self.rect.w, self.rect.h - frozen_height))
        elif self.sun_cost > sun_value: # card disable status
            image = self.orig_image.copy()
            image.set_alpha(192)
        else:
            image = self.orig_image
        return image
    # cập nhật hình ảnh của thẻ cây dựa trên giá trị sun_value và thời gian hiện tại.
    def update(self, sun_value, current_time):
        if (current_time - self.refresh_timer) >= 250:
            self.image = self.createShowImage(sun_value, current_time)
            self.refresh_timer = current_time

    #vẽ thẻ cây trên bề mặt được chỉ định.
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class MenuBar():
    #  tạo ra một thanh menu với một danh sách thẻ card cụ thể và giá trị sun cụ thể.
    def __init__(self, card_list, sun_value):
        self.loadFrame(c.MENUBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 0
        
        self.sun_value = sun_value
        self.card_offset_x = 32
        self.setupCards(card_list)

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)
        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    #  cập nhật thời gian hiện tại và cập nhật các thẻ card trong thanh menu.
    def update(self, current_time):
        self.current_time = current_time
        for card in self.card_list:
            card.update(self.sun_value, self.current_time)

    # tạo hình ảnh của thanh menu dựa trên số lượng và vị trí cụ thể.
    def createImage(self, x, y, num):
        if num == 1:
            return
        img = self.image
        rect = self.image.get_rect()
        width = rect.w
        height = rect.h
        self.image = pg.Surface((width * num, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        for i in range(num):
            x = i * width
            self.image.blit(img, (x,0))
        self.image.set_colorkey(c.BLACK)

    #  thiết lập danh sách thẻ card cụ thể trên thanh menu dựa trên danh sách card đã cho.
    def setupCards(self, card_list):
        self.card_list = []
        x = self.card_offset_x
        y = 8
        for index in card_list:
            x += 55
            self.card_list.append(Card(x, y, index))

    # kiểm tra xem chuột có được nhấp vào thẻ card trong thanh menu không.
    def checkCardClick(self, mouse_pos):
        result = None
        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.canClick(self.sun_value, self.current_time):
                    result = (plant_name_list[card.name_index], card)
                break
        return result

    #  kiểm tra xem chuột có được nhấp vào thanh menu không.
    def checkMenuBarClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False
    #  giảm giá trị sun theo giá trị cụ thể.
    def decreaseSunValue(self, value):
        self.sun_value -= value

    # tăng giá trị sun theo giá trị cụ thể.
    def increaseSunValue(self, value):
        self.sun_value += value

    # đặt thời gian đóng băng của thẻ card cụ thể dựa trên tên cây.
    def setCardFrozenTime(self, plant_name):
        for card in self.card_list:
            if plant_name_list[card.name_index] == plant_name:
                card.setFrozenTime(self.current_time)
                break
    # vẽ giá trị sun trên thanh menu.
    def drawSunValue(self):
        self.value_image = getSunValueImage(self.sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.rect.bottom - 21
        
        self.image.blit(self.value_image, self.value_rect)

    #  vẽ thanh menu trên bề mặt được chỉ định.
    def draw(self, surface):
        self.drawSunValue()
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)

class Panel():
    def __init__(self, card_list, sun_value):
        self.loadImages(sun_value)
        self.selected_cards = []
        self.selected_num = 0
        self.setupCards(card_list)

    #tải khung hình ảnh theo tên được chỉ định và trả về hình ảnh đã được tải.
    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        return tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    # tải các hình ảnh cần thiết cho bảng điều khiển, bao gồm hình ảnh nền của menu,
    # hình ảnh nền của bảng điều khiển và hình ảnh giá trị của tài nguyên mặt trời.
    def loadImages(self, sun_value):
        self.menu_image = self.loadFrame(c.MENUBAR_BACKGROUND)
        self.menu_rect = self.menu_image.get_rect()
        self.menu_rect.x = 0
        self.menu_rect.y = 0

        self.panel_image = self.loadFrame(c.PANEL_BACKGROUND)
        self.panel_rect = self.panel_image.get_rect()
        self.panel_rect.x = 0
        self.panel_rect.y = PANEL_Y_START

        
        self.value_image = getSunValueImage(sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.menu_rect.bottom - 21

        self.button_image =  self.loadFrame(c.START_BUTTON)
        self.button_rect = self.button_image.get_rect()
        self.button_rect.x = 155
        self.button_rect.y = 547

    # thiết lập vị trí cho từng thẻ trên bảng điều khiển, dựa trên danh sách thẻ đã cho.
    def setupCards(self, card_list):
        self.card_list = []
        x = PANEL_X_START - PANEL_X_INTERNAL
        y = PANEL_Y_START + 43 - PANEL_Y_INTERNAL
        for i, index in enumerate(card_list):
            if i % 8 == 0:
                x = PANEL_X_START - PANEL_X_INTERNAL
                y += PANEL_Y_INTERNAL
            x += PANEL_X_INTERNAL
            self.card_list.append(Card(x, y, index, 0.75))

    #  kiểm tra xem người dùng đã nhấp vào thẻ nào trên bảng điều khiển chưa và thực hiện hành động tương ứng.
    def checkCardClick(self, mouse_pos):
        delete_card = None
        for card in self.selected_cards:
            if delete_card:
                card.rect.x -= 55
            elif card.checkMouseClick(mouse_pos):
                self.deleteCard(card.name_index)
                delete_card = card

        if delete_card:
            self.selected_cards.remove(delete_card)
            self.selected_num -= 1

        if self.selected_num == CARD_LIST_NUM:
            return

        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.canSelect():
                    self.addCard(card)
                break

    # thêm một thẻ vào danh sách các thẻ đã chọn trên bảng điều khiển.
    def addCard(self, card):
        card.setSelect(False)
        y = 8
        x = 78 + self.selected_num * 55
        self.selected_cards.append(Card(x, y, card.name_index))
        self.selected_num += 1
    #  xóa một thẻ từ danh sách các thẻ đã chọn trên bảng điều khiển.
    def deleteCard(self, index):
        self.card_list[index].setSelect(True)

    # kiểm tra xem người dùng đã nhấp vào nút bắt đầu trò chơi trên bảng điều khiển chưa.
    def checkStartButtonClick(self, mouse_pos):
        if self.selected_num < CARD_LIST_NUM:
            return False

        x, y = mouse_pos
        if (x >= self.button_rect.x and x <= self.button_rect.right and
            y >= self.button_rect.y and y <= self.button_rect.bottom):
           return True
        return False

    # rả về danh sách các thẻ đã chọn.
    def getSelectedCards(self):
        card_index_list = []
        for card in self.selected_cards:
            card_index_list.append(card.name_index)
        return card_index_list

    # vẽ các thành phần của bảng điều khiển lên màn hình chơi. Điều này bao gồm vẽ hình ảnh nền,
    # vẽ các thẻ và vẽ nút bắt đầu nếu đủ số lượng thẻ đã chọn.
    def draw(self, surface):
        self.menu_image.blit(self.value_image, self.value_rect)
        surface.blit(self.menu_image, self.menu_rect)
        surface.blit(self.panel_image, self.panel_rect)
        for card in self.card_list:
            card.draw(surface)
        for card in self.selected_cards:
            card.draw(surface)

        if self.selected_num == CARD_LIST_NUM:
            surface.blit(self.button_image, self.button_rect)

class MoveCard():
    def __init__(self, x, y, card_name, plant_name, scale=0.78):
        self.loadFrame(card_name, scale)
        self.rect = self.orig_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = 1
        self.image = self.createShowImage()

        self.card_name = card_name
        self.plant_name = plant_name
        self.move_timer = 0
        self.select = True

    def loadFrame(self, name, scale):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.orig_image = tool.get_image(frame, 0, 0, width, height, c.BLACK, scale)
        self.orig_rect = self.orig_image.get_rect()
        self.image = self.orig_image

    # kiểm tra xem người dùng đã nhấp chuột vào thẻ di chuyển hay chưa.
    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    #  tạo hình ảnh hiển thị của thẻ di chuyển
    def createShowImage(self):
        if self.rect.w < self.orig_rect.w:
            image = pg.Surface([self.rect.w, self.rect.h])
            image.blit(self.orig_image, (0, 0), (0, 0, self.rect.w, self.rect.h))
            self.rect.w += 1
        else:
            image = self.orig_image
        return image

    # cập nhật vị trí của thẻ di chuyển trên thanh di chuyển và thời gian di chuyển của nó.
    def update(self, left_x, current_time):
        if self.move_timer == 0:
            self.move_timer = current_time
        elif (current_time - self.move_timer) >= c.CARD_MOVE_TIME:
            if self.rect.x > left_x:
                self.rect.x -= 1
                self.image = self.createShowImage()
            self.move_timer += c.CARD_MOVE_TIME

    #  vẽ hình ảnh của thẻ di chuyển lên màn hình.
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class MoveBar():
    def __init__(self, card_pool):
        self.loadFrame(c.MOVEBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 0
        
        self.card_start_x = self.rect.x + 8
        self.card_end_x = self.rect.right - 5
        self.card_pool = card_pool
        self.card_list = []
        self.create_timer = -c.MOVEBAR_CARD_FRESH_TIME

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    #  tạo thẻ di chuyển mới nếu còn chỗ trống trên thanh di chuyển.
    def createCard(self):
        if len(self.card_list) > 0 and self.card_list[-1].rect.right > self.card_end_x:
            return False
        x = self.card_end_x
        y = 6
        index = random.randint(0, len(self.card_pool) - 1)
        card_index = self.card_pool[index]
        card_name = card_name_list[card_index] + '_move'
        plant_name = plant_name_list[card_index]
        self.card_list.append(MoveCard(x, y, card_name, plant_name))
        return True

    # cập nhật vị trí của các thẻ di chuyển trên thanh di chuyển và thời gian tạo thẻ mới.
    def update(self, current_time):
        self.current_time = current_time
        left_x = self.card_start_x
        for card in self.card_list:
            card.update(left_x, self.current_time)
            left_x = card.rect.right + 1

        if(self.current_time - self.create_timer) > c.MOVEBAR_CARD_FRESH_TIME:
            if self.createCard():
                self.create_timer = self.current_time

    # kiểm tra xem người dùng đã nhấp chuột vào thẻ trên thanh di chuyển hay chưa.
    def checkCardClick(self, mouse_pos):
        result = None
        for index, card in enumerate(self.card_list):
            if card.checkMouseClick(mouse_pos):
                result = (card.plant_name, card)
                break
        return result

    # kiểm tra xem người dùng đã nhấp chuột vào thanh di chuyển hay chưa.
    def checkMenuBarClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    #  xóa một thẻ khỏi danh sách thẻ trên thanh di chuyển.
    def deleateCard(self, card):
        self.card_list.remove(card)

    # vẽ thanh di chuyển cùng với các thẻ di chuyển trên màn hình.
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)