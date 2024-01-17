import os
import random
import sys
import pygame
import pytmx


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    # Если изображение уже прозрачно(это обычно бывает у картинок форматов png и gif),
    # то после загрузки вызываем функцию convert_alpha(), и загруженное изображение сохранит прозрачность
    else:
        image = image.convert_alpha()
    return image


# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
pygame.display.set_caption('Три богатыря и Ко')
SIZE = WIDTH, HEIGHT = 1200, 650
screen = pygame.display.set_mode(SIZE)
FPS = 50  # скорость смена 50 кадров в секунду

fon = pygame.transform.scale(load_image('три богатыря заставка.png'), (WIDTH, HEIGHT))
screen.blit(fon, (0, 0))
playlist = ['data/рэп Юлия.mp3', 'data/Кукарача.mp3', 'data/песня Юлия.mp3', 'data/Песня_Юлия.mp3',
            'data/три богатыря.mp3', 'data/песня девиц.mp3']
pygame.mixer.music.load(playlist[0])  # добавление фоновой музыки
playlist.pop(0) # удалили проигрываемую музыку из списка playlist
pygame.mixer.music.play() # проигрываемую музыку 1 раз
pygame.mixer.music.queue(playlist[0])  # постановка музыки в очередь
playlist.pop(0) # удалили проигрываемую музыку из списка


# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
GRAVITY = 0.2
LEVEL_TWO = False
LEVEL_THREE = False
LEVEL_FOUR = False

...
# для отслеживания улетевших частиц
# удобно использовать пересечение прямоугольников
screen_rect = (0, 0, WIDTH, HEIGHT)

class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы (облака) разного размера
    fire = [load_image("облако.png", colorkey=-1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 1
    # возможные скорости
    numbers = range(-5, 15)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def terminate(): # закрытие окна, корректный выход
    pygame.quit()
    sys.exit()


# в главном игровом цикле регулировка музыки
running = True
fps = 10
flPause = False
flStop = False
clock = pygame.time.Clock()
vol = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                flPause = not flPause
                if flPause:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            elif event.key == pygame.K_SPACE:
                if flStop:
                    pygame.mixer.music.stop()
                    flStop = True
                else:
                    pygame.mixer.music.rewind()

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                vol -= 0.2
                pygame.mixer.music.set_volume(vol)
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                vol += 0.2
                pygame.mixer.music.set_volume(vol)

    create_particles((100, 100))
    create_particles((WIDTH - 500, 100))

    all_sprites.update()
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 50))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(fps)


# старт игры
def start_screen():
    intro_text = ["                                  'Три богатыря и Ко'                                                   Возрастные ограничения 3+", "",
                  "квест по мотивам мульфильмов про трех богатырей,",
                  "где осуществляют путешествие",
                  "несколько персонажей к",
                  "поставленной цели путем",
                  "преодоления разнообразных",
                  "трудностей.", "",
                  "                                   Правила игры:", "",
                  "1. Выбор уровня (начать игру сначала(пробел),",
                      "с желаемого уровня(нажатие номера уровня – 1, 2, 3)", "",
                  "2. Регулировка фоновой музыки",
                      "(остановка/воспроизведение(пробел),",
                      "пауза/воспроизведение(ESCAPE),",
                      "уровня громкости(LEFT/RIGHT))", "",
                  "3. Перемещение героя с помощью клавиш (LEFT, RIGTH, UP, DOWN)", "",
                  "4. Возможность переиграть 3 и специальный уровень (при нажатии ESCAPE)"]

    # создание текста надписей на заставке
    font = pygame.font.Font('data/unicephalon.otf', 15)  # загрузим красивый шрифт
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.key.get_pressed()[pygame.K_1]:
                # если была нажата цифра 1
                level_one()  # запускаем 1 уровень игры
            elif pygame.key.get_pressed()[pygame.K_2]:
                # если была нажата цифра 2
                level_two()  # запускаем 2 уровень игры
            elif pygame.key.get_pressed()[pygame.K_3]:
                # если была нажата цифра 3
                level_three()  # запускаем 3 уровень игры
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# список героев для выбора
players_images = ['алеша.png', 'алеша на осле.png', 'добрыня на верблюде.png', 'добрыня никитич.png']
# словарь тайлов для отрисовки карты
tile_images = {'wall'[1]: load_image('дерево.png'), 'wall'[2]: load_image('пенек.png'),
               'empty'[2]: load_image('сосульки.png'), 'empty'[1]: load_image('трава.png')}

player_image = load_image(players_images[2], colorkey=-1)  # наш выбранный герой

portal_image = load_image('дерево портал.png', colorkey=-1)
house_image = load_image('избушка.png', colorkey=-1)
potion_image = load_image('зелье.png', colorkey=-1)
octopus = load_image('осьминог.png', colorkey=-1)
tile_width = tile_height = 50

# основной персонаж
player = None
running = True
clock = pygame.time.Clock()
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()



def load_level(filename): # загрузка карты уровня и прочтение ее построчно в список, т.е. получим список символом,
    # по которым потом будет рисоваться карта
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level): # отрисовка карты картинками-тайлами, x и y показывают где нам надо отступить
    new_player, x, y, portal, mushroom = None, None, None, None, None
    if LEVEL_TWO:
        num = 2
    else:
        num = 1
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty'[num], x, y)
            elif level[y][x] == '#':
                Tile('wall'[num], x, y)
            elif level[y][x] == '&':
                Tile('empty'[num], x, y)
                portal = Portal(x, y)
            elif level[y][x] == '$':
                Tile('empty'[num], x, y)
                house = House(x, y)
            elif level[y][x] == '*':
                Tile('empty'[num], x, y)
                potion = Potion(x, y)
            elif level[y][x] == '@':
                Tile('empty'[num], x, y)
                new_player = Player(x, y) # создаем объект игрока

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, portal, house, potion


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites) #
        self.image = tile_images[tile_type] # загружается тип тайла, вид тайла, т.е. соответствующую картинку
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y) # показывает где размещать конкретно в пикселях

        self.add(tiles_group, all_sprites) # добавляем в группу всех спрайтов, чтобы все сразу отобразить,
        # а в группу тайлов добавляем, потому что у нас есть класс игрока, который будет не тайлом


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

        self.add(player_group, all_sprites)

    def move_up(self):
        self.rect = self.rect.move(0, -tile_height)

    def move_down(self):
        self.rect = self.rect.move(0, tile_height)

    def move_left(self):
        self.rect = self.rect.move(-tile_width, 0)

    def move_right(self):
        self.rect = self.rect.move(tile_height, 0)


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = portal_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        #self.pos = pos_x, pos_y

        self.add(portal_group, all_sprites)

class House(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = house_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

        self.add(house_group, all_sprites)


class Potion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = potion_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

        self.add(potion_group, all_sprites)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def gameower():
    image = load_image("gameover.png", colorkey=-1)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    rect = image.get_rect(left=-WIDTH)

    # в главном игровом цикле
    running = True
    fps = 200
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        # рисуем на экране нашу картинку
        screen.blit(image, rect.topleft)
        if rect[0] != 0:
            rect.move_ip(1, 0)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


def level_one():
    global player_image, screen, LEVEL_TWO
    rename = False
    pygame.display.set_caption('Три богатыря и Ко. Уровень 1. По болотам и лесам.')
    level_map = load_level('level1.txt')  # загружаем 1 уровень
    player, level_x, level_y, portal, house, potion = generate_level(level_map) # отрисовываем уровень

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                # если была нажата стрелка влево
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    player.move_left()
                # если была нажата стрелка вправо
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    player.move_right()
                # если была нажата стрелка вниз
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    player.move_down()
                # если была нажата стрелка вверх
                if pygame.key.get_pressed()[pygame.K_UP]:
                    player.move_up()
            # проверяем столкновение с зельем
            if pygame.sprite.collide_rect(player, potion):
                pass
            # с помощью метода collide_rect проверяем, есть ли столкновение героя с избушкой. Если да, то
            if pygame.sprite.collide_rect(player, house):
                player_group.empty()  # очищаем группу спрайта героя с помощью метода empty
                player_image = load_image(players_images[3], colorkey=-1)  # загружаем у героя другую картинку
                rename = True
                if rename:
                    level_one()
                return player_image, rename

        # с помощью метода collide_rect проверяем, есть ли столкновение героя с порталом. Пока нет столкновения, то
        if not pygame.sprite.collide_rect(player, portal):
            screen.fill((0, 0, 0)) # заливаем поле черным цветом,
            # потом отрисовываем группу тайлов
            tiles_group.draw(screen)
            portal_group.draw(screen)
            house_group.draw(screen)
            potion_group.draw(screen)
            # и только потом отрисовываем игрока
            player_group.draw(screen)
        # Если столкновение есть, то
        else:
            screen = pygame.display.set_mode((630, 750))  # временно уменьшаем размер экрана,
            # чтобы не видно было карту во время анимации
            pygame.display.set_caption('Три богатыря и Ко. Уровень 1. Телепортация.')
            screen.fill((0, 0, 0))  # заливаем поле черным цветом,
            AnimatedSprite(load_image("дерево портал.jpg"), 3, 2, 0, 0)
            # в главном игровом цикле
            running = True
            fps = 5
            cloc = pygame.time.Clock()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        # очищаем все группы, готовим их для нового уровня
                        empty()
                        #return

                        level_two()
                screen.fill((250, 250, 250))
                all_sprites.draw(screen)
                all_sprites.update()
                pygame.display.flip()
                cloc.tick(fps)
            pygame.quit()
        clock.tick(FPS)
        pygame.display.flip()


def empty():
    # очищаем все группы, готовим их для нового уровня
    all_sprites.empty()
    tiles_group.empty()
    portal_group.empty()
    house_group.empty()
    potion_group.empty()
    player_group.empty()


def level_two():
    global LEVEL_TWO
    LEVEL_TWO = True
    pygame.display.set_caption('Три богатыря и Ко. Уровень 2. В Арктике.')
    screen = pygame.display.set_mode(SIZE)
    level_map = load_level('level2.txt')  # загружаем уровень 2
    player, level_x, level_y, portal, house, potion = generate_level(level_map) # отрисовываем уровень

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                # если была нажата стрелка влево
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    player.move_left()
                # если была нажата стрелка вправо
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    player.move_right()
                # если была нажата стрелка вниз
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    player.move_down()
                # если была нажата стрелка вверх
                elif pygame.key.get_pressed()[pygame.K_UP]:
                    player.move_up()
        if pygame.sprite.collide_rect(player, house):  # проверяем на столкновение с избушкой. Если да, то
            screen.fill((250, 250, 250))  # заливаем поле белым цветом,
            # очищаем все группы, готовим их для нового уровня
            empty()
            pygame.display.set_caption('Три богатыря и Ко. Уровень 2. Телепортация.')
            AnimatedSprite(load_image("дракон.png"), 3, 4, 200, 50)

            # в главном игровом цикле
            running = True
            fps = 5
            cloc = pygame.time.Clock()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        all_sprites.empty()
                        level_catch_up() # вызываем уровень Догонялки в пустыне
                create_particles((100, 100))  # запускаем поверх экрана облака
                create_particles((WIDTH - 400, 100))  # запускаем поверх экрана облака
                screen.fill((250, 250, 250))
                all_sprites.draw(screen)
                all_sprites.update()
                pygame.display.flip()
                cloc.tick(fps)

        elif pygame.sprite.collide_rect(player, potion):
            gameower()
            terminate()

        # с помощью метода collide_rect проверяем, есть ли столкновение героя с порталом. Пока нет столкновения, то
        if not pygame.sprite.collide_rect(player, portal):
            screen.fill((0, 0, 0))  # заливаем поле черным цветом,
            # потом отрисовываем группу тайлов
            tiles_group.draw(screen)
            portal_group.draw(screen)
            house_group.draw(screen)
            potion_group.draw(screen)
            # и только потом отрисовываем игрока
            player_group.draw(screen)
            # Если столкновение есть, то
        else:
            # очищаем все группы, готовим их для нового уровня
            empty()
            screen.fill((250, 250, 250))  # заливаем поле белым цветом,
            pygame.display.set_caption('Три богатыря и Ко. Уровень 3. Телепортация.')
            AnimatedSprite(load_image("led.png"), 9, 6, 300, 50)

            # в главном игровом цикле
            running = True
            fps = 5
            cloc = pygame.time.Clock()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        all_sprites.empty()
                        level_three() # переходим на 3 уровень
                create_particles((100, 100))  # запускаем поверх экрана облака
                create_particles((WIDTH - 400, 100))  # запускаем поверх экрана облака
                screen.fill((250, 250, 250))
                all_sprites.draw(screen)
                all_sprites.update()
                pygame.display.flip()
                cloc.tick(fps)
            pygame.quit()
        clock.tick(FPS)
        pygame.display.flip()


def level_three():
    global LEVEL_THREE
    pygame.mixer.music.load(playlist[0])  # добавление фоновой музыки
    pygame.mixer.music.play(-1)  # проигрываемую музыку 1 раз
    pygame.display.set_caption('Три богатыря и Ко. Уровень 3. У морского царя.')
    labyrinth = Labyrinth('level_three.tmx', [902, 903, 904, 905, 906, 968, 969, 970, 971, 972, 1034, 1038, 1076, 1274,
                                              1279, 1340, 1345, 1406, 1411, 1472, 1477, 1538, 1543, 1604, 1670, 1736],
                          970)
    hero = Hero('юлий.png', (12, 5))
    enemy = Enemy('осьминог.png', (35, 18))
    game = Game(labyrinth, hero, enemy)
    LEVEL_THREE = True
    clck = pygame.time.Clock()
    run = True
    game_over = False
    while run:
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                level_three()
            elif event.type == pygame.QUIT:
                run = False
                gameower()
                terminate()
            elif event.type == ENEMY_EVENT_TYPE and not game_over:
                game.move_enemy()
        if not game_over:
            game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        if game.chek_win():
            game_over = True
            show_message(screen, 'Не смешите мои подковы! Победа!')
        if game.chek_lose():
            game_over = True
            show_message(screen, 'Юлий, ты попал!')
        pygame.display.flip()
        clck.tick(FPS)


TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30
MAPS_DIR = 'data'


class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target):
        INF = 1000
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 <= next_y < self.height and \
                    self.is_free((next_x, next_y)) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Hero:
    def __init__(self, pic, position):
        self.x, self.y = position
        self.image = pygame.image.load(f'{MAPS_DIR}/{pic}')

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Enemy:
    def __init__(self, pic, position):
        self.x, self.y = position
        self.image = pygame.image.load(f'{MAPS_DIR}/{pic}')
        self.delay = 100
        # создали таймер с задержкой перемещения для врага
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Game:
    def __init__(self, labyrinth, hero, enemy):
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemy = enemy

    def render(self, screen):
        self.labyrinth.render(screen)
        self.hero.render(screen)
        self.enemy.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.labyrinth.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))  # обновляем координаты нашего персонажа

    def move_enemy(self):
        next_position = self.labyrinth.find_path_step(self.enemy.get_position(),
                                                      self.hero.get_position())
        self.enemy.set_position(next_position)

    def chek_win(self):
        return self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.finish_tile

    def chek_lose(self):
        return self.hero.get_position() == self.enemy.get_position()

def show_message(screen, message):
    font = pygame.font.Font('data/unicephalon.otf', 50)
    text = font.render(message, 1, (50, 70, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def level_catch_up():  # уровень Догонялки в пустыне
    pygame.display.set_caption('Три богатыря и Ко. Специальный уровень. Догонялки в пустыне.')
    labyrinth = Labyrinth('level_spec.tmx', [4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 22, 23, 24, 30, 38, 39, 40, 47, 48, 46],
                          46)
    hero = Hero('верблюд_вася.png', (14, 8))
    enemy = Enemy('змей_горыныч2.png', (26, 18))
    game = Game(labyrinth, hero, enemy)

    clck = pygame.time.Clock()
    run = True
    game_over = False
    while run:
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                level_catch_up()
            if event.type == pygame.QUIT:
                level_two()
            if event.type == ENEMY_EVENT_TYPE and not game_over:
                game.move_enemy()
        if not game_over:
            game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        if game.chek_win():
            game_over = True
            show_message(screen, 'Горыныч, я тебя сделал!')
        if game.chek_lose():
            game_over = True
            show_message(screen, 'Вася, я тебя съем!')
        pygame.display.flip()
        clck.tick(FPS)
    pygame.quit


start_screen() # запускаем заставку
level_one() # вызываем 1 уровень