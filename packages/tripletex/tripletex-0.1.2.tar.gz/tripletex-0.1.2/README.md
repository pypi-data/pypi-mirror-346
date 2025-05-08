# tripletex

An efficient and user-friendly Python library crafted specifically for seamless integration with [Tripletex](https://www.tripletex.no)'s accounting and financial management APIs.

## Features

- Easy authentication with the Tripletex API
- Access to invoices, customers, projects, and more
- Clean and extensible design for integration into your own systems

## Installation

```bash
pip install tripletex
```


## Usage
```python
from tripletex import TripletexClient

client = TripletexClient(token="your_token_here")
customers = client.customers.list()
```

