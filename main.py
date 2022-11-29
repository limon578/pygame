import random
import pygame
import sprites


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Amoeba Jump')

   # Отрисовка шривтов
        self.high_score = 0
        self.big_font = pygame.freetype.Font('Font.ttf', 75)
        self.middle_font = pygame.freetype.Font('Font.ttf', 40)
        self.small_font = pygame.freetype.Font('Font.ttf', 25)

        self.on_ground = True
        self.speed = 0
        self.player = None
        self.menu()
        pygame.quit()

    def draw_menu_header(self):
        # Вывод на экран меню названия игры
        text_surface, rect = self.big_font.render('Amoeba Jump', (0, 0, 0))
        self.screen.blit(text_surface, (250, 200))

        # Вывод на экран меню счетчика очков
        text_surface, rect = self.small_font.render(f'Highscore: {self.high_score}', (0, 0, 0))
        self.screen.blit(
            text_surface,
            (
                (self.screen.get_rect().w - rect.w) / 2,
                300,
            ),
        )

   # Отрисовка окаймлающих прямоугольников в меню
    def draw_overlay(self):
        pygame.draw.rect(self.screen, (123, 104, 238), (0, 0, 150, 800), 0)
        pygame.draw.rect(self.screen, (123, 104, 238), (650, 0, 150, 800), 0)
        pygame.draw.rect(self.screen, (139, 0, 139), (0, 0, 150, 800), 10)
        pygame.draw.rect(self.screen, (139, 0, 139), (650, 0, 150, 800), 10)

    def menu(self):

        play_button = sprites.Button(400, 540, 'Play', self.middle_font)
        menu_run = True
        while menu_run:

            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.be_inside(pos[0], pos[1]):
                        menu_run = self.game()

            play_button.update(pos[0], pos[1])

            self.screen.fill((127, 255, 212))
            self.draw_overlay()
            self.draw_menu_header()
            self.screen.blit(play_button.image, play_button.rect)
            pygame.display.flip()

            self.clock.tick(20)

    def draw_result(self, score):
        text_surface, rect = self.small_font.render(f'Score: {score}', (0, 0, 0))
        self.screen.blit(text_surface, (20, 50))

    def boundaries(self, platforms):
    # Обработка касаний между платформой и игроком
        for platform in platforms.sprites():
            # Условия касания с правой и левой границей, проверка нахождения игрока выше верхней поверхности платформы
            if (
                    self.player.rect.right >= platform.rect.left and
                    self.player.rect.left <= platform.rect.right and
                    platform.rect.bottom >= self.player.rect.bottom >= platform.rect.top
            ):
                if self.speed >= 0:
                    self.speed = 0
                    self.on_ground = True

        # Увеличиваем скорость, если игрок не стоит на земле
        if not self.on_ground:
            self.speed += 1

    def game(self):

        game_run = True
        # Переменная power отвечает за силу прыжка
        power = 10
        next_level = 10

        self.player = sprites.Sprite(400, 500, 50, 50, 'amoeba.png')
        score = 0

        platforms = pygame.sprite.Group(
            [sprites.Sprite(random.randint(217, 550), (i * 100) + 100, 130, 40, 'plat.png') for i in range(10)]
        )
        upper_platform = platforms.sprites()[0]

        self.speed = 0
        self.on_ground = True
        fail = False

        while game_run:
           # Перемещение персонажа вправо и влево
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += 5

            if keys[pygame.K_LEFT]:
                self.player.rect.x -= 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False

            if self.on_ground:
                self.speed = -power
                self.on_ground = False

            self.player.rect.y += self.speed

           # Увеличение количества платформ, задание размера платформы (длина,ширина)
            if upper_platform.rect.y > power * 10:
                upper_platform = sprites.Sprite(random.randint(217, 550), 0, 130, 40, 'plat.png')
                platforms.add(upper_platform)

            for platform in platforms.sprites():
                # Если значение скорости меньше 0 и если игрок вблизи 300 по у, то платформы должны двигаться вниз
                if self.speed < 0:
                    if self.player.rect.y < 300:
                        platform.rect.y -= self.speed * 2
                    platform.rect.y -= self.speed
                if platform.rect.y >= 800:
                    platform.kill()
                    # Добавление очков в сслучае уничтожения платформы, когда она выходит за границу экрана
                    score += 1

            self.screen.fill((176, 196, 222))
            self.draw_overlay()
            self.draw_result(score)
            self.screen.blit(self.player.image, self.player.rect)
            platforms.draw(self.screen)
            self.boundaries(platforms)

            if self.player.rect.y >= 800:
                # Обновление результата заработанных очков
                if score > self.high_score:
                    self.high_score = score
                game_run = False
                fail = True

            if score > next_level:
                next_level += 10
                power += 1

            pygame.display.flip()
            self.clock.tick(60)

        return fail


Game()