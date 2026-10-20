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
    for pid, price in enumerate(prices, start=1):
        catalog.add_product(pid, f"product {pid}", price)
    return catalog, Cart(catalog)

# ---- YOUR SMOKE TESTS (at least 5) ----
@pytest.mark.smoke
def test_register_user_and_reject_duplicates():
    """Author: Sai. Smoke: a new user can register. And registration of a duplicate username is rejected."""
    users = Users()
    assert users.register("newuser", "password123") is True
    assert "newuser" in users.users
    assert users.register("newuser", "dummiebot321") is False


@pytest.mark.smoke
def test_login_works_and_rejects_invalid_credentials():
    """Author: Sai. Smoke: a registered user can log in. Also checks that login rejects invalid credentials."""
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
    """Author: Sai. Smoke: a product can be added to the catalog and is findable."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    assert catalog.products["B1"] == {"title": "Python Book", "price": 10}
    assert catalog.search("Python") == ["B1"]
    assert "B1" in catalog.products

@pytest.mark.smoke
def test_add_product_to_cart():
    """Author: Sai. Smoke: a valid product can be added to the cart via catalog."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    cart = Cart(catalog)
    assert cart.add("B1") is True
    assert cart.items == ["B1"]

@pytest.mark.smoke
def test_checkout_nonempty_cart_and_saves_order_and_empties_cart():
    """Author: Sai. Smoke: checkout saves the order and empties the cart."""
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
    users.register("student1", "hello123")
    assert users.login("student1", "hello123") is True
    assert users.login("student1", "hello@123") is False

@pytest.mark.regression
def test_catalog_search_case_insensitive():
    """Author: Aung Thet Khine. Check that searching ignores uppercase and lowercase."""
    catalog = Catalog()
    catalog.add_product(1, "Python Programming", 500)
    assert 1 in catalog.search("python")
    assert 1 in catalog.search("PYTHON")

@pytest.mark.regression
def test_cart_total_includes_all_items():
    """Author: Ethan. Check that the total price of the cart includes all items."""
    _, cart = make_cart(10, 20, 30)
    for pid in [1, 2, 3]:
        cart.add(pid)
    assert cart.total() == 60  # 10 + 20 + 30
    _, single_cart = make_cart(15)
    single_cart.add(1)
    assert single_cart.total() == 15  # Only one item in the cart

@pytest.mark.regression
def test_cart_checkout_empty_cart():
    """Author: Ethan. Check that checkout returns an empty list for an empty cart."""
    catalog = Catalog()
    cart = Cart(catalog)

    assert cart.checkout() == None  # Should return an empty list for an empty cart
    assert cart.history() == [] # History should remain empty

@pytest.mark.regression
def test_cart_add_and_remove_product():
    """Author: Ethan. Check that adding and removing a product works correctly."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    cart = Cart(catalog)

    assert cart.add("B1") is True
    assert "B1" in cart.items

    assert cart.remove("B1") is True
    assert "B1" not in cart.items

@pytest.mark.regression
def test_cart_add_and_remove_nonexistent_product():
    """Author: Ethan. Check that adding or removing a nonexistent product returns False."""
    catalog = Catalog()
    cart = Cart(catalog)

    assert cart.add("nonexistent_product") is False
    assert cart.remove("nonexistent_product") is False

@pytest.mark.regression
def test_cart_remove_product_and_checkout_multiple_products():
    """Author: Ethan. Check that removing a product and checking out the remaining items works correctly."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    catalog.add_product("B2", "JavaScript Book", 15)
    cart = Cart(catalog)
    cart.add("B1")
    cart.add("B2")

    assert cart.remove("B1") is True
    assert "B1" not in cart.items

    assert cart.checkout() == ["B2"]
    assert cart.items == []

@pytest.mark.regression
def test_import_products_returns_exact_count():
    """Author: Ethan. Check that importing products returns the exact count of imported products."""
    cart = Cart(Catalog())
    assert cart.import_products([(1, "A", 5), (2, "B", 6)]) == 2
    assert cart.import_products([]) == 0

# ---- SLOW TESTS ----
@pytest.mark.slow
def test_bulk_import_stores_twenty_thousand_products():
    """Author: Scott. Slow: import and verify 20,000 products."""
    # Arrange
    catalog = Catalog()
    cart = Cart(catalog)
    product_count = 20_000

    products = [
        (product_id, f"book {product_id}", 100)
        for product_id in range(product_count)
    ]

    # Act
    # Slow: processes 20,000 records through the real import method.
    imported_count = cart.import_products(products)

    # Assert
    assert imported_count == product_count
    assert len(catalog.products) == product_count

    for product_id, title, price in products:
        assert catalog.products[product_id] == {
            "title": title,
            "price": price,
        }


@pytest.mark.slow
def test_repeated_searches_return_correct_products_in_large_catalog():
    """Author: Scott. Slow: 3,000 searches across 10,000 products."""
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
        actual_ids = catalog.search_all("python")

        assert len(actual_ids) == len(expected_ids)
        assert set(actual_ids) == expected_ids

@pytest.mark.slow
def test_search_remains_correct_as_catalog_grows():
    """Author: Ethan. Slow: search remains correct as catalog grows from 1,000 to 10,000 products."""
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
            actual_ids = catalog.search_all(search_keyword)

            assert len(actual_ids) == len(expected_ids)
            assert set(actual_ids) == expected_ids

@pytest.mark.slow
def test_cart_checkout_history_persists():
    """Author: Ethan. Slow: checkout history persists across multiple checkouts."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    catalog.add_product("B2", "JavaScript Book", 15)
    cart = Cart(catalog)

    # First checkout
    cart.add("B1")
    first_order = cart.checkout()
    assert first_order == ["B1"]
    assert cart.history() == [first_order]

    # Second checkout
    cart.add("B2")
    second_order = cart.checkout()
    assert second_order == ["B2"]
    assert cart.history() == [first_order, second_order]

@pytest.mark.slow
def test_cart_import_and_checkout_large_number_of_products():  
    """Author: Ethan. Slow: import and checkout a large number of products."""
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
def test_cart_checkout_empty_cart_returns_none():
    """Author: Ethan. Slow: checkout returns None for an empty cart."""
    catalog = Catalog()
    cart = Cart(catalog)

    result = cart.checkout()
    assert result is None

