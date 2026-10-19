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


# ---- YOU REGRESSION TESTS (the bug hunt) ----

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


# ---- YOUR SLOW TESTS (at least 2) ----
