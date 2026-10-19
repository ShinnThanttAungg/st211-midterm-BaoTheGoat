# FINDINGS.md -- Bug-hunt log

One entry per bug, five maximum, ~150 words each. Copy the block per bug.
Marks are for the Observed/Expected pair being specific and checkable.

Group: <name>   Members: <names>

---

## Bug 1
- **Suspected:** <which function, and what made you suspicious>
- **Tried:** <the input or test you used>
- **Observed:** <the actual, wrong result -- paste it>
- **Expected:** <the correct behaviour, and why that is correct>
- **Fixed:** <what you changed>
- **Author:** <name>

---

## Bug 2
(copy the block above per bug)

## Bug 5
- **Suspected:** Cart.total() in bookstore_app/cart.py. The loop uses range(len(self.items) - 1), which may skip the final product.
- **Tried:** Added three products to the cart with prices 10, 20, and 5, then checked cart.total().
- **Observed:** The original buggy code returned 30.
- **Expected:** The total should be 35, because 10 + 20 + 5 = 35.
- **Fixed:** Changed the loop to iterate through every product ID in ``` self.items ``` .
- **Author:** Sai Lin Thant Maung 
