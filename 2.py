import pygame
import os


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, f):
        super().__init__(all_sprites)
        self.frames = []
        self.left_turn = False
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.index = 0
        self.velocity = pygame.math.Vector2()
        self.animation_frames = f
        self.image = self.frames[self.index]
        self.rect = self.rect.move(x, y)
 
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                if self.left_turn:
                    self.frames.append(pygame.transform.flip(sheet.subsurface(
                        pygame.Rect(frame_location, self.rect.size)), True, False))
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


def end_screen():
    fon = load_image('game_over.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #elif event.type == pygame.MOUSEBUTTONDOWN:
                ## координаты кнопки
                #if event.pos[0] in range(316, 625) and event.pos[1] in range(260, 365):
                    #k = 1
                    #fon = load_image('rule' + str(k) + '.png')
                    #screen.blit(fon, (0, 0))                
        pygame.display.flip()
        clock.tick(100)


class cat(AnimatedSprite):
    def __init__(self, sheet=load_image("m_k1.png"), columns=7, rows=2, x=0, y=517, f=10):
        super().__init__(sheet, columns, rows, x, y, f)
        self.jump = 0
        self.down = False #спрыгивает ли игрок вниз, нажимая на "s"
        self.mask = pygame.mask.from_surface(self.image)
        self.below = kv(self.rect.x, self.rect.y, down=True)
        self.above = kv(self.rect.x, self.rect.y, down=False)
        self.right = kv(self.rect.x, self.rect.y, right=True)
        self.left = kv(self.rect.x, self.rect.y, right=False)
        self.count = 3
    
    def update_constraints(self):
        self.below.update(self.rect.x, self.rect.y)
        self.above.update(self.rect.x, self.rect.y)
        self.right.update(self.rect.x, self.rect.y)
        self.left.update(self.rect.x, self.rect.y)
    
    def update(self):
        self.update_constraints()
        self.movement()
        self.update_frame_dependent()

    def movement(self):
        if self.velocity.y < 0 and self.jump != 50 and not pygame.sprite.spritecollideany(self.above, horizontal_borders):
            self.jump += 1
            self.frames = []
            x, y = self.rect[:2]
            sheet = load_image("m_k3.png")
            if self.velocity.x < 0:
                if pygame.sprite.spritecollideany(self.left, vertical_borders):
                    self.velocity.x = 0 
                self.left_turn = True
            else:
                if pygame.sprite.spritecollideany(self.right, vertical_borders) and self.velocity.x>0:
                    self.velocity.x = 0                 
                self.left_turn = False  
            self.cut_sheet(sheet, 5, 2)
            self.rect = self.rect.move(x, y)
            self.animation_frames = 5
        elif not pygame.sprite.spritecollideany(self.below, horizontal_borders) and (
            not pygame.sprite.spritecollideany(self.below, horizontal_borders2) or self.down ):
            # Столкновение с горизонтальными стенками
            self.down = False
            if self.velocity.x != 0 and pygame.sprite.spritecollideany(self.right, vertical_borders) and self.velocity.x > 0 or\
                pygame.sprite.spritecollideany(self.left, vertical_borders) and self.velocity.x < 0:
                self.velocity.x = 0
            self.index = 7
            self.velocity.y = 2
        elif pygame.sprite.spritecollideany(self.left, vertical_borders) and self.velocity.x < 0 or\
             pygame.sprite.spritecollideany(self.right, vertical_borders) and self.velocity.x > 0:
            self.jump = 0
            self.animation_frames = 10
            self.velocity.y = 0
            self.frames = []
            x, y = self.rect[:2]
            if self.velocity.x < 0:
                self.left_turn = False
            else:
                self.left_turn = True            
            self.velocity.x = 0
            sheet = load_image("m_k2.png")   
            self.cut_sheet(sheet, 5, 1)
            self.rect = self.rect.move(x, y)      
        else:
            self.down = False
            self.jump = 0
            self.animation_frames = 10
            self.velocity.y = 0
            self.frames = []
            x, y = self.rect[:2]
            if self.velocity.x != 0:
                sheet = load_image("m_k2.png")
                if self.velocity.x < 0:
                    self.left_turn = True
                else:
                    self.left_turn = False  
                self.cut_sheet(sheet, 5, 1)                                    
            else:
                self.cut_sheet(load_image("m_k1.png"), 7, 2)
            self.rect = self.rect.move(x, y)

    
class fireball(AnimatedSprite):
    def __init__(self, x, y, sheet=load_image("cn.png"), columns=1, rows=1, f=10):
        super().__init__(sheet, columns, rows, x+20, y+20, f)
        if player.left_turn:
            self.velocity.x = -4
        else:
            self.velocity.x = 4
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.spritecollideany(self, vertical_borders):
            self.update_frame_dependent()
        else:
            global shot
            all_sprites.remove(self)
            shot = None


class enemy(AnimatedSprite):
    def __init__(self, sheet=load_image("en.png"), columns=1, rows=1, x=500, y=500, f=10):
        super().__init__(sheet, columns, rows, x, y, f)
        self.velocity.x = -1
        self.mask = pygame.mask.from_surface(self.image)
    
    def death(self):
        global shot
        if pygame.sprite.collide_mask(self, shot):
            all_sprites.remove(shot)
            all_sprites.remove(self)
            enemys.remove(self)
            shot = None
        
    def update(self):
        global shot
        if shot != None:
            self.death()
        if pygame.sprite.collide_mask(self, player):
            global running
            running = False        
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.frames = []
            self.velocity.x *= -1
            self.left_turn = not self.left_turn
            x, y = self.rect[:2]
            self.cut_sheet(load_image("en.png"), 1, 1)
            self.rect = self.rect.move(x, y)
        self.update_frame_dependent()


class kv(pygame.sprite.Sprite):
    def __init__(self, x, y, down=None, right=None):
        super().__init__()
        self.down = down
        self.right = right
        if self.down != None:
            if self.down:
                self.image = pygame.Surface([100 - 10, 2])
                self.rect = pygame.Rect(x + 5, y + 78, 100 - 10, 2)
            else:
                self.image = pygame.Surface([100 - 10, 2])
                self.rect = pygame.Rect(x + 5, y + 15, 100 - 10, 2)
        else:
            if self.right:
                self.image = pygame.Surface([2, 100 - 37])
                self.rect = pygame.Rect(x + 94, y + 16, 2, 100 - 37)
            else:
                self.image = pygame.Surface([2, 100 - 37])
                self.rect = pygame.Rect(x + 4, y + 16, 2, 100 - 37)
    
    def update(self, x1, y1):
        if self.down != None:
            if self.down:
                x1 += 5
                y1 += 78
            else:
                x1 += 5
                y1 += 15
        else:
            if self.right:
                x1 += 94
                y1 += 16
            else:
                x1 += 4
                y1 += 16
        self.rect.x = x1
        self.rect.y = y1        


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, ability=False):
        super().__init__(all_sprites)
        #super().__init__()
        if ability:
            self.add(horizontal_borders2)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
            self.image.fill(pygame.Color('green'))
        else:
            if x1 == x2:  # вертикальная стенка
                self.add(vertical_borders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:  # горизонтальная стенка
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

st = True
while st:
    pygame.init()
    size = (1000, 600)
    running = True
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    shot = None
    all_sprites = pygame.sprite.Group()
    #start_screen()
    enemys = pygame.sprite.Group(enemy())
    horizontal_borders2 = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    Border(5, 5, 1000 - 5, 5)
    Border(5, 600 - 5, 1000 - 5, 600 - 5)
    Border(5, 500, 400, 500, True)
    Border(400, 500, 500, 500)
    Border(5, 5, 5, 600 - 5)
    Border(500, 500, 500, 600 - 5) #АНТИ-МОНСТР
    player = cat()
    Border(1000 - 5, 5, 1000 - 5, 600 - 5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                st = False
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
                elif event.key == pygame.K_SPACE:
                    if shot == None and player.count > 0:
                        shot = fireball(*player.rect[:2])
                        player.count -= 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    player.velocity.x = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity.y = 0
        screen.fill(pygame.Color('white'))
        if shot != None:
            shot.update()        
        player.update()
        enemys.update()
        all_sprites.draw(screen)
        clock.tick(100)
        pygame.display.flip()
    if st:
        end_screen()
pygame.quit()
