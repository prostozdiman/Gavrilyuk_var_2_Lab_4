import random
import os

class Game:
    def __init__(self, size=20):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.ship = Ship(self)
        self.planet = Planet(self)
        self.obstacles = []  # Инициализация пустого списка препятствий
        self.generate_obstacles()
        self.running = True

    def generate_obstacles(self):
        self.obstacles = [Obstacle(self) for _ in range(random.randint(2, 4))]

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Очищаем экран перед каждым ходом
        for row in self.grid:
            print(" ".join(row))

    def update_grid(self):
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        
        self.planet.place_on_grid()
        for obstacle in self.obstacles:
            obstacle.place_on_grid()
        self.ship.place_on_grid()

    def check_collision(self):
        ship_x, ship_y = self.ship.position
        
        # Проверяем столкновение с препятствиями
        for obstacle in self.obstacles:
            if obstacle.check_collision(ship_x, ship_y):
                print("\n🚨 Корабель розбився об перешкоду! Гра закінчена. 🚀💥")
                self.running = False
                return
        
        # Проверяем, достигли ли планеты
        if self.planet.check_landing(ship_x, ship_y):
            print("\n🎉 Вітаємо! Ви успішно посадили корабель на планету! 🌍🚀")
            self.running = False

    def run(self):
        while self.running:
            self.update_grid()
            self.display()
            self.ship.move()
            self.check_collision()
        print("Гра завершена!")

class Ship:
    def __init__(self, game):
        self.game = game
        self.position = (random.randint(0, game.size - 1), random.randint(0, game.size - 1))

    def place_on_grid(self):
        x, y = self.position
        self.game.grid[y][x] = 'S'

    def move(self):
        try:
            x, y = map(int, input("\nВведіть координати для руху (x y): ").split())
            if 0 <= x < self.game.size and 0 <= y < self.game.size:
                self.position = (x, y)
            else:
                print("❌ Некоректний рух! Введіть координати в межах поля.")
        except ValueError:
            print("❌ Некоректний ввід! Введіть два числа.")

class Planet:
    def __init__(self, game):
        self.game = game
        self.size = random.randint(4, 5)
        self.x = random.randint(0, game.size - self.size)
        self.y = random.randint(0, game.size - self.size)

    def place_on_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.game.grid[self.y + i][self.x + j] = 'P'

    def check_landing(self, x, y):
        return self.x - 1 <= x <= self.x + self.size and self.y - 1 <= y <= self.y + self.size

class Obstacle:
    def __init__(self, game):
        self.game = game
        self.size = random.randint(1, 3)
        while True:
            self.x = random.randint(0, game.size - self.size)
            self.y = random.randint(0, game.size - self.size)
            if not self._is_too_close_to_other_obstacles():
                break

    def _is_too_close_to_other_obstacles(self):
        for obstacle in self.game.obstacles:
            if abs(self.x - obstacle.x) < 3 and abs(self.y - obstacle.y) < 3:
                return True
        return False

    def place_on_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.game.grid[self.y + i][self.x + j] = 'X'

    def check_collision(self, x, y):
        return self.x - 1 <= x <= self.x + self.size and self.y - 1 <= y <= self.y + self.size

if __name__ == "__main__":
    game = Game()
    game.run()
