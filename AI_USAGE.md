# AI Usage Declaration and Audit

**Group:** Bao The Goat  
**Assessment:** ST211 Midterm — Part D3 (20 marks)

## Group Members

| Member | GitHub Username | 
|---|---|---|
| Zwe Naing Set | DivineKeraunos | 
| Aung Thet Khine | AungThetKhine21 |
| Sai Lin That Maung | Sailinthant | 
| Shin Thant Aung | ShinnThanttAungg | 
| Hein Naing Soe | ScottG619 | 

## Part 1 — AI Usage Declaration

Our group used three AI tools during the project: ChatGPT, Claude, and Gemini. We used their suggestions as supporting resources rather than accepting generated answers without review. We checked relevant suggestions against our application, assignment requirements, and test results.

| AI Tool | Purpose | Project Areas | Verification |
|---|---|---|---|
| ChatGPT | Assisted our debugging of login and product search, development of regression tests, interpretation of Python errors, and use of Git commands. | `bookstore_app/users.py`, `bookstore_app/catalog.py`, `tests/test_bookstore.py`, `FINDINGS.md` | We reviewed suggestions, adjusted the code where necessary, and ran pytest before committing changes. |
| Claude | Supported code review, identification of possible implementation errors, and improvements to our testing approach. | Application code and test development | We compared suggestions with our implementation and checked relevant changes through testing. |
| Gemini | Helped us understand testing concepts, interpret assignment requirements, and improve technical documentation. | Test planning and project documentation | We compared explanations with the assignment instructions and reviewed written material for accuracy. |

## Part 2 — Audit of the Supplied AI-Generated Test Set

### 2.1 Audit Approach

We reviewed the eight tests in `ai_review/test_ai_generated.py` and compared their results against the original (shipped) application and our group's modified version. We classified each test using the outcomes of these two runs. A test that fails is not automatically a valid defect detector: its assertion must also reflect the intended application behavior.

| Shipped Version | Modified Version | Classification | Interpretation |
|---|---|---|---|
| FAIL | PASS | Genuine detection | The test identified a defect that was subsequently fixed. |
| PASS | PASS | Detects nothing | The test passed in both versions and did not reveal the relevant defect. |
| PASS | FAIL | Locks in the bug | The test depended on the original incorrect behavior. |
| FAIL | FAIL | Invented requirement | The test remained unsuccessful; an unsupported expectation must be checked against the requirements. |

### 2.2 Summary of Test Results

The following results are taken from our recorded shipped-version and modified-version runs. Detailed audit entries have been completed for the three tests assigned to Aung Thet Khine; the remaining entries require confirmation and supporting evidence from the responsible group members.

| No. | Test | Intended Check | Shipped | Modified | Recorded Verdict | Auditor |
|---|---|---|---|---|---|---|
| 1 | `test_cart_total_sums_items` | Correct cart total | FAIL | PASS | Genuine detection | To be completed |
| 2 | `test_login_rejects_wrong_password` | Incorrect password is rejected | PASS | PASS | Detects nothing | Aung Thet Khine |
| 3 | `test_search_finds_exact_title` | Exact title can be found | PASS | PASS | Detects nothing | Aung Thet Khine |
| 4 | `test_import_returns_count` | Correct number of imported products | FAIL | PASS | Genuine detection | To be completed |
| 5 | `test_register_duplicate_returns_false` | Duplicate registration is rejected | PASS | PASS | Detects nothing | To be completed |
| 6 | `test_checkout_empty_returns_none` | Empty-cart checkout returns `None` | FAIL | PASS | Genuine detection | To be completed |
| 7 | `test_add_to_cart_returns_true_for_known_product` | Existing product can be added to cart | PASS | PASS | Detects nothing | To be completed |
| 8 | `test_search_is_limited_to_ten_results` | Search returns at most ten matches | FAIL | FAIL | Invented requirement* | Aung Thet Khine |

*The classification for test 8 is based on the documented `search()` behavior and the available test output. The group should reconfirm it against the final assignment requirements before submission.*

### 2.3 Detailed Audit Entries

#### Test 2 — `test_login_rejects_wrong_password`

**Audited by:** Aung Thet Khine  
**Test file:** `ai_review/test_ai_generated.py`

**Purpose.** This test checks whether the application rejects an incorrect password during login. However, it does not examine the special-character password handling issue identified in `bookstore_app/users.py`.

**Evidence — shipped version**

```text
ai_review/test_ai_generated.py::test_login_rejects_wrong_password PASSED
```

**Evidence — modified version**

```text
ai_review/test_ai_generated.py::test_login_rejects_wrong_password PASSED [ 25%]
```

**Analysis.** The test passed on both versions. Its assertion did not detect the original password-handling defect because it only checked a straightforward incorrect-password case. An effective regression test would compare passwords exactly, including special characters.

**Verdict:** Detects nothing (PASS → PASS).

#### Test 3 — `test_search_finds_exact_title`

**Audited by:** Aung Thet Khine  
**Test file:** `ai_review/test_ai_generated.py`

**Purpose.** This test checks whether a product can be found when the search keyword exactly matches its title.

**Evidence — shipped version**

```text
ai_review/test_ai_generated.py::test_search_finds_exact_title PASSED
```

**Evidence — modified version**

```text
ai_review/test_ai_generated.py::test_search_finds_exact_title PASSED [ 37%]
```

**Analysis.** The test passed before and after our changes, so it did not detect the case-sensitivity defect in `bookstore_app/catalog.py`. It only tested an exact match. A stronger test would use different uppercase and lowercase combinations and confirm that the correct product is still returned.

**Verdict:** Detects nothing (PASS → PASS).

#### Test 8 — `test_search_is_limited_to_ten_results`

**Audited by:** Aung Thet Khine  
**Test file:** `ai_review/test_ai_generated.py` (test starts near line 52; failing assertion at line 60)

**Purpose.** This test checks whether catalog search returns no more than ten matching products.

**Evidence — shipped version**

```text
FAILED ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results - AssertionError: assert 20 <= 10
```

**Evidence — modified version**

```text
FAILED ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results
AssertionError: assert 20 <= 10
```

**Analysis.** Both versions returned twenty matches when the test added twenty matching products. The `search()` implementation returns matching product IDs and does not impose a ten-result limit. This assertion does not test our actual search defect, which involved case sensitivity. Based on the documented behavior available to us, the ten-result restriction appears unsupported; this should be checked once more against the final project specification.

**Verdict:** Invented requirement (FAIL → FAIL), subject to final requirements verification.

### 2.4 Remaining Audit Contributions

The group will add the individual detailed audit entries for tests 1, 4, 5, 6, and 7. Each entry must identify the auditor, explain the assertion, include the actual pytest output from both versions, and justify its verdict. We have not attributed these entries to members who have not yet completed them.

**Evidence note:** The output excerpts above reproduce the lines already recorded in our draft. Before final submission, we should paste the complete, unedited pytest output for each test from both versions, as required by the assessment.

## Part 3 — Coverage Against Our Bug Findings

We will compare the defects recorded in `FINDINGS.md` with the AI-generated test set. The table below includes the two defects already investigated in our login and catalog work. Other findings and newly detected defects will be added after the remaining group members complete their audit.

| Defect Recorded in `FINDINGS.md` | Found by Our Group | Detected by the Supplied Test Set | Supporting Test and Reason |
|---|---|---|---|
| Login password comparison mishandled special characters | Yes | No | `test_login_rejects_wrong_password` passed on both versions and did not exercise special-character handling. |
| Product search was case-sensitive | Yes | No | `test_search_finds_exact_title` passed on both versions and did not test mixed-case queries. |
| Additional group findings and defects detected by supplied tests | Pending group review | Pending group review | To be completed using `FINDINGS.md` and verified test output. |

## Part 4 — Group Evaluation

*Pending completion by the group after all eight detailed audits and the coverage comparison are verified.*

Our final evaluation will address the most common test failure mode, why a test that passes against defective code can create false confidence, whether the supplied tests found defects we missed, and the specific checks we performed before trusting AI-generated tests. We will base our conclusions on the completed summary table, the two evidence runs for each test, and `FINDINGS.md`, keeping this section under 400 words.

## Submission Status

Our AI usage declaration and three individual test audits are drafted. Before final submission, we still need to incorporate the remaining members' audit entries, paste full original and modified test outputs for all eight tests, confirm the final coverage table, and complete the group evaluation. We will review the combined document for consistency before committing the final version.
