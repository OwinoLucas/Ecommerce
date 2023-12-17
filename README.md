# Ecommerce application
This is a ecommerce application with authentication and payment options(Paypal and MPESA) with shipping options.

## Screenshots
Store Page 
![Screenshot from 2023-12-16 20-03-56](https://github.com/OwinoLucas/Ecommerce/assets/60548928/385a6582-a4b0-407a-b79c-20173bfb1197)


Cart Page
![Screenshot from 2023-12-16 19-38-24](https://github.com/OwinoLucas/Ecommerce/assets/60548928/e1e03ceb-371a-4036-b456-651bfa7a8af9)

Checkout Page
![Screenshot from 2023-12-16 19-38-58](https://github.com/OwinoLucas/Ecommerce/assets/60548928/b7bb2f6d-b9e0-4121-920c-f9309e154ddd)

### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First
```
$  pip install virtualenv
```

Create Virtual Environment

For Windows
```
$  python -m venv venv
```
For Mac
```
$  python3 -m venv venv
```
For Linux
```
$  virtualenv .
```

Activate Virtual Environment

For Windows
```
$  source venv/scripts/activate
```

For Mac
```
$  source venv/bin/activate
```

For Linux
```
$  source bin/activate
```

**3. Clone this project**
```
$  git clone https://github.com/OwinoLucas/Ecommerce.git
```

Then, Enter the project
```
$  cd Ecommerce
```

**4. Install Requirements from 'requirements.txt'**
```python
$  pip3 install -r requirements.txt
```

**5. Run migrations and migrate**
```python manage.py makemigrations```
```python manage.py migrate```

**6. Now Run Server**

Command for PC:
```python
$ python manage.py runserver
```

Command for Mac:
```python
$ python3 manage.py runserver
```

Command for Linux:
```python
$ python3 manage.py runserver
```

**7. Login Credentials**

Create Super User
Command for PC:
```
$  python manage.py createsuperuser
```

Command for Mac:
```
$  python3 manage.py createsuperuser
```

Command for Linux:
```
$  python3 manage.py createsuperuser
```
