# Bug-Hunt Findings Log

Group: BaoTheGoat

Members:
- Aung Thet Khine - 6705142032
- Sai Lin Thant Maung - 6705140073
- Shin Thant Aung - 6705140076

---

## Bug 1: Login ignores symbols in the typed password

- **Module / function:** `bookstore_app/users.py` → `Users.login()`
- **Suspected:** `login()` builds `cleaned = "".join(ch for ch in password if ch.isalnum())` and compares the stored password with `cleaned`, not with what the user typed. Symbols are thrown away before the check, so wrong passwords could be accepted and passwords containing symbols could never match.
- **Tried:** Registered `student1` with `hello123` and called `login("student1", "hello@123")`. Then registered `student2` with `p@ss!` and logged in with exactly `p@ss!`.
- **Observed:** `login("student1", "hello@123")` returned `True` (wrong password accepted). `login("student2", "p@ss!")` returned `False` (correct password rejected).
- **Expected:** `False` for `hello@123` because it differs from `hello123`, and `True` for `p@ss!` because it is the exact registered password. Login must compare the typed password exactly.
- **Fixed:** Removed the `cleaned` line and compare `stored == password` directly.
- **Author:** Aung Thet Khine

---

## Bug 2: Product search is case-sensitive

- **Module / function:** `bookstore_app/catalog.py` → `Catalog.search()`
- **Suspected:** The check `keyword in info["title"]` compares letters exactly as typed, so a lowercase keyword should miss a capitalised title.
- **Tried:** Added product 1, title `Python Programming`, price 500. Searched for `python` and for `Python`.
- **Observed:** `search("python")` returned `[]`. `search("Python")` returned `[1]`.
- **Expected:** `search("python")` should return `[1]`. A shopper should find a book whatever the letter case.
- **Fixed:** Compare `keyword.lower() in info["title"].lower()`.
- **Author:** Aung Thet Khine

---

## Bug 3: Cart total skips the last item

- **Module / function:** `bookstore_app/cart.py` → `Cart.total()`
- **Suspected:** The loop uses `range(len(self.items) - 1)`, which stops one item early.
- **Tried:** Added three products priced 10, 20 and 5 to the cart and called `total()`. Then a cart holding one item priced 10.
- **Observed:** `total()` returned `30` for the three items, and `0` for the single item.
- **Expected:** `35` (10 + 20 + 5) and `10`. The total must include every item in the cart.
- **Fixed:** Loop over every product id in `self.items`.
- **Author:** Sai Lin Thant Maung

---

## Bug 4: Checkout of an empty cart records an order

- **Module / function:** `bookstore_app/cart.py` → `Cart.checkout()`
- **Suspected:** The docstring says checkout returns "None if the cart is empty", but the code copies `self.items` and appends it to `self.orders` with no check.
- **Tried:** Created a `Cart` with an empty catalog, called `checkout()` straight away, then looked at `history()`.
- **Observed:** `checkout()` returned `[]` and `history()` returned `[[]]`, so an empty order was stored.
- **Expected:** `checkout()` returns `None` and `history()` stays `[]`. An empty cart should not create an order.
- **Fixed:** Added `if not self.items: return None` at the top of `checkout()`.
- **Author:** Shin Thant Aung

---

## Bug 5: import_products returns one too many

- **Module / function:** `bookstore_app/cart.py` → `Cart.import_products()`
- **Suspected:** The loop counts each product in `count`, but the last line returns `count + 1`.
- **Tried:** Imported two tuples `(1, "A", 5)` and `(2, "B", 6)`, then imported an empty list.
- **Observed:** Two products returned `3`, and the empty list returned `1`.
- **Expected:** `2` and `0`. The docstring says it returns how many were imported.
- **Fixed:** Changed `return count + 1` to `return count`.
- **Author:** Shin Thant Aung

---