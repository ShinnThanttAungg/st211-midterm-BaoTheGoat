# AI_USAGE.md — AI Usage and Critique

**Group:** BaoTheGoat

**Members:**
- Shin Thant Aung — 6705140076
- Sai Lin Thant Maung — 6705140073
- Aung Thet Khine — 6705142032
- Zwe Naing Sett — 6705140077
- Hein Naing Soe — 6705140071

---

## Part 3a: AI Declaration

Our group used ChatGPT (GPT) and Claude as supporting tools during the bookstore testing project. We used them to understand the application, investigate possible bugs, review test failures, and organize our findings.

| AI Tool | What We Used It For | How We Used the Output |
|---|---|---|
| ChatGPT (GPT) | Helped us understand the project requirements, investigate errors in user authentication, catalog search, cart total, checkout, and product importing. | We reviewed the suggestions, compared them with our source code, and modified our implementation based on actual test results. |
| Claude | Helped us discuss possible causes of test failures, understand debugging steps, and organize the bug findings. | We used its explanations as guidance and checked the proposed solutions against our application and pytest results. |

We did not treat AI responses as automatically correct. Our group checked the suggestions using the application code and test results before deciding whether to use them.

---

## Part 3b: Review of AI-Generated Tests

Our group reviewed the eight AI-generated tests in:

`ai_review/test_ai_generated.py`

The purpose of this review was to understand whether the AI-generated tests checked real application behaviour or introduced assumptions that were not supported by the project requirements.

### 1. AI-Generated Test List

| No. | Test Name | What It Checks |
|---|---|---|
| 1 | `test_cart_total_sums_items` | Checks whether the cart total includes all product prices. |
| 2 | `test_login_rejects_wrong_password` | Checks whether login rejects an incorrect password. |
| 3 | `test_search_finds_exact_title` | Checks whether catalog search can find an exact product title. |
| 4 | `test_import_returns_count` | Checks whether importing products returns the correct count. |
| 5 | `test_register_duplicate_returns_false` | Checks whether duplicate user registration is rejected. |
| 6 | `test_checkout_empty_returns_none` | Checks whether empty checkout returns `None`. |
| 7 | `test_add_to_cart_returns_true_for_known_product` | Checks whether adding a known product returns `True`. |
| 8 | `test_search_is_limited_to_ten_results` | Assumes catalog search should return no more than ten results. |

### 2. Execution Evidence

We ran the AI-generated test file using:

```powershell
python -m pytest ai_review/test_ai_generated.py -v
```

The recorded result was:

```text
collected 8 items

test_cart_total_sums_items PASSED
test_login_rejects_wrong_password PASSED
test_search_finds_exact_title PASSED
test_import_returns_count PASSED
test_register_duplicate_returns_false PASSED
test_checkout_empty_returns_none PASSED
test_add_to_cart_returns_true_for_known_product PASSED
test_search_is_limited_to_ten_results FAILED

7 passed, 1 failed in 0.52s
```

### 3. Review and Critique

**Tests 1–7: Passed**

The first seven AI-generated tests passed against the application version used in this execution. These results show that the tested behaviours worked in that version. However, passing tests alone do not prove that the tests can detect every related bug.

**Test 8: `test_search_is_limited_to_ten_results` — Failed**

This test created 20 products with the title `"match"` and expected the search result to contain no more than ten products.

The assertion was:

```python
assert len(cat.search("match")) <= 10
```

The actual result was 20 matching products.

Pytest reported:

```text
E AssertionError: assert 20 <= 10
1 failed, 7 passed in 0.52s
```

Our review found that the test assumes a ten-result limit. The available project information does not establish that this limit is a requirement of `Catalog.search()`.

Therefore, this failure does not automatically mean that the application has a bug. The expected behaviour must be checked against the original project specification.

We kept the AI-generated test unchanged for auditing and did not treat its assumption as a confirmed application defect.

### 4. AI Test Review Summary

| Review Item | Result |
|---|---|
| Total AI-generated tests | 8 |
| Passed in the recorded run | 7 |
| Failed in the recorded run | 1 |
| Main issue identified | Unsupported ten-result search assumption |
| Confirmed additional application bug | Not established by this failure |

**Note:** This execution result is from the project version shown in the supplied terminal output. It should not be confused with the earlier regression or slow-test runs, which were performed at different stages of development.

---

## Part 3c: Reflection on AI Usage

### 1. What was the most common failure mode in the AI-generated tests?

One important issue was that an AI-generated test could make an assumption that was not included in the project requirements. For example, the search-limit test expected a maximum of ten results even though the available project information did not establish that restriction.

### 2. Why can a test that passes against buggy code be more dangerous than one that crashes?

A test that passes against buggy code can give the team false confidence. The team may believe that a feature works correctly even though the test does not check the actual problem. A failing test clearly shows that something needs investigation, but a weak passing test can hide a defect.

### 3. What did our group learn from reviewing AI-generated tests?

We learned that AI-generated tests are useful starting points, but they are not always correct. We need to understand the expected behaviour, check the source code, and compare test results before accepting an AI suggestion.

The ten-result search test also taught us that a failing test does not always mean the application is wrong. Sometimes the test itself contains an unsupported requirement.

### 4. What will we do differently when using AI in future projects?

In future projects, we will use AI to support our understanding and debugging process, but we will not depend on it completely. We will check the original requirements, review the generated code, run tests, and verify the actual results before accepting suggested changes.

---

## Conclusion

ChatGPT and Claude helped our group understand possible bugs, investigate test failures, and organize our findings during the bookstore project.

However, our group learned that AI suggestions must be checked carefully. The AI-generated search-limit test demonstrated why we should not automatically accept every test expectation. We need to compare AI suggestions with the project requirements and actual application behaviour.

Overall, AI was used as a supporting tool, while our group remained responsible for reviewing the code, checking test evidence, and deciding which changes were appropriate.
