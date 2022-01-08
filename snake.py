import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right"
        self.new_direction = []
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()

        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body = ImageTk.PhotoImage(Image.open("snek.png"))
            
            self.food = ImageTk.PhotoImage(Image.open("fod.png"))
            
        except IOError as error:
            print(error)
            window.destroy()

    def create_objects(self):
        self.create_text(
            45,
            12,
            text=f"Score: {self.score}",
            tag="score",
            fill="#fff",
            font=("digital-7", 14)
        )
        for x, y in self.snake_positions:
            self.create_image(x, y, image=self.snake_body, tag="snake")
        self.create_image(self.food_position[0], self.food_position[1], image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    def move_snake(self):
        if self.new_direction:
            self.direction = self.new_direction.pop(0)
        
        head_x, head_y = self.snake_positions[0]
        if self.direction == "Right":
            new_head_position = (head_x + MOVE_INCREMENT, head_y)
        elif self.direction == "Down":
            new_head_position = (head_x, head_y + MOVE_INCREMENT)
        elif self.direction == "Left":
            new_head_position = (head_x - MOVE_INCREMENT, head_y)
        elif self.direction == "Up":
            new_head_position = (head_x, head_y - MOVE_INCREMENT)
        
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            return
        self.check_food_eaten()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x, head_y = self.snake_positions[0]

        return(
            head_x in (0, 600)
            or head_y in (20, 620)
            or (head_x, head_y) in self.snake_positions[1:]
        )
    
    def on_key_press(self, e):
        key_pressed = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if(
            key_pressed in all_directions
            and {key_pressed, self.direction} not in opposites
        ):
            self.new_direction.append(key_pressed)

    def check_food_eaten(self):
        if self.snake_positions[0] == self.food_position:
            
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
            
            self.food_position = self.set_new_food_position()
            food = self.find_withtag("food")
            self.coords(food, self.food_position)

            self.score += 1
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}")

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

            
window = tk.Tk()
window.title("Snake")
window.resizable(False, False)

game = Snake()
game.pack()

window.mainloop()
