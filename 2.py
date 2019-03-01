import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, f):
        super(AnimatedSprite, self).__init__()
        self.frames = []
        self.transform = False
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.index = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.animation_frames = f
        self.image = self.frames[self.index]
        self.rect = self.rect.move(x, y)
 
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                if self.transform:
                    self.frames.append(pygame.transform.flip(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), True, False))
                else:
                    self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_frame_dependent(self):
        self.cur_frame += 1
        if self.cur_frame >= self.animation_frames:
            self.cur_frame = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
        self.rect.move_ip(self.velocity)
        

def start_screen():
    fon = load_image('заставка.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)

    k = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # координаты кнопки
                if event.pos[0] in range(316, 625) and event.pos[1] in range(260, 365):
                    k = 1
                    fon = load_image('rule' + str(k) + '.png')
                    screen.blit(fon, (0, 0))                    
                if 0 < k < 3 and event.pos[0] in range(800, 960)\
                             and event.pos[1] in range(510, 543):
                    k += 1
                    fon = load_image('rule' + str(k) + '.png')
                    screen.blit(fon, (0, 0))
                elif k == 3:
                    if event.pos[0] in range(490, 561)\
                       and event.pos[1] in range(510, 540):
                        k = 1
                        fon = load_image('rule' + str(k) + '.png')
                        screen.blit(fon, (0, 0))
                    elif event.pos[0] in range(795, 865)\
                       and event.pos[1] in range(510, 540):
                        return
        pygame.display.flip()
        clock.tick(100)


class cat(AnimatedSprite):
    def __init__(self, sheet=load_image("m_k1.png"), columns=7, rows=2, x=300, y=515, f=10):
        super(cat, self).__init__(sheet, columns, rows, x, y, f)
        self.jump = 0
        self.down = False
    
    def update(self):
        rect2 = kv(self.rect.x, self.rect.y, down=True)
        rect3 = kv(self.rect.x, self.rect.y, down=False)
        rect4 = kv(self.rect.x, self.rect.y, right=False)
        rect5 = kv(self.rect.x, self.rect.y, right=True)
        if self.velocity.y < 0 and self.jump != 50 and not pygame.sprite.spritecollideany(rect3, horizontal_borders):
            self.jump += 1
            self.frames = []
            x, y = self.rect[:2]
            sheet = load_image("m_k3.png")
            if self.velocity.x < 0:
                if pygame.sprite.spritecollideany(rect4, vertical_borders):
                    self.velocity.x = 0 
                self.transform = True
            else:
                if pygame.sprite.spritecollideany(rect5, vertical_borders) and self.velocity.x>0:
                    self.velocity.x = 0                 
                self.transform = False  
            self.cut_sheet(sheet, 5, 2)
            self.rect = self.rect.move(x, y)
            self.animation_frames = 5
        elif not pygame.sprite.spritecollideany(rect2, horizontal_borders) or self.down:
            #ЗДЕСЬ НУЖНО ПРОЕРЯТЬ НА СТОЛКНОВЕНИЕ С ОБЪЕКТАМИ
            self.down = False
            if self.velocity.x != 0:
                if pygame.sprite.spritecollideany(rect5, vertical_borders) and self.velocity.x > 0 or\
                   pygame.sprite.spritecollideany(rect4, vertical_borders) and self.velocity.x < 0:
                    self.velocity.x = 0
            self.index = 7
            self.velocity.y = 2
        elif pygame.sprite.spritecollideany(rect4, vertical_borders) and self.velocity.x < 0 or\
             pygame.sprite.spritecollideany(rect5, vertical_borders) and self.velocity.x > 0:
            self.jump = 0
            self.animation_frames = 10
            self.velocity.y = 0
            self.frames = []
            x, y = self.rect[:2]            
            self.velocity.x = 0
            sheet = load_image("m_k2.png")
            sheet = load_image("m_k2.png")
            if self.velocity.x < 0:
                self.transform = True
            else:
                self.transform = False   
            self.cut_sheet(sheet, 5, 1)
            self.rect = self.rect.move(x, y)      
        else:
            self.jump = 0
            self.animation_frames = 10
            self.velocity.y = 0
            self.frames = []
            x, y = self.rect[:2]
            if self.velocity.x != 0:
                sheet = load_image("m_k2.png")
                if self.velocity.x < 0:
                    self.transform = True
                else:
                    self.transform = False  
                self.cut_sheet(sheet, 5, 1)                                    
            else:
                self.cut_sheet(load_image("m_k1.png"), 7, 2)
            self.rect = self.rect.move(x, y)
        self.update_frame_dependent()


class kv(pygame.sprite.Sprite):
    def __init__(self, x1, y1, down=None, right=None):
        super(kv, self).__init__()
        if down != None:
            if down:
                self.image = pygame.Surface([100-10, 2])
                self.rect = pygame.Rect(x1+5, y1+78, 100-10, 2)
            else:
                self.image = pygame.Surface([100-10, 2])
                self.rect = pygame.Rect(x1+5, y1+15, 100-10, 2)
        else:
            if right:
                self.image = pygame.Surface([2, 100-37])
                self.rect = pygame.Rect(x1+94, y1+16, 2, 100-37)
            else:
                self.image = pygame.Surface([2, 100-37])
                self.rect = pygame.Rect(x1+4, y1+16, 2, 100-37)         
            

class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        #super(Border, self).__init__()
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


pygame.init()
size = (1000, 600)
running = True
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
#start_screen()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(5, 5, 1000 - 5, 5)
Border(5, 600 - 5, 1000 - 5, 600 - 5)
Border(5, 500, 400, 500)
Border(5, 5, 5, 600 - 5)
player = cat()
all_sprites.add(player)
Border(1000 - 5, 5, 1000 - 5, 600 - 5)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.velocity.x = 3
                player.index = 0
            elif event.key == pygame.K_a:
                player.velocity.x = -3
                player.index = 0
            elif event.key == pygame.K_s:
                player.down = True
            elif event.key == pygame.K_w:
                player.velocity.y = -2
                player.index = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                player.velocity.x = 0
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity.y = 0
    screen.fill(pygame.Color('white'))
    player.update()
    all_sprites.draw(screen)
    clock.tick(100)
    pygame.display.flip()
pygame.quit()
