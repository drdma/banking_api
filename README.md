# banking API

## Overview
3 relational tables to store customers information, accounts and transactions.

### List all customers
- added "identification" field for storing e.g. passport numbers to distinguish between customers with same names for example

**Definition**

`GET /customers`

**Response**

`200 OK` on success

```json
[
    {"customers": {
        "id": 1,
        "name": "Thomas Anderson",
        "identification": "a232fdb9-c7c5-4ad0-b8df-e606bff483e6"
    }}
]
```

`404 Not Found` on error

Note: not adding list all accounts and list all transactions functionalities for
security reasons. Only allow viewing of single account and transactions related to an account.

**Definition**

`POST /customers`

**Arguments**

- `"first_name": string` customer's first name (not case sensitive)
- `"surname": string` customer's last name (not case sensitive)
- `"identification": string` customer's identification document number

**Response**

`201 created` on success

```json
[
    {"SUCCESS": {
      "message": "customer added",
      "id": 1,
      "name": "Thomas Anderson",
      "identification": "a232fdb9-c7c5-4ad0-b8df-e606bff483e6"
    }}
]
```

`400 Bad Request` on error
- if customer already exists in database
- if missing argument
- if unknown error


### Create a new bank account for a customer, with an initial deposit amount. A single customer may have multiple bank accounts.

**Definition**

`POST /accounts`

**Arguments**

- `"first_name": string` customer's first name (not case sensitive)
- `"surname": string` customer's last name (not case sensitive)
- `"identification": string` customer's identification document number
- `"balance": float` initial deposit

**Response**

`201 created` on success

```json
[
    {"SUCCESS": {
        "message": "New account added",
        "id": 1,
        "balance": 100,
        "customer_id": 1,
        "name": "Thomas Anderson",
    }}
]
```

`400 Bad Request` on error
- if customer does not exist in database
- if missing argument
- if unknown error

### Transfer amounts between any two accounts, including those owned by different customers.

**Definition**

`POST /transactions`

**Arguments**

- `"account_id_from": integer` account id transferring from
- `"account_id_to": integer` account id transferring to
- `"amount": float` transfer amount (cannot be negative)

**Response**

`201 created` on success

```json
[
    {
      "uuid": "0734c20c-5807-4f20-8233-e1a861df8eea",
      "account_id_from": 1,
      "account_id_to": 2,
      "amount": 10.50,
      "transaction_timestamp": 2020-10-10 13:30:02
    }
]
```
`400 Bad Request` on error
- if account does not exist in database
- if amount is negative
- if missing argument
- if unknown error

### Retrieve balances for a given account.

**Definition**

`GET /account/<account_id>`

**Response**

`200 OK` on success

```json
[
    {"SUCCESS": {
        "message": "account 1 retreived",
        "balance": 100
    }}
]
```

`404 Not Found` on error
- if account does not exist in database


### Retrieve transfer history for a given account.

**Definition**

`GET /account/<account_id>/transactions`

**Response**

`200 OK` on success

```json
[
    {"transactions":{
        "uuid": "0734c20c-5807-4f20-8233-e1a861df8eea",
        "account_id_from": 1,
        "account_id_to": 2,
        "amount": 10.50,
        "transaction_timestamp": "2020-10-10 13:30:02"
    }}
]
```

`404 Not Found` on error

## Future work

- use MySQL or Postgres instead of sqlite, depends on exact application
- put limit on negative balance on accounts in transaction requests
- consider storing balance as integer to prevent rounding error (then divide by 100) e.g. store 10.50 as 1050
- more endpoints + routes (e.g. view all accounts, delete account etc.)
- login credentials to view all accounts, transactions