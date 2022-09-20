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
DEFAULT_COLOUR = "gray90"

global button_size
button_size = int((WIDTH - BUTTON_GAP * 5) / 4)
ck.set_appearance_mode("dark")
ck.set_default_color_theme("blue")


class Calculator:
    def __init__(self):
        self.root = ck.CTk()
        self.root.title("Calculator")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.operators = {"/":"\u00F7","*":"\u00D7", "-":"\u2212", "+":"+", "=":"="}
        self.bottom_buttons = [0, "."]
        self.number = ""
        self.equation = ""
            
        self.display()
        self.digit_position()
        self.create_operator_buttons()
        self.create_special_buttons()


    def display(self):
        self.entry = ck.CTkEntry(self.root, placeholder_text="0", placeholder_text_color=DEFAULT_COLOUR, justify="right", 
                                 width=WIDTH-BUTTON_GAP*2, height=100, text_font=DISPLAY_FONT)
        self.entry.grid(row=0, column=0, columnspan=4, padx=(BUTTON_GAP, 0), pady=10)


    def clear_display(self):
        self.entry.delete(0, tk.END)
        self.number = ""
        self.equation = ""


    def update_display(self, digit):
        self.number += str(digit)
      
        # Delete leading zero if it is the first digit entered
        if self.number[0] == "0" and len(self.number) > 1 and "." not in self.number:
            self.number = str(digit)
            self.entry.insert(0, self.number)

        # Only allow 1 decimal point
        if self.number.count(".") > 1:
            self.number = self.number[:-1]

        # Add a zero to leading decimal point
        elif len(self.number) == 1 and str(digit) == ".":
            self.number = "0."
            self.entry.insert(0, self.number)
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.number)


    def calculate(self, operator):
        self.equation += self.number
        try:
            if len(self.equation) != 0:
                if self.equation[-1] not in list(self.operators.keys())[:-1]:
                    self.equation += operator
                else:
                    # Replace existing operator with the most recent operator
                    self.equation = self.equation[:-1] + operator
                self.entry.delete(0, tk.END)
                self.number = ""

                # Calculate final answer and remove floating point from integers
                if operator != "=":
                    self.equation = str(eval(self.equation[:-1])) + operator
                    if self.equation[-3:-1] == ".0":
                        self.equation = self.equation.replace(".0", "")            
                    self.entry.insert(0, self.equation[:-1])

                else:
                    self.equation = str(eval(self.equation[:-1]))
                    self.equation = self.remove_floating_point(self.equation)       
                    self.entry.insert(0, self.equation)
                    self.equation = ""
            # Reset display
            elif len(self.equation) == 0 and operator == "=":
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "0")
        except ZeroDivisionError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")


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
        button = ck.CTkButton(self.root, text=f"{digit}", width=button_size, height=button_size, 
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=DIGIT_FONT, 
                              command=lambda digit=digit: self.update_display(digit))
        button.grid(row=digit_row, column=digit_column, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))        


    def create_operator_buttons(self):
        count_x = 1
        for operator, value in self.operators.items():
            button = ck.CTkButton(self.root, text=f"{value}", width=button_size, height=button_size, 
                                 corner_radius=BUTTON_CORNER_RADIUS, text_font=OPERATOR_FONT, 
                                 command=lambda operator=operator: self.calculate(operator))
            button.grid(row=count_x, column=3, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))
            count_x += 1


    def create_button(self, text, row, column, command):
        button = ck.CTkButton(self.root, text=text, width=button_size, height=button_size, 
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=SPECIAL_FONT, command=command)
        button.grid(row=row, column=column, padx=(BUTTON_GAP, 0), pady=(BUTTON_GAP, 0))

    
    def create_special_buttons(self):
        self.create_button(text="C", row=1, column=0, command=self.clear_display)
        self.create_button(text=f"\u232b", row=5, column=0, command=self.backspace_display)
        self.create_button(text=f"\u00b9\u2044\u2093", row=1, column=1, command=self.fraction)
        self.create_button(text=f"\u00B1", row=1, column=2, command=self.plus_minus)


    def backspace_display(self):
        self.entry.delete(len(self.number) - 1, tk.END)
        self.number = self.number[:-1]


    def fraction(self):
        self.number = self.entry.get()
        try:
            if len(self.number) != 0:
                self.number = 1 / float(self.number)
                self.number = self.remove_floating_point(self.number)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.number)
                self.number = ""
        except ZeroDivisionError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")


    def plus_minus(self):
        self.number = self.entry.get()
        if len(self.number) != 0:
            self.number = float(self.number)* -1
            self.number = self.remove_floating_point(self.number)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.number)


    def remove_floating_point(self, number):
        if str(number)[-2:] == ".0":
            number = str(number)[:-2] 
        else:
            number = str(number)
        return number


if __name__ == "__main__":
    calculator = Calculator()
    calculator.root.mainloop()