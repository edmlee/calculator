import tkinter as tk
import customtkinter as ck


WIDTH = 360
HEIGHT = 580
BUTTON_GAP = 10
BUTTON_CORNER_RADIUS = 20

DISPLAY_FONT = ("Arial", 30)
DIGIT_FONT = ("Arial", 25)
OPERATOR_FONT = ("Arial", 25)
CLEAR_FONT = ("Arial", 20)
SPECIAL_FONT = ("Arial", 18)

global button_size
button_size = int((WIDTH - BUTTON_GAP * 5) / 4)

ck.set_appearance_mode("dark")
ck.set_default_color_theme("blue")

class Calculator:
    def __init__(self):
        self.root = ck.CTk()
        self.root.title("Calculator")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.number_buttons = {}
        self.operators = {"/":"\u00F7","*":"\u00D7", "-":"\u2212", "+":"+", "=":"="}
        self.bottom_buttons = [0, "."]
        self.number = ""
        self.equation = ""
            
        self.display()
        self.digit_position()
        self.create_operator_button()
        self.create_clear_button()
        self.create_backspace_button()
        self.create_percentage_button()
        self.create_plus_minus_button()


    def display(self):
        self.entry = ck.CTkEntry(self.root, placeholder_text=0, placeholder_text_color="white", justify="right", 
                                 width=WIDTH-BUTTON_GAP*2, height=100, text_font=DISPLAY_FONT)
        self.entry.grid(row=0, column=0, columnspan=4, padx=(BUTTON_GAP, 0), pady=10)


    def clear_display(self):
        self.entry.delete(0, tk.END)


    def update_display(self, digit):
        self.number = str(self.entry.get()) + str(digit)

        # Only allow 1 decimal point
        if self.number.count(".") > 1:
            self.number = self.number[:-1]

        # Add a zero to leading decimal point
        elif len(self.entry.get()) == 0 and str(digit) == ".":
            self.number = self.number[:-1]
            self.entry.insert(0, "0.")

        # Delete leading zero if it is the first digit entered
        elif len(self.entry.get()) == 1 and self.number[0] == "0" and "." not in self.number:
            self.clear_display()
            self.entry.insert(0, self.number[1:])
        else:
            self.clear_display()
            self.entry.insert(0, self.number)


    def calculate(self, operator):
        self.equation += self.number
        if self.equation[-1] not in list(self.operators.values())[:-1]:
            self.equation += operator
        else:
            self.equation = self.equation[:-1] + operator
        self.clear_display()
        self.number = ""
        print(self.equation)

        if operator == "=":
            self.entry.insert(0, eval(self.equation[:-1]))
            print(eval(self.equation[:-1]))
            self.equation = ""


    def digit_position(self):
        digit_row = 1
        digit_column = 3

        # Digits [1-9]
        for digit in range(9, 0, -1):
            if digit % 3 == 0:
                digit_row += 1
                digit_column = 2
            
            self.create_digit_button(digit_row, digit_column, digit)
            digit_column -= 1

        # Digit 0 and the decimal point
        digit_column = 1
        for digit in self.bottom_buttons:
            self.create_digit_button(5, digit_column, digit)
            digit_column += 1      


    def create_digit_button(self, digit_row, digit_column, digit):
        self.number_buttons[digit] = ck.CTkButton(self.root, text=f"{digit}", width=button_size, height=button_size, 
                                                  corner_radius=BUTTON_CORNER_RADIUS, text_font=DIGIT_FONT, 
                                                  command=lambda digit=digit: self.update_display(digit))
        self.number_buttons[digit].grid(row=digit_row, column=digit_column, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))        


    def create_operator_button(self):
        operator_button = {}
        count_x = 1
        for operator, value in self.operators.items():
            operator_button[operator] = ck.CTkButton(self.root, text=f"{value}", width=button_size, height=button_size, 
                                                     corner_radius=BUTTON_CORNER_RADIUS, text_font=OPERATOR_FONT, 
                                                     command=lambda operator=operator: self.calculate(operator))
            operator_button[operator].grid(row=count_x, column=3, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))
            count_x += 1


    def create_clear_button(self):
        button = ck.CTkButton(self.root, text=f"C", width=button_size, height=button_size, 
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=CLEAR_FONT, command=self.clear_display)
        button.grid(row=1, column=0, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))


    def backspace_display(self):
        self.entry.delete(len(self.number) - 1, tk.END)
        self.number = self.number[:-1]


    def create_backspace_button(self):
        button = ck.CTkButton(self.root, text=f"\u232b", width=button_size, height=button_size, 
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=SPECIAL_FONT, command=self.backspace_display)
        button.grid(row=5, column=0, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))


    def create_percentage_button(self):
        button = ck.CTkButton(self.root, text=f"%", width=button_size, height=button_size, 
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=SPECIAL_FONT, command=self.backspace_display)
        button.grid(row=1, column=1, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))


    def create_plus_minus_button(self):
        button = ck.CTkButton(self.root, text=f"\u00B1", width=button_size, height=button_size, 
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=SPECIAL_FONT, command=self.backspace_display)
        button.grid(row=1, column=2, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))


if __name__ == "__main__":
    calculator = Calculator()
    calculator.root.mainloop()