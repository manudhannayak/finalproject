# Dosa Restaurant Backend API (FastAPI + SQLite)

This project is a RESTful API backend for a Dosa restaurant. It is built using **FastAPI** and **SQLite**, supporting full **CRUD operations** on:

-  Items (Menu)
-  Customers
-  Orders

The API includes automatic timestamping for orders and a root redirect to the Swagger UI docs (`/docs`).

---

##  Features

- FastAPI-based REST API
- SQLite lightweight database
- Auto-generated documentation via Swagger UI
- Auto timestamping for new and updated orders
- Clean and modular codebase
- Error handling and validations

---

##  Project Setup
1. Clone the Repository

```bash
git clone https://github.com/manudhannayak/finalproject.git
cd finalproject
```
2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate 
```
3. Install Dependencies
```bash
pip install fastapi uvicorn pydantic
```
4. Initialize the Database
```bash
python init_db.py
```
5. Running the Server
```bash
uvicorn main:app --reload
```

After this you will get a link to access Swagger UI API 

