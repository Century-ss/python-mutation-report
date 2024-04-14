class Product:
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price


class Shop:
    def __init__(self, name: str) -> None:
        self.name = name
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def list_products(self) -> list[Product]:
        return self.products
