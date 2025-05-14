from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import sqlite3
from pydantic import BaseModel
from datetime import datetime

# Request body models
class Item(BaseModel):
    name: str
    price: float

class Customer(BaseModel):
    name: str
    phone: int

class Orders(BaseModel):
    customer_id: int
    notes: str

# DB connection
connection = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = connection.cursor()

# FastAPI app
app = FastAPI()

# Root redirect to docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# ------------------ ITEMS ------------------

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    cursor.execute("SELECT * FROM items WHERE id=?;", (item_id,))
    item = cursor.fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "name": item[1], "price": item[2]}

@app.post("/items")
async def add_item(item: Item):
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (item.name, item.price))
    connection.commit()
    return {"id": cursor.lastrowid, "name": item.name, "price": item.price}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    cursor.execute("UPDATE items SET name=?, price=? WHERE id=?;", (item.name, item.price, item_id))
    connection.commit()
    return {"id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    cursor.execute("DELETE FROM items WHERE id=?;", (item_id,))
    connection.commit()
    return {"message": "Item deleted successfully"}

# ------------------ CUSTOMERS ------------------

@app.get("/customers/{customer_id}")
async def get_customer(customer_id: int):
    cursor.execute("SELECT * FROM customers WHERE id=?;", (customer_id,))
    customer = cursor.fetchone()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": customer[0], "name": customer[1], "phone": customer[2]}

@app.post("/customer")
async def add_customer(customer: Customer):
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    connection.commit()
    return {"id": cursor.lastrowid, "name": customer.name, "phone": customer.phone}

@app.put("/customers/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    cursor.execute("UPDATE customers SET name=?, phone=? WHERE id=?;", (customer.name, customer.phone, customer_id))
    connection.commit()
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    cursor.execute("SELECT * FROM orders WHERE customer_id=?;", (customer_id,))
    if cursor.fetchone():
        return {"message": "Cannot delete. Remove related orders first."}
    cursor.execute("DELETE FROM customers WHERE id=?;", (customer_id,))
    connection.commit()
    return {"message": "Customer deleted successfully"}

# ------------------ ORDERS ------------------

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    cursor.execute("SELECT * FROM orders WHERE id=?;", (order_id,))
    order = cursor.fetchone()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": order[0], "timestamp": order[1], "customer_id": order[2], "notes": order[3]}

@app.post("/orders")
async def add_order(order: Orders):
    current_timestamp = int(datetime.now().timestamp())
    cursor.execute("INSERT INTO orders (timestamp, customer_id, notes) VALUES (?, ?, ?);",
                   (current_timestamp, order.customer_id, order.notes))
    connection.commit()
    return {"id": cursor.lastrowid, "timestamp": current_timestamp,
            "customer_id": order.customer_id, "notes": order.notes}

@app.put("/orders/{order_id}")
async def update_order(order_id: int, order: Orders):
    current_timestamp = int(datetime.now().timestamp())
    cursor.execute("UPDATE orders SET timestamp=?, customer_id=?, notes=? WHERE id=?;",
                   (current_timestamp, order.customer_id, order.notes, order_id))
    connection.commit()
    return {"id": order_id, "timestamp": current_timestamp,
            "customer_id": order.customer_id, "notes": order.notes}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    cursor.execute("DELETE FROM orders WHERE id=?;", (order_id,))
    connection.commit()
    return {"message": "Order deleted successfully"}
