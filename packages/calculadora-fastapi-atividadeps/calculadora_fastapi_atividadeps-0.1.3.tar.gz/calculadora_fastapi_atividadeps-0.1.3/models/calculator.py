# models/calculator.py
class Calculator:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def add(self):
        return self.value1 + self.value2

    def subtract(self):
        return self.value1 - self.value2

    def multiply(self):
        return self.value1 * self.value2

    def divide(self):
        if self.value2 != 0:
            return self.value1 / self.value2
        else:
            return "Error: Division by zero is not allowed."