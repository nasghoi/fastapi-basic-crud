from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hai, kau datang di saat yang tak tepat"

products = [
    Product(id=1, name="Phone", description="Entry phone", price=600, quantity=30),
    Product(id=2, name="Phone", description="Mid-Tier phone", price=1700, quantity=15),
    Product(id=3, name="Phone", description="Flagship phone", price=3700, quantity=10),
    Product(name="Laptop", description="Flagship laptop", id=4, price=3950, quantity=3),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()
    count = db.query(database_models.Product).count()
    
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

    db.commit()
        
init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # names = ""
    # for product in products:
    #     names += product.name + ", "
    # return names.rstrip(", ")
    db_products = db.query(database_models.Product).order_by(database_models.Product.id).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):

    # dua cara, filter atau get
    # get only works with primary key, filter can work with any column
    # For other columns, Big O depends on whether the column has an index.
    # A filter on an unindexed column scans the whole table, which is O(n).
    # Add index=True on columns you filter often.
    
    # db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    db_product = db.get(database_models.Product, id)
    if db_product:
        return db_product
    return "Item not found"

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    # products.append(product)
    products = db.query(database_models.Product).order_by(database_models.Product.id).all()
    return products

@app.patch("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    # for p in products:
    #     if p.id == id:
    #         for field, value in product.model_dump(exclude_unset=True, exclude={"id"}).items():
    #             setattr(p, field, value)
    #         return {"message": "Item updated successfully", "item": p}
    # return "Item not found"
    db_product = db.get(database_models.Product, id)
    if not db_product:
        return "Item not found"
    for field, value in product.model_dump(exclude_unset=True, exclude={"id"}).items():
        setattr(db_product, field, value)
    db.commit()
    
    return {"message": "Item updated successfully", "item": db_product}

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    # for p in products:
    #     if p.id == id:
    #         products.remove(p)
    #         return {"message": "Item deleted successfully", "item": products}
    # return "Item not found"
    db_product = db.get(database_models.Product, id)
    if not db_product:
        return "Item not found"
    db.delete(db_product)
    db.commit()
    
    return {"message": "Item deleted successfully"}
