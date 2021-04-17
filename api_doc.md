# GET PRODUCT API


## 1. Get by Key

    api/products/get_product?key=2

Type: Get


## 2. GET ALL OF OWNER (ALL TILL NOW)

>http://127.0.0.1:8000/api/products/get_product

Type: Get


## 3. UPDATE PRODUCT

>http://127.0.0.1:8000/api/products/update_product?key=1

Type: Patch

```
{
    "name":"newName1"
}

```

## 4. Create Product

>http://127.0.0.1:8000/api/products/create_product

Type: Put

```
{
    "name": "big item",
    "code": "777",
    "currency": "Rs.",
    "price": "110",
    "quantity": 50,
    "qr_code": "{SDsdsdsdsc}"
}
```

## 5. Delete Product

>http://127.0.0.1:8000/api/products/delete_product?key=1

Type: Delete

## 6. Create User

>http://127.0.0.1:8000/api/accounts/create_user

Type: post

This will return a JWT 

```
{

    "email": "password@gmail.com",
    "username":"pass122",
    "password":"password",
    "mobile_number": "56563",
    "first_name": "pass",
    "last_name": "word"

}
```

## 7. Login User

>http://127.0.0.1:8000/api/accounts/login_user

Type: post

```
{
    "username": "tokens1@gmail.com",
    "password":"password"
}
```