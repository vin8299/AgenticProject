from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float
    quantity: int

product = Product(name="Laptop", price=75000, quantity=2)
print(product.price) # 75000.0

# You can also add rules:
class Prod(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=1)

# Now this is invalid:
Prod(name="Laptop", price=-500, quantity=1)
# because the rules say: price > 0, quantity >= 1