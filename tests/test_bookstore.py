"""Your test suite. Write smoke, regression, and slow tests here.

Every test MUST carry exactly one marker (@pytest.mark.smoke / regression /
slow) and name its author in the docstring, e.g.:

    @pytest.mark.smoke
    def test_login_works():
        '''Author: <name>. Smoke test for login.'''

Run:  pytest            (all)     pytest -m smoke     pytest -m regression
"""
import pytest
from bookstore_app import Users, Catalog, Cart


def make_cart(*prices):
    """Helper: make a catalog and cart with products of the given prices."""
    catalog = Catalog()
    for product_id, price in enumerate(prices, start=1):
        catalog.add_product(product_id, f"product {product_id}", price)
    return catalog, Cart(catalog)

# ---- SMOKE TESTS (core functionality) ----
@pytest.mark.smoke
def test_register_user_and_reject_duplicates():
    """Author: Ethan. Smoke: a new user can register. And registration of a duplicate username is rejected."""
    users = Users()
    assert users.register("newuser", "password123") is True
    assert "newuser" in users.users
    assert users.register("newuser", "dummiebot321") is False


@pytest.mark.smoke
def test_login_works_and_rejects_invalid_credentials():
    """Author: Ethan. Smoke: a registered user can log in. Also checks that login rejects invalid credentials."""
    users = Users()
    users.register("alice", "password123")
    assert users.login("alice", "password123") is True
    assert users.login("alice", "dummiebot321") is False
    assert users.login("bob", "password123") is False  # unregistered user

@pytest.mark.smoke
def test_add_to_cart_and_puts_item_in_cart():
    """Author: Ethan. Smoke: a product can be added to the cart and is reflected in the cart's items."""
    _, cart = make_cart(10, 20)
    assert cart.add(1) is True
    assert cart.items == [1]
    assert cart.add(999) is False  # non-existent product
    assert cart.items == [1]  # cart should remain unchanged

@pytest.mark.smoke
def test_add_product_is_saved_and_findable():
    """Author: Ethan. Smoke: a product can be added to the catalog and is findable."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    assert catalog.products["B1"] == {"title": "Python Book", "price": 10}
    assert catalog.search("Python") == ["B1"]
    assert "B1" in catalog.products

@pytest.mark.smoke
def test_checkout_nonempty_cart_and_saves_order_and_empties_cart():
    """Author: Ethan. Smoke: checkout saves the order and empties the cart."""
    _, cart = make_cart(10, 20)
    cart.add(1)
    cart.add(2)
    order = cart.checkout()
    assert order == [1, 2]
    assert cart.items == []
    assert cart.history() == [[1, 2]]

@pytest.mark.smoke
def test_checkout_history_accumulates_across_orders():
    """Author: Ethan. Smoke: each checkout is appended to the order history."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    catalog.add_product("B2", "JavaScript Book", 15)
    cart = Cart(catalog)
    cart.add("B1")
    first = cart.checkout()
    cart.add("B2")
    second = cart.checkout()
    assert first == ["B1"] and second == ["B2"]
    assert cart.history() == [["B1"], ["B2"]]

# ---- REGRESSION TESTS (the bug hunt) ----

@pytest.mark.regression
def test_login_password_special_characters():
    """Author: Aung Thet Khine. Check that login rejects an incorrect password."""
    users = Users()
    users.register("student1", "hello@123")
    assert users.login("student1", "hello@123") is True
    assert users.login("student1", "hello123@") is False

@pytest.mark.regression
def test_catalog_search_case_insensitive():
    """Author: Aung Thet Khine. Check that searching ignores uppercase and lowercase."""
    catalog = Catalog()
    catalog.add_product(1, "Python Programming", 500)
    assert 1 in catalog.search("python")
    assert 1 in catalog.search("PYTHON")

@pytest.mark.regression
def test_cart_total_includes_all_items():
    """Author: Aung Thet Khine. Check that the total price of the cart includes all items."""
    _, cart = make_cart(10, 20, 30)
    for product_id in [1, 2, 3]:
        cart.add(product_id)
    assert cart.total() == 60  # 10 + 20 + 30
    _, single_cart = make_cart(15)
    single_cart.add(1)
    assert single_cart.total() == 15  # Only one item in the cart

@pytest.mark.regression
def test_cart_checkout_empty_cart():
    """Author: Aung Thet Khine. Check that checkout returns an empty list for an empty cart."""
    catalog = Catalog()
    cart = Cart(catalog)

    assert cart.checkout() == [] or None  # Should return an empty list for an empty cart
    assert cart.history() == [] # History should remain empty

@pytest.mark.regression
def test_cart_checkout_empty_cart():
    """Author: Ethan. Check that checkout returns an empty list for an empty cart."""
    catalog = Catalog()
    cart = Cart(catalog)

    assert cart.checkout() == None  # Should return an empty list for an empty cart
    assert cart.history() == [] # History should remain empty

@pytest.mark.regression
def test_import_products_returns_exact_count():
    """Author: Ethan. Check that importing products returns the exact count of imported products."""
    cart = Cart(Catalog())
    assert cart.import_products([(1, "A", 5), (2, "B", 6)]) == 2
    assert cart.import_products([]) == 0

# ---- SLOW TESTS ----
@pytest.mark.slow
def test_bulk_import_stores_twenty_thousand_products():
    """Author: Sai. Slow: import and verify 20,000 products."""
    catalog = Catalog()
    cart = Cart(catalog)
    product_count = 20_000

    products = [
        (product_id, f"book {product_id}", 100)
        for product_id in range(product_count)
    ]

    # Slow: processes 20,000 records through the real import method.
    imported_count = cart.import_products(products)

    # Assert
    assert imported_count == product_count
    assert len(catalog.products) == product_count
    assert set(catalog.products.keys()) == set(range(product_count))

    for product_id, title, price in products:
        assert catalog.products[product_id] == {
            "title": title,
            "price": price,
        }


@pytest.mark.slow
def test_repeated_searches_return_correct_products_in_large_catalog():
    """Author: Sai. Slow: 3,000 searches across 10,000 products."""
    # Arrange
    catalog = Catalog()
    product_count = 10_000
    search_count = 3_000

    for product_id in range(product_count):
        if product_id % 100 == 0:
            title = f"python book {product_id}"
        else:
            title = f"history book {product_id}"

        catalog.add_product(product_id, title, 100)

    expected_ids = set(range(0, product_count, 100))

    # Act and Assert
    # Slow: approximately 30 million product checks in total.
    for _ in range(search_count):
        actual_ids = catalog.search("python")

        assert len(actual_ids) == len(expected_ids)
        assert set(actual_ids) == expected_ids

@pytest.mark.slow
def test_search_remains_correct_as_catalog_grows():
    """Author: Sai. Slow: search remains correct as catalog grows from 1,000 to 10,000 products."""
    catalog = Catalog()
    product_count = 10_000
    search_keyword = "python"

    for product_id in range(product_count):
        if product_id % 100 == 0:
            title = f"python book {product_id}"
        else:
            title = f"history book {product_id}"

        catalog.add_product(product_id, title, 100)

        if (product_id + 1) % 1000 == 0:
            expected_ids = set(range(0, product_id + 1, 100))
            actual_ids = catalog.search(search_keyword)

            assert len(actual_ids) == len(expected_ids)
            assert set(actual_ids) == expected_ids

@pytest.mark.slow
def test_cart_import_and_checkout_large_number_of_products():  
    """Author: Sai. Slow: import and checkout a large number of products."""
    catalog = Catalog()
    cart = Cart(catalog)
    product_count = 5_000

    products = [
        (product_id, f"book {product_id}", 100)
        for product_id in range(product_count)
    ]

    # Import products
    imported_count = cart.import_products(products)
    assert imported_count == product_count
    assert len(catalog.products) == product_count

    # Add all products to the cart
    for product_id in range(product_count):
        assert cart.add(product_id) is True

    # Checkout
    order = cart.checkout()
    assert len(order) == product_count
    assert set(order) == set(range(product_count))

@pytest.mark.slow
def test_many_users_register_and_login():
    """Author: Divine. Slow: register and login 400,000 users."""
    users = Users()
    user_count = 400_000

    for i in range(user_count):
        assert users.register(f"user{i}", f"password{i}") is True

    for i in range(user_count):
        assert users.login(f"user{i}", f"password{i}") is True
        assert users.login(f"user{i}", f"xx{i}") is False
        assert users.login(f"user{i}", f"dummybot") is False
    assert len(users.users) == user_count

@pytest.mark.slow
def test_two_hundred_thousand_checkouts_keeps_every_order():
    """Author: Divine. Slow: checkout 200,000 times and verify order history."""
    catalog = Catalog()
    order_count = 200_000

    for product_id in range(50):    
        catalog.add_product(product_id, f"book {product_id}", 10)
    
    cart = Cart(catalog)
    expected_orders = []

    for order_id in range(order_count):
        batch = [(order_id + offset) % len(catalog.products) for offset in range(3)]
        for product_id in batch:
            cart.add(product_id)
        assert cart.checkout() == batch
        assert cart.items == []
        expected_orders.append(batch)
    assert cart.history() == expected_orders

@pytest.mark.slow
def test_random_cart_operations_match_a_simple_model():
    """Author: Divine. Slow: perform 1,000,000 random cart operations and verify the cart's state matches a simple model."""
    state = 211

    def rand(n):
        nonlocal state
        state = (state * 1103515245 + 12345) % (2**31)
        return (state >> 16) % n

    operations = ["add", "add", "add", "remove", "checkout", "bad_add"]
    catalog = Catalog()
    for product_id in range(100):
        catalog.add_product(product_id, f"book {product_id}", 5)
    cart = Cart(catalog)
    model_items, model_orders = [], []
    for _ in range(1_000_000):
        op = operations[rand(len(operations))]
        product_id = rand(100)
        if op == "add":
            assert cart.add(product_id) is True
            model_items.append(product_id)
        elif op == "bad_add":
                    assert cart.add(10_000 + product_id) is False
        elif op == "remove":
            present = product_id in model_items
            assert cart.remove(product_id) is present
            if present:
                model_items.remove(product_id)
        elif model_items:       # only checkout if there are items in the cart
            assert cart.checkout() == model_items
            model_orders.append(model_items)
            model_items = []
        assert cart.items == model_items
    assert cart.history() == model_orders

# Bonus Mark Try
@pytest.mark.slow
def test_search_all_mixed_case_bulk_results_remain_complete():
    """Author: Ethan. Slow regression: mixed-case bulk searches stay complete."""
    catalog = Catalog()
    product_count = 20_000
    title_variants = ("Python", "PYTHON", "python", "PyThOn")
    queries = ("python", "PYTHON", "PyThOn", "pYtHoN")
    expected_ids = set(range(0, product_count, 10))

    for product_id in range(product_count):
        if product_id % 10 == 0:
            word = title_variants[(product_id // 10) % len(title_variants)]
            title = f"{word} book {product_id}"
        else:
            title = f"History book {product_id}"
        catalog.add_product(product_id, title, 100)

    for attempt in range(10_000):
        query = queries[attempt % len(queries)]
        actual_ids = catalog.search(query)
        assert len(actual_ids) == len(expected_ids), (attempt, query)
        assert set(actual_ids) == expected_ids, (attempt, query)

    assert catalog.search("no-such-title") == []
    