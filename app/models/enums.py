import enum


class ProductCategory(str, enum.Enum):
    electronics = "electronics"
    books = "books"
    clothing = "clothing"
    food = "food"
    other = "other"