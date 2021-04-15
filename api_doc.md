# GET PRODUCT API


## 1. Get by Key

>http://127.0.0.1:8000/api/products/get_product_by_key?key=2

Type: Get


## 2. GET ALL OF OWNER (ALL TILL NOW)

>http://127.0.0.1:8000/api/products/get_product_by_key

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
