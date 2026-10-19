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


@pytest.mark.smoke
def test_example_register():
    """Author: <example>. Smoke: a new user can register."""
    assert Users().register("newuser", "password123") is True


# ---- YOUR SMOKE TESTS (at least 5) ----
@pytest.mark.smoke
def test_register_user():
    """Author: Sai Smoke: a new user can register."""
    users = Users()
    assert users.register("newuser", "password123") is True


@pytest.mark.smoke
def test_login_works():
    """Author: Sai Smoke: a registered user can log in."""
    users = Users()
    users.register("alice", "password123")
    assert users.login("alice", "password123") is True


@pytest.mark.smoke
def test_add_product_to_catalog():
    """Author: Sai Smoke: a product can be added to the catalog."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    assert "B1" in catalog.products


@pytest.mark.smoke
def test_add_product_to_cart():
    """Author: Sai Smoke: a valid product can be added to the cart."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    cart = Cart(catalog)
    assert cart.add("B1") is True
    assert cart.items == ["B1"]


@pytest.mark.smoke
def test_checkout_cart():
    """Author: Sai Smoke: checkout saves the order."""
    catalog = Catalog()
    catalog.add_product("B1", "Python Book", 10)
    cart = Cart(catalog)
    cart.add("B1")

    assert cart.checkout() == ["B1"]
    assert cart.items == []


# ---- YOUR REGRESSION TESTS (the bug hunt) ----

# ---- YOUR SLOW TESTS (at least 2) ----
