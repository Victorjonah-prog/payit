import enum

class Gender(enum.Enum):
    M = "M"
    F = "F"

class OrderStatus(enum.Enum):
    pending = "pending"
    delivered = "delivered"

class Category(enum.Enum):
    grains = "grains"
    tubers = "tubers"
    cereals = "cereals"
    fruits = "fruits"
    livestock = "livestock"
    vegetables = "vegetables"
    oils = "oils"
    latex = "latex"

category_names=["grains","tubers","cereals","fruits","livestock","vegetables","oils","latex"]