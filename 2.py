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
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 60)
    font2 = pygame.font.Font(None, 50)
    
    game_name = font.render("НАЗВАНИЕ ИГРЫ", 1, (255, 255, 255))
    start = font2.render("начать игру", 1, (255, 255, 255))
    rules = font2.render("правила", 1, (255, 255, 255))
    quit = font2.render("выйти", 1, (255, 255, 255))
    
    screen.blit(game_name, ((width - game_name.get_width()) // 2, 120))
    screen.blit(start, ((width - start.get_width()) // 2, 230))
    screen.blit(rules, ((width - rules.get_width()) // 2, 300))
    screen.blit(quit, ((width - quit.get_width()) // 2, 370))
    pos = None
    k = 0
    st_game = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION and st_game:
                if event.pos[1] in range(230, 240 + start.get_height()):
                    if pos != "s":
                        sound1.play()
                        pos = "s"
                        start = font2.render("начать игру", 1, (0, 0, 0))
                        pygame.draw.rect(screen, (255, 204, 0), pygame.Rect(0, 230, width, start.get_height() + 10))
                        screen.blit(start, ((width - start.get_width()) // 2, 230))
                else:
                    if pos == "s":
                        pos = None
                        start = font2.render("начать игру", 1, (255, 255, 255))
                        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 230, width, start.get_height() + 10))
                        screen.blit(start, ((width - start.get_width()) // 2, 230))
                        
                if event.pos[1] in range(300, 310 + rules.get_height()):
                    if pos != "r":
                        sound1.play()
                        pos = "r"
                        rules = font2.render("правила", 1, (0, 0, 0))
                        pygame.draw.rect(screen, (255, 204, 0), pygame.Rect(0, 300, width, rules.get_height() + 10))
                        screen.blit(rules, ((width - rules.get_width()) // 2, 300))
                else:
                    if pos == "r":
                        pos = None
                        rules = font2.render("правила", 1, (255, 255, 255))
                        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 300, width, rules.get_height() + 10))
                        screen.blit(rules, ((width - rules.get_width()) // 2, 300))
                        
                if event.pos[1] in range(370, 380 + quit.get_height()):
                    if pos != "q":
                        sound1.play()
                        pos = "q"
                        quit = font2.render("выйти", 1, (0, 0, 0))
                        pygame.draw.rect(screen, (255, 204, 0), pygame.Rect(0, 370, width, quit.get_height() + 10))
                        screen.blit(quit, ((width - quit.get_width()) // 2, 370))
                else:
                    if pos == "q":
                        pos = None
                        quit = font2.render("выйти", 1, (255, 255, 255))
                        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 370, width, quit.get_height() + 10))
                        screen.blit(quit, ((width - quit.get_width()) // 2, 370))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # координаты кнопки
                if event.pos[1] in range(370, 380 + quit.get_height()) and st_game:
                    pygame.quit()
                    sys.exit()
                elif event.pos[1] in range(230, 240 + start.get_height()):
                    sound2.play()
                    return
                elif event.pos[1] in range(300, 310 + rules.get_height()):
                    sound2.play() 
                    st_game = False
                    k = 1
                    fond = load_image('rule' + str(k) + '.png')
                    screen.blit(fond, (0, 0))                    
                if 0 < k < 3 and event.pos[0] in range(800, 960)\
                        and event.pos[1] in range(510, 543):
                    sound2.play() 
                    k += 1
                    fond = load_image('rule' + str(k) + '.png')
                    screen.blit(fond, (0, 0))
                elif k == 3:
                    if event.pos[0] in range(490, 561)\
                       and event.pos[1] in range(510, 540):
                        sound3.play() 
                        k = 1
                        fond = load_image('rule' + str(k) + '.png')
                        screen.blit(fond, (0, 0))
                    elif event.pos[0] in range(795, 865)\
                            and event.pos[1] in range(510, 540):
                        sound3.play() 
                        st_game = True
                        screen.fill((0, 0, 0))
                        screen.blit(game_name, ((width - game_name.get_width()) // 2, 120))
                        screen.blit(start, ((width - start.get_width()) // 2, 230))
                        screen.blit(rules, ((width - rules.get_width()) // 2, 300))
                        screen.blit(quit, ((width - quit.get_width()) // 2, 370))
                        k = 0
        pygame.display.flip()
        clock.tick(100)


def end_screen(text):
    fond = load_image('end.png')
    screen.blit(fond, (0, 0))
    font = pygame.font.Font(None, 80)
    font2 = pygame.font.Font(None, 50)
    game_text = font.render(text, 1, (255, 255, 255))
    btn1 = font2.render("Главное меню", 1, (255, 255, 255))
    btn2 = font2.render("Выход", 1, (255, 255, 255))
    screen.blit(game_text, ((width - game_text.get_width()) // 2, 180))
    screen.blit(btn1, ((width - btn1.get_width()) // 4, 325))
    screen.blit(btn2, ((width - btn1.get_width()) // 10 * 9, 325))
    s = True
    bt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                if event.pos[0] in range(155, 415) and event.pos[1] in range(320, 360):
                    if s:
                        s = False
                        sound1.play()
                    bt = 1
                    btn1 = font2.render("Главное меню", 1, (255, 204, 0))
                elif event.pos[0] in range(580, 710) and event.pos[1] in range(320, 360):
                    if s:
                        s = False
                        sound1.play()
                    bt = 2
                    btn2 = font2.render("Выход", 1, (255, 204, 0))

                elif (event.pos[0] not in range(155, 415) or event.pos[1] not in range(320, 360)) and bt == 1:
                    s = True
                    bt = 0
                    btn1 = font2.render("Главное меню", 1, (255, 255, 255))
                elif (event.pos[0] not in range(580, 710) or event.pos[1] not in range(320, 360)) and bt == 2:
                    s = True
                    bt = 0
                    btn2 = font2.render("Выход", 1, (255, 255, 255))
                screen.blit(btn1, ((width - btn1.get_width()) // 4, 325))
                screen.blit(btn2, ((width - btn1.get_width()) // 10 * 9, 325))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(155, 415) and event.pos[1] in range(320, 360):
                    sound2.play()
                    return
                elif event.pos[0] in range(580, 710) and event.pos[1] in range(320, 360):
                    global is_game
                    is_game = False
                    return

        pygame.display.flip()
        clock.tick(100)


class Player(AnimatedSprite):
    def __init__(self, sheet=load_image("m_k1.png"), columns=7, rows=2, x=0, y=480, f=7):
        super().__init__(sheet, columns, rows, x, y, f)
        self.jump = 0
        self.down = False  # спрыгивает ли игрок вниз, нажимая на "s"
        self.mask = pygame.mask.from_surface(self.image)
        self.below = PlayerConstraint(self.rect.x, self.rect.y, down=True)
        self.above = PlayerConstraint(self.rect.x, self.rect.y, down=False)
        self.right = PlayerConstraint(self.rect.x, self.rect.y, right=True)
        self.left = PlayerConstraint(self.rect.x, self.rect.y, right=False)
        self.count = 0
        self.nm = 0
        self.lives = 1
    
    def update_constraints(self):
        self.below.update(self.rect.x, self.rect.y)
        self.above.update(self.rect.x, self.rect.y)
        self.right.update(self.rect.x, self.rect.y)
        self.left.update(self.rect.x, self.rect.y)
    
    def update(self):
        if self.nm == 5:
            global running
            running = False
        self.update_constraints()
        self.movement()
        self.update_frame_dependent()

    def movement(self):
        if self.lives == 0:
            global running
            running = False
        if self.velocity.y < 0 and self.jump != 30\
                and not pygame.sprite.spritecollideany(self.above, horizontal_borders):
            self.jump += 1
            self.frames = []
            x, y = self.rect[:2]
            sheet = load_image("m_k3.png")
            if self.velocity.x < 0:
                if pygame.sprite.spritecollideany(self.left, vertical_borders):
                    self.velocity.x = 0 
                self.left_turn = True
            else:
                if pygame.sprite.spritecollideany(self.right, vertical_borders) and self.velocity.x > 0:
                    self.velocity.x = 0                 
                self.left_turn = False  
            self.cut_sheet(sheet, 5, 2)
            self.rect = self.rect.move(x, y)
            self.animation_frames = 5

        elif not pygame.sprite.spritecollideany(self.below, horizontal_borders) and (
                not pygame.sprite.spritecollideany(self.below, green_borders) or self.down):
            # Столкновение с горизонтальными стенками
            self.down = False
            self.velocity.y = 3
            if self.velocity.x != 0 and pygame.sprite.spritecollideany(self.right, vertical_borders)\
                    and self.velocity.x > 0 or pygame.sprite.spritecollideany(self.left, vertical_borders)\
                    and self.velocity.x < 0:
                self.velocity.x = 0
            self.index = 7
        elif pygame.sprite.spritecollideany(self.left, vertical_borders) and self.velocity.x < 0 or\
                pygame.sprite.spritecollideany(self.right, vertical_borders) and self.velocity.x > 0:
            self.jump = 0
            self.animation_frames = 7
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
            self.animation_frames = 7
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

    
class Fireball(AnimatedSprite):
    def __init__(self, x, y, sheet=load_image("cn.png"), columns=1, rows=1, f=10):
        super().__init__(sheet, columns, rows, x + 20, y + 20, f)
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


class Enemy(AnimatedSprite):
    def __init__(self, sheet=load_image("en.png"), columns=1, rows=1, x=500, y=500, f=10):
        super().__init__(sheet, columns, rows, x, y, f)
        self.velocity.x = -1
        self.mask = pygame.mask.from_surface(self.image)
    
    def death(self):
        global shot
        if pygame.sprite.collide_mask(self, shot):
            all_sprites.remove(shot)
            all_sprites.remove(self)
            enemies.remove(self)
            shot = None
        
    def update(self):
        global shot
        if shot is not None:
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


class Potion(AnimatedSprite):
    def __init__(self, x, y, sheet=load_image("p.png"), columns=1, rows=1, f=10):
        super().__init__(sheet, columns, rows, x, y, f)
        self.mask = pygame.mask.from_surface(self.image)
        
    def drink(self):
        if pygame.sprite.collide_mask(self, player):
            player.count += 3
            all_sprites.remove(self)
            potions.remove(self)
            sound4.play()
    
    def update(self):
        self.drink()
        self.update_frame_dependent()


class Object(AnimatedSprite):
    def __init__(self, sheet, x, y, columns=1, rows=1, f=10):
        super().__init__(sheet, columns, rows, x, y, f)
        self.mask = pygame.mask.from_surface(self.image)
    
    def taking(self):
        if pygame.sprite.collide_mask(self, player):
            player.nm += 1
            all_sprites.remove(self)
            things.remove(self)
            sound4.play()
    
    def update(self):
        self.taking()
        self.update_frame_dependent()    


class PlayerConstraint(pygame.sprite.Sprite):
    def __init__(self, x, y, down=None, right=None):
        super().__init__()  # all_sprites)
        self.down = down
        self.right = right
        if self.down is not None:
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
        if self.down is not None:
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
        super().__init__()  # all_sprites)
        if ability:
            self.add(green_borders)
            self.image = pygame.Surface([x2 - x1, 2])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 2)
            self.image.fill(pygame.Color('green'))
        else:
            if x1 == x2:  # вертикальная стенка
                self.add(vertical_borders)
                self.image = pygame.Surface([3, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 3, y2 - y1)
            else:  # горизонтальная стенка
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 2])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 2)
            self.image.fill(pygame.Color('red'))


is_game = True
while is_game:
    pygame.init()
    sound1 = pygame.mixer.Sound('sound/2.wav')
    sound2 = pygame.mixer.Sound('sound/1.wav')
    sound3 = pygame.mixer.Sound('sound/3.wav')
    sound4 = pygame.mixer.Sound('sound/4.wav')
    width, height = size = 900, 580
    running = True
    
    screen = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()
    shot = None
    all_sprites = pygame.sprite.Group()
    start_screen()
    enemies = pygame.sprite.Group(Enemy())
    things = pygame.sprite.Group(Object(load_image('t.png'), 300, 500),
                                 Object(load_image('t.png'), 700, 500))
    potions = pygame.sprite.Group(Potion(400, 500))
    green_borders = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    Border(5, 5, 1000 - 5, 5)
    Border(5, 600 - 35, 1000 - 5, 600 - 35)
    Border(112, 474, 290, 474, True)
    Border(112, 392, 290, 392, True)
    Border(112, 302, 290, 302, True)
    Border(112, 218, 290, 218, True)
    Border(112, 136, 290, 136, True)
    Border(230, 474, 290, 474)
    Border(240, 302, 290, 302)
    Border(112, 302, 145, 302)

    Border(112, 50, 290, 50)

    Border(108, 50, 108, 474)
    Border(290, 219, 290, 565)

    Border(400, 450, 500, 450, True)
    Border(5, 5, 5, 600 - 5)
    player = Player()
    Border(1000 - 5, 5, 1000 - 5, 600 - 5)
    fond = load_image('plan.png')
    screen.blit(fond, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.velocity.x = 4
                    player.index = 0
                elif event.key == pygame.K_1:
                    player.lives = 0
                elif event.key == pygame.K_a:
                    player.velocity.x = -4
                    player.index = 0
                elif event.key == pygame.K_s:
                    player.down = True
                elif event.key == pygame.K_w:
                    player.velocity.y = -4
                    player.index = 0
                elif event.key == pygame.K_SPACE:
                    if shot is None and player.count > 0:
                        shot = Fireball(*player.rect[:2])
                        player.count -= 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    player.velocity.x = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity.y = 0
        if shot is not None:
            shot.update()
        screen.blit(fond, (0, 0))
        player.update()
        enemies.update()
        potions.update()
        things.update()
        all_sprites.draw(screen)
        clock.tick(100)
        pygame.display.flip()
    if is_game:
        end_screen("Конец 'игры', вы выиграли")
pygame.quit()
