# AI_USAGE.md -- Declaration and Audit

**Group:** BaoTheGoat

**Members:**
- Aung Thet Khine — 6705142032
- Sai Lin Thant Maung — 6705140073
- Shin Thant Aung — 6705140076

## D3.1 Declaration (required)

| AI tool | How we used it |
|---|---|
| ChatGPT | Helped us understand the bookstore project requirements, Python functions, pytest markers, and Git commands. |
| ChatGPT | Suggested test cases for smoke testing and regression testing and helped us understand the bugs in login, product search, cart totals, checkout, and product importing. |
| ChatGPT | |
| ClaudeAI | Helped us suggesting detailed slow pytest. |
| ClaudeAI | |

We used AI as a learning and development assistant. We reviewed its suggestions and compared them with our code, assignment requirements, and test results. We understand that AI-generated tests can contain incorrect assumptions and must be checked before being trusted.

## D3.2 Audit of the supplied `ai_review/` test set

We compared the supplied AI-generated tests against the recorded results for the original shipped application and our modified application.

A test that passes does not automatically prove that the application is correct. We need to check whether its assertion can detect the intended defect and whether its expected behavior matches the assignment requirements.

| Test | What it claims to catch | Does it actually? | Evidence / recorded result | Verdict |
|---|---|---|---|---|
| `test_cart_total_sums_items` | Incorrect cart total | Yes, based on the recorded results | Shipped: FAIL; modified: PASS. Add the actual pytest output before submission. | Genuine detection, pending evidence check |
| `test_login_rejects_wrong_password` | Incorrect password accepted | It does not detect the special-character password bug | Shipped: PASS; modified: PASS | Passes anyway |
| `test_search_finds_exact_title` | Product title search failure | It does not detect the case-sensitivity bug | Shipped: PASS; modified: PASS | Passes anyway |
| `test_import_returns_count` | Incorrect imported product count | Yes, based on the recorded results | Shipped: FAIL; modified: PASS. Add the actual pytest output before submission. | Genuine detection, pending evidence check |
| `test_register_duplicate_returns_false` | Duplicate usernames accepted | Recorded results show PASS on both versions | Shipped: PASS; modified: PASS | Passes anyway |
| `test_checkout_empty_returns_none` | Empty checkout creates an incorrect result | Yes, based on the recorded results | Shipped: FAIL; modified: PASS. Add the actual pytest output before submission. | Genuine detection, pending evidence check |
| `test_add_to_cart_returns_true_for_known_product` | Adding a valid product fails | Recorded results show PASS on both versions | Shipped: PASS; modified: PASS | Passes anyway |
| `test_search_is_limited_to_ten_results` | Search returns more than ten products | The requirement is not established by the supplied evidence | Shipped: FAIL; modified: FAIL; the recorded assertion was `assert 20 <= 10` | Possible invented requirement; verify against the specification |

**Important evidence note:** These results are based on the audit information already recorded in our project draft. We must verify them against the actual test file and full pytest output before treating them as final evidence.

### Audit interpretation

- **FAIL → PASS:** The test may have detected a genuine defect, provided its expected behavior is supported by the requirements.
- **PASS → PASS:** The test did not distinguish the original application from the modified application. It may still be a useful basic test, but it did not detect the targeted defect.
- **PASS → FAIL:** The test may depend on incorrect behavior in the original application.
- **FAIL → FAIL:** The test may have an incorrect expectation, an unresolved defect, or another failure. The requirement and error output must be checked before deciding.

## D3.3 Verdict

The supplied AI-generated tests did not detect every defect found during our investigation. For example, the login test checked a normal incorrect password but did not test how special characters were handled. Similarly, the exact-title search test did not check whether lowercase and uppercase search terms behaved consistently.

A test that passes against buggy code can be dangerous because it may give the team false confidence that a feature works correctly. The test may simply fail to exercise the defective behavior.

In the future, we will check AI-generated tests against the project requirements and inspect the assertions carefully. We will run tests against the original application and the modified application, examine the actual output, and verify that each test detects the intended problem. We will also avoid treating an AI-suggested requirement as correct until we find evidence in the assignment instructions or documented application behavior.


