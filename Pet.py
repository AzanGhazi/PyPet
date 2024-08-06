import pygame

class Item:
    def __init__(self, x, y, health, happiness, image_name) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.happiness = happiness
        self.image = pygame.image.load(image_name)

        rect = self.image.get_rect()
        self.image_rect = pygame.Rect(x - rect.width/2, y - rect.height/2, rect.width, rect.height)

class Pet:
    def __init__(self, x, y, health, max_health, happiness, max_happiness) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.happiness = happiness
        self.max_health = max_health
        self.max_happiness = max_happiness
        self.color = pygame.Color(0, happiness, 0)
    
    def get_pos(self):
        return pygame.Vector2(self.x, self.y)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.health, self.y - self.health, self.health * 2, self.health * 2)
    # Increases/decreases x and/or y
    def move(self, x_amount, y_amount):
        self.x += x_amount
        self.y += y_amount

    def consume_item(self, item):
        self.update_happiness(item.happiness)
        self.update_health(item.health)


    def update_health(self, health):
        self.health += health
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health <0:
            self.health = 0
    


    def update_happiness(self, happiness):
        self.happiness += happiness
        if self.happiness > self.max_happiness:
            self.happiness = self.max_happiness
        elif self.happiness <0:
            self.happiness = 0
        self.color = pygame.Color(0, self.happiness, 0)

    # Checks end game conditions
    def check_if_dead(self):
        return self.health <= 0 or self.happiness <= 0


class Game:
    def __init__(self) -> None:
        self.width = 500
        self.height = 500
        self.background_color = "white"
        self.buttons_bar_height = 100
        self.buttons_bar_colour = "orange"

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Pet")

        self.clock_tick = 60
        self.clock = pygame.time.Clock()
        # Item variables
        self.image_names = ["apple.png", "icecream.png", "toy.png"]
        self.item_mode_index = 0
        self.item = None
        
        # Button variables
        self.apple_button = Item(self.width / 4, self.buttons_bar_height / 2, 0, 0, self.image_names[0])
        self.icecream_button = Item(2*self.width / 4, self.buttons_bar_height / 2, 0, 0, self.image_names[1])
        self.toy_button = Item(3*self.width / 4, self.buttons_bar_height / 2, 0, 0, self.image_names[2])
        # Creates our pet
        self.pet = Pet(self.width / 2, self.height / 2, 50, 100, 180, 255)
        self.speed = 2
        self.d_x = 0
        self.d_y = 0
        self.decay_rate = -1
        self.current_tick = 0
        self.health_update_rate = self.clock_tick / 3
        self.colour_update_rate = self.clock_tick / 10



    
    def handle_mouse_click(self):
        pos = pygame.mouse.get_pos()

        if self.apple_button.image_rect.collidepoint(pos):
            self.item_mode_index = 0
        elif self.icecream_button.image_rect.collidepoint(pos):
            self.item_mode_index = 1
        elif self.toy_button.image_rect.collidepoint(pos):
            self.item_mode_index = 2
        elif pos[1] < self.buttons_bar_height:
            return
        else:
            self.create_item(pos)
    
    def create_item(self, pos):
        if self.item_mode_index == 0:
            self.item = Item(pos[0], pos[1], 20, 0, self.image_names[0])
        elif self.item_mode_index == 1:
            self.item = Item(pos[0], pos[1], -10, 60, self.image_names[1])
        elif self.item_mode_index == 2:
            self.item = Item(pos[0], pos[1], 0, 40, self.image_names[2])
        self.set_speed()

    def set_speed(self):
        # Gets differences in x and y positions of pet and item
        d_x = abs(self.pet.x - self.item.x)
        d_y = abs(self.pet.y - self.item.y)
        
        # Checks whether x difference is greater than y difference
        if d_x >= d_y:
            self.d_x = self.speed
            # Slows down the y movement
            self.d_y = self.speed * (d_y / d_x)
        else:
            # Slows down the x movement instead
            self.d_x = self.speed * (d_x / d_y)
            self.d_y = self.speed
            
        # Sets x speed to negative if item is further left than pet
        if self.pet.x > self.item.x:
            self.d_x = -self.d_x
        # Sets y speed to negative if item is further up than pet
        if self.pet.y > self.item.y:
            self.d_y = -self.d_y
    
    # Updates pet position
    def update_pet(self):
        self.pet.move(self.d_x, self.d_y)
        self.current_tick +=1
        if self.current_tick % self.health_update_rate == 0:
            self.pet.update_health(self.decay_rate)
        if self.current_tick % self.colour_update_rate:
            self.pet.update_happiness(self.decay_rate)
        if self.current_tick == 60:
            self.current_tick = 0



    def handle_item_collision(self):
        if self.item != None and self.item.image_rect.colliderect(self.pet.get_rect()):
            self.pet.consume_item(self.item)
            self.item = None
            self.d_x = 0
            self.d_y = 0
    






    def draw_canvas(self):
        self.screen.fill(self.background_color)
        # Buttons bar
        pygame.draw.rect(self.screen, self.buttons_bar_colour, pygame.Rect(0, 0, self.width, self.buttons_bar_height))
    
        # Buttons
        self.screen.blit(self.apple_button.image, self.apple_button.image_rect)
        self.screen.blit(self.icecream_button.image, self.icecream_button.image_rect)
        self.screen.blit(self.toy_button.image, self.toy_button.image_rect)

        # Item
        if self.item != None:
            self.screen.blit(self.item.image, self.item.image_rect)
        # Pet
        pygame.draw.circle(self.screen, self.pet.color, self.pet.get_pos(), self.pet.health)
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()

            self.handle_item_collision()
            # Updates pet
            if self.pet.check_if_dead():
                pygame.quit()
                return
      
            self.update_pet()
            self.draw_canvas()

            self.clock.tick(self.clock_tick)
            
#Initialize Pygame
pygame.init()

#Create game
game = Game()
game.run()