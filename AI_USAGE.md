# AI Usage Declaration and Audit

**Group:** 
      Bao The Goat  

**Members:**  
| Member | Git Username | File |
|---|---|---|
| Zwe Naing Set | DivineKeraunos | test_deposit.py |
| Aung Thet Khine | AungThetKhine21 | conftest.py |
| Sai Lin That Maung | Sailinthant | test_withdraw.py |
| Shin Thant Aung | ShinnThanttAungg | test_teardown.py |
| Hein Naing Soe | ScottG619 | test_shared.py |

**Part D3 of the midterm — 20 marks.** Part 1 is required but carries no marks;

its absence is an academic-honesty matter. Part 2 is worth 16 (2 per test).

Parts 3 and 4 together are worth 4.

Before you submit, check all eight boxes:
- [ ] Part 1 declaration complete, or the "no AI used" statement written
- [ ] All eight tests appear in the summary table with a verdict
- [ ] All eight have **two** pasted evidence runs (shipped code, and your fixed code)
- [ ] Part 3 coverage table filled in against `FINDINGS.md`
- [ ] Part 4 verdict written, under 400 words
- [ ] Every audit entry names the member who did it
- [ ] No claim made that you cannot demonstrate from pasted output
- [ ] File committed as `AI_USAGE.md` in the repository root

---

## Part 1 — AI usage declaration (required, unmarked)

Every AI tool any member used anywhere in this project. Using AI is allowed.

Not declaring it is not.
| Tool | What we used it for | Where in the project | How we checked it before relying on it |
|---|---|---|---|
| ChatGPT | We used ChatGPT to support our debugging process, identify potential issues in the login and product search functions, and develop regression tests. It also assisted us in understanding Python errors and Git commands. | `bookstore_app/users.py`, `bookstore_app/catalog.py`, `tests/test_bookstore.py`, `FINDINGS.md` | We reviewed the suggested solutions, made necessary adjustments, and used pytest to verify the application behaviour before committing our changes. |
| Claude | We used Claude to review parts of our Python implementation, examine possible errors, and suggest improvements to our testing approach. | Application code and test development | We evaluated the suggestions against our existing implementation and verified relevant changes through testing. |
| Gemini | We used Gemini to clarify software testing concepts, support our understanding of the assignment requirements, and assist with technical documentation. | Test planning and project documentation | We compared the explanations with the assignment instructions and reviewed the written content for accuracy and relevance. |

If you kept prompts worth showing, add them in an appendix at the end of this

file. Do not paste whole conversations.

---

## Part 2 — Audit of the supplied test set (16 marks)

`ai_review/test_ai_generated.py` contains eight tests presented as a finished

AI bug hunt for this bookstore. They are confident and they are not all

correct. Your job is to establish, for each one, what it actually does.

### How to classify a test

A single test run cannot tell you. "Fails against the buggy code" does **not**

mean the test found a bug — a test demanding behaviour the application was

never meant to have also fails. You need two runs, and the pair of results is

what identifies the category:
| Shipped Code | Fixed Code | What This Tells You | Verdict |
|---|---|---|---|
| ❌ FAIL | ✅ PASS | The test failed when the bug existed and passed after the bug was fixed. It successfully detected a real defect. | **Genuine detection** |
| ✅ PASS | ✅ PASS | The test passed before and after the fix. It never noticed the bug, so it provides false confidence. | **Detects nothing** |
| ✅ PASS | ❌ FAIL | The test expected the buggy behaviour. After the bug was fixed, the test broke. | **Locks in the bug** |
| ❌ FAIL | ❌ FAIL | The test failed both before and after the fix. It is testing something unrelated to the bug, or a requirement that does not exist. | **Invented requirement** |

The third row is the one to think hardest about. A test that locks in a bug is

worse than one that detects nothing: a team that trusts its suite will see the

test go red after a correct fix, conclude the fix was wrong, and revert it. The

bug then has a test defending it.

### How to produce the evidence

Run each test twice — once with the application as you received it, once with

your fixes in place. If you have already fixed the code, you can get back to

the shipped state with git:

```bash

\# your fixed code

pytest ai_review/test_ai_generated.py -v | tee /tmp/fixed.txt

\# the code as it was shipped (replace <sha> with your first commit)

git stash

git checkout <sha> -- bookstore_app/

pytest ai_review/test_ai_generated.py -v | tee /tmp/shipped.txt

git checkout HEAD -- bookstore_app/

git stash pop

```

Paste the real output. Not a screenshot, not a retyped summary — the text.

### Marks, per test
| | marks |
|---|---|
| Correct verdict | 1 |
| Both evidence runs pasted, showing the outcome you claim | 1 |

**A claim you cannot demonstrate costs a mark.** If you assert a test is broken

and the output does not support it, you lose more than you would have gained by

leaving the row blank. Check before you write.

### Summary table — fill this in first
| # | Test | What it claims to catch | Shipped | Fixed | Verdict | Auditor |
|---|---|---|---|---|---|---|
| 1 | `test_cart_total_sums_items` | Checks whether the cart calculates the correct total. | FAIL | PASS | Genuine detection | |
| 2 | `test_login_rejects_wrong_password` | Checks whether login rejects an incorrect password. | PASS | PASS | Detects nothing | Aung Thet Khine |
| 3 | `test_search_finds_exact_title` | Checks whether product search finds an exact matching title. | PASS | PASS | Detects nothing | Aung Thet Khine |
| 4 | `test_import_returns_count` | Checks whether importing products returns the correct count. | FAIL | PASS | Genuine detection | |
| 5 | `test_register_duplicate_returns_false` | Checks whether duplicate registration is rejected. | PASS | PASS | Detects nothing | |
| 6 | `test_checkout_empty_returns_none` | Checks whether checkout with an empty cart returns None. | FAIL | PASS | Genuine detection | |
| 7 | `test_add_to_cart_returns_true_for_known_product` | Checks whether adding an existing product to the cart succeeds. | PASS | PASS | Detects nothing | |
| 8 | `test_search_is_limited_to_ten_results` | Checks whether search returns a maximum of ten products. | FAIL | FAIL | Invented requirement | Aung Thet Khine |

### Detail entries

Copy the block below once for each of the eight tests. Do not paste the test

code — it is in the repository and identical for everyone. Reference it by name

and line instead.

---

#### Test: `test_login_rejects_wrong_password`

**Audited by:** Aung Thet Khine

**1. What it claims to catch.**

This test checks whether the application rejects an incorrect password during login. However, it does not check the password-handling issue we identified in `users.py`.

**2. Evidence — against the shipped code**

```text

ai_review/test_ai_generated.py::test_login_rejects_wrong_password PASSED

```

**3. Evidence — against our fixed code**

```text

ai_review/test_ai_generated.py::test_login_rejects_wrong_password PASSED [ 25%]

```

**4. What that pair proves.**

The test passed on both versions, so it did not detect the original login bug. The test only checks an incorrect password and does not cover the special-character handling problem. A stronger regression test should check that passwords are compared exactly, including special characters.

**5. Verdict**
- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_search_finds_exact_title`

**Audited by:** Aung Thet Khine

**1. What it claims to catch.**

This test checks whether the catalog can find a product when the search text matches its title exactly.

**2. Evidence — against the shipped code**

```text

ai_review/test_ai_generated.py::test_search_finds_exact_title PASSED

```

**3. Evidence — against our fixed code**

```text

ai_review/test_ai_generated.py::test_search_finds_exact_title PASSED     [ 37%]

```

**4. What that pair proves.**

The test passed before and after our changes, so it did not detect the case-sensitive search bug in `catalog.py`. The test uses an exact title match instead of checking different uppercase and lowercase combinations. A stronger test should confirm that searching with a different letter case still returns the correct product.

**5. Verdict**
- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_search_is_limited_to_ten_results` (`ai_review/test_ai_generated.py:52`)

**Audited by:** Aung Thet Khine

**1. What it claims to catch.**

This test checks whether the catalog search returns no more than ten matching products.

**2. Evidence — against the shipped code**

```text
FAILED ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results - AssertionError: assert 20 <= 10
```

**3. Evidence — against our fixed code**

```text
FAILED ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results
AssertionError: assert 20 <= 10
```

**4. What that pair proves.**

The test failed in both versions because the catalog returned twenty matching products. The `search()` function in `bookstore_app/catalog.py` returns all product IDs with matching titles, and its documented behavior does not specify a limit of ten. The assignment instructions also do not establish this limit. Our actual catalog bug involved case-sensitive searching, not the number of results returned. This test therefore checks an unsupported requirement rather than the defect we fixed.

**5. Verdict**
- [ ] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [x] Invented requirement — FAIL then FAIL

---

## Part 3 — Coverage against your own bug hunt

One row per bug you recorded in `FINDINGS.md`, plus a row for any bug the

supplied set caught that you had not found yourself.
| Bug (your description) | We found it | The supplied set catches it | Which test, and how you established that |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

This is a factual cross-reference, not an opinion. Every "yes" in the third

column must point at a test you classified as a genuine detection in Part 2.

---

## Part 4 — Verdict (4 marks, 400 words maximum)

Four questions. Be specific and cite your own table.

1. **Which failure mode was most common** in the supplied set? Give the count

   from your summary table.

2. **Why is a test that passes against buggy code more dangerous than one that

   crashes?** A crashing test gets attention. Say what happens to the other

   kind.

3. **Did the supplied set catch anything you had missed?** If yes, what, and

   what would have led you to it. If no, say so — that is a legitimate answer

   and does not cost marks.

4. **What will you check before trusting a generated test in future?** Name

   checks you actually performed in this exercise, not general principles.

Answers that could have been written about any project score half marks at

best.

---

## Appendix (optional)

Prompts, or notes on AI use, that support Part 1.