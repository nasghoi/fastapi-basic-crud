from pydantic import BaseModel

class Product(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
    
    