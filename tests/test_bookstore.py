"""Your test suite. Write smoke, regression, and slow tests here.

Every test MUST carry exactly one marker (@pytest.mark.smoke / regression /
slow) and name its author in the docstring, e.g.:

    @pytest.mark.smoke
    def test_login_works():
        '''Author: <name>. Smoke test for login.'''

Run:  pytest            (all)     pytest -m smoke     pytest -m regression
"""
import time
import pytest
from bookstore_app import Users, Catalog, Cart

def make_cart(*prices):
    cat = Catalog()
    for i, price in enumerate(prices):
        cat.add_book(i, f"Book {i}", price)
    return cat, Cart(cat)

# --- SMOKE TESTS (must PASS on shipped code) ---
@pytest.mark.smoke
def test_example_register():
    """Author: <example>. Smoke: a new user can register."""
    assert Users().register("newuser", "password123") is True

def test_register_new_user_then_duplicate_rejected():
    """Author: <name>. Smoke: registration works and is stored."""
    u = Users()
    assert u.register("alice", "secret1") is True
    assert "alice" in u.users
    assert u.register("alice", "other") is False

@pytest.mark.smoke
def test_login_correct_ok_wrong_rejected():
    """Author: <name>. Smoke: right password logs in, wrong one does not."""
    u = Users(); u.register("alice", "secret1")
    assert u.login("alice", "secret1") is True
    assert u.login("alice", "wrongpw") is False   # catches 'accepts any password'
    assert u.login("nobody", "secret1") is False

@pytest.mark.smoke
def test_add_product_is_saved_and_searchable():
    """Author: <name>. Smoke: a product added is really stored."""
    cat = Catalog()
    cat.add_product(1, "Python", 30)
    assert 1 in cat.products
    assert cat.products[1]["price"] == 30
    assert cat.search("Python") == [1]

@pytest.mark.smoke
def test_add_to_cart_reaches_cart():
    """Author: <name>. Smoke: item actually lands in the cart."""
    cat, cart = make_cart(10)
    assert cart.add(1) is True
    assert cart.items == [1]
    assert cart.add(999) is False

@pytest.mark.smoke
def test_checkout_nonempty_cart_produces_order():
    """Author: <name>. Smoke: checkout returns the order and empties the cart."""
    cat, cart = make_cart(10, 20)
    cart.add(1); cart.add(2)
    order = cart.checkout()
    assert order == [1, 2]
    assert cart.items == []
    assert cart.history() == [[1, 2]]

# ---- REGRESSION TESTS (must FAIL on shipped code) ----
@pytest.mark.regression
def test_cart_total_includes_last_item():
    """Author: <name>. Cart.total skipped the last item. 10+20+5 must be 35."""
    cat, cart = make_cart(10, 20, 5)
    for pid in (1, 2, 3):
        cart.add(pid)
    assert cart.total() == 35

@pytest.mark.regression
def test_checkout_empty_cart_returns_none():
    """Author: <name>. Cart.checkout on an empty cart should return None
    and not record an order; it returned [] and logged an empty order."""
    cart = Cart(Catalog())
    assert cart.checkout() is None
    assert cart.history() == []

@pytest.mark.regression
def test_import_products_returns_exact_count():
    """Author: <name>. Cart.import_products returned count+1; 2 imported must be 2."""
    cart = Cart(Catalog())
    assert cart.import_products([(1, "A", 5), (2, "B", 6)]) == 2

@pytest.mark.regression
def test_login_password_special_characters():
    """Author: Aung Thet Khine. Check that login rejects an incorrect password."""
    users = Users()
    users.register("student1", "hello123")

    assert users.login("student1", "hello@123") is False

@pytest.mark.regression
def test_catalog_search_case_insensitive():
    """Author: Aung Thet Khine. Check that searching ignores uppercase and lowercase."""
    catalog = Catalog()
    catalog.add_product(1, "Python Programming", 500)

    assert 1 in catalog.search("python")

# ---- SLOW TESTS ----
@pytest.mark.slow
def test_import_fifty_thousand_products():
    """Author: <name>. Slow: bulk-imports 50,000 products, then searches them."""
    cart = Cart(Catalog())
    data = [(i, f"Book {i}", 1) for i in range(50_000)]
    assert cart.import_products(data) == 50_000      # fails until bug 3 is fixed; fine for slow
    assert len(cart.catalog.products) == 50_000

@pytest.mark.slow
def test_many_cart_operations_in_a_loop():
    """Author: <name>. Slow: 20,000 add/total cycles over a large catalog."""
    cat = Catalog()
    for i in range(2000):
        cat.add_product(i, f"Book {i}", 2)
    cart = Cart(cat)
    for i in range(20_000):
        cart.add(i % 2000)
    assert len(cart.items) == 20_000
    assert len(cat.search("Book 19")) > 0            # full scan of the catalog