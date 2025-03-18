import random
import os

class Гра:
    def __init__(self, розмір=20):
        self.розмір = розмір
        self.поле = [['.' for _ in range(розмір)] for _ in range(розмір)]
        self.космічний_корабель = Корабель(self)
        self.планета = Планета(self)
        self.перешкоди = []  # Ініціалізація порожнього списку перешкод
        self.генерувати_перешкоди()
        self.грає = True

    def генерувати_перешкоди(self):
        self.перешкоди = [Перешкода(self) for _ in range(random.randint(2, 4))]

    def відобразити(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Очищення екрана перед кожним ходом
        for рядок in self.поле:
            print(" ".join(рядок))

    def оновити_поле(self):
        self.поле = [['.' for _ in range(self.розмір)] for _ in range(self.розмір)]
        
        self.планета.розмістити_на_полі()
        for перешкода in self.перешкоди:
            перешкода.розмістити_на_полі()
        self.космічний_корабель.розмістити_на_полі()

    def перевірити_зіткнення(self):
        x_корабля, y_корабля = self.космічний_корабель.позиція
        
        # Перевіряємо зіткнення з перешкодами
        for перешкода in self.перешкоди:
            if перешкода.перевірити_зіткнення(x_корабля, y_корабля):
                print("\n🚨 Корабель розбився об перешкоду! Гра закінчена. 🚀💥")
                self.грає = False
                return
        
        # Перевіряємо, чи досягнуто планети
        if self.планета.перевірити_приземлення(x_корабля, y_корабля):
            print("\n🎉 Вітаємо! Ви успішно посадили корабель на планету! 🌍🚀")
            self.грає = False

    def запустити(self):
        while self.грає:
            self.оновити_поле()
            self.відобразити()
            self.космічний_корабель.рухатися()
            self.перевірити_зіткнення()
        print("Гра завершена!")

class Корабель:
    def __init__(self, гра):
        self.гра = гра
        self.позиція = (random.randint(0, гра.розмір - 1), random.randint(0, гра.розмір - 1))

    def розмістити_на_полі(self):
        x, y = self.позиція
        self.гра.поле[y][x] = 'S'

    def рухатися(self):
        try:
            x, y = map(int, input("\nВведіть координати для руху (x y): ").split())
            if 0 <= x < self.гра.розмір and 0 <= y < self.гра.розмір:
                self.позиція = (x, y)
            else:
                print("❌ Некоректний рух! Введіть координати в межах поля.")
        except ValueError:
            print("❌ Некоректний ввід! Введіть два числа.")

class Планета:
    def __init__(self, гра):
        self.гра = гра
        self.розмір = random.randint(4, 5)
        self.x = random.randint(0, гра.розмір - self.розмір)
        self.y = random.randint(0, гра.розмір - self.розмір)

    def розмістити_на_полі(self):
        for i in range(self.розмір):
            for j in range(self.розмір):
                self.гра.поле[self.y + i][self.x + j] = 'P'

    def перевірити_приземлення(self, x, y):
        return self.x - 1 <= x <= self.x + self.розмір and self.y - 1 <= y <= self.y + self.розмір

class Перешкода:
    def __init__(self, гра):
        self.гра = гра
        self.розмір = random.randint(1, 3)
        while True:
            self.x = random.randint(0, гра.розмір - self.розмір)
            self.y = random.randint(0, гра.розмір - self.розмір)
            if not self._занадто_близько_до_інших():
                break

    def _занадто_близько_до_інших(self):
        for перешкода in self.гра.перешкоди:
            if abs(self.x - перешкода.x) < 3 and abs(self.y - перешкода.y) < 3:
                return True
        return False

    def розмістити_на_полі(self):
        for i in range(self.розмір):
            for j in range(self.розмір):
                self.гра.поле[self.y + i][self.x + j] = 'X'

    def перевірити_зіткнення(self, x, y):
        return self.x - 1 <= x <= self.x + self.розмір and self.y - 1 <= y <= self.y + self.розмір

if __name__ == "__main__":
    гра = Гра()
    гра.запустити()
