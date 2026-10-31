# Automated Software Testing

## Midterm Project Report

**Course:** Automated Software Testing (192-211)  
**Instructor:** Arj. Doung Vu Xuan Quynh  
**Group Name:** BaoTheGoat

### Members

- Shin Thant Aung — 6705140076
- Sai Thant Lin Maung — 6705140073
- Aung Thet Khine — 6705142032
- Zwe Naing Sett — 6705140077
- Hein Naing Soe — 6705140071

---

## Table of Contents

- [Part A — Test Types](#part-a--test-types)
- [Part B — Scenario Classification](#part-b--scenario-classification)
- [Part C — Test Execution Results](#part-c--test-execution-results)
- [Part D — AI-Generated Test Review](#part-d--ai-generated-test-review)
- [Part F — Team Reflection](#part-f--team-reflection)
- [Conclusion](#conclusion)

---

## Part A — Test Types

### 1. Smoke Testing

Smoke testing is a basic test that checks whether the main functions of an application work correctly. It helps us find major problems before running more detailed tests.

In our online bookstore project, smoke tests check important features such as:

- Registering a new user and rejecting duplicate usernames.
- Logging in with correct and incorrect credentials.
- Adding products to the shopping cart.
- Adding products to the catalog and searching for them.
- Checking out a cart and saving the order.
- Checking that order history can store multiple orders.

Smoke tests should run whenever developers push new code to the repository. They help the team quickly check whether the main application functions are still working.

### 2. Regression Testing

Regression testing checks whether previously working features still work after code changes or bug fixes.

In our bookstore application, regression tests are important because changing one function may affect another function.

Examples include:

- Checking that passwords containing special characters are handled correctly.
- Checking that catalog search works with uppercase and lowercase letters.
- Checking that the cart calculates the total price of every product.
- Checking that checking out an empty cart does not create an incorrect order.
- Checking that importing products returns the correct number.

Regression tests should run after bug fixes and whenever related code is changed.

### 3. Slow Testing

Slow testing checks application performance and behavior when handling large amounts of data or repeated operations. These tests usually take longer than normal tests.

In our bookstore project, examples include:

- Importing 20,000 products.
- Performing 3,000 searches in a catalog containing 10,000 products.
- Checking search results as the catalog grows.
- Importing and checking out 5,000 products.
- Registering and logging in 400,000 users.
- Performing 200,000 checkout operations.
- Performing 1,000,000 random cart operations.
- Checking mixed-case search results in a large catalog.

Slow tests help us understand whether the application can handle larger workloads without unexpected problems.

They should normally run separately from quick smoke tests, such as during a scheduled nightly test.

---

## Part B — Scenario Classification

The following scenarios show how we classify different tests in our online bookstore application.

| No. | Test Scenario | Test Type | Reason |
|---|---|---|---|
| 1 | Check that a user can register and log in successfully. | Smoke | Registration and login are important basic functions. |
| 2 | Check that login handles passwords containing special characters correctly. | Regression | It checks a previously identified password-handling problem. |
| 3 | Check that catalog search works with different uppercase and lowercase letters. | Regression | It checks the previous search problem. |
| 4 | Check that the cart calculates the total price of all products. | Regression | It prevents the previous bug where the last item was skipped. |
| 5 | Check that an empty cart does not create an incorrect order. | Regression | It checks the expected behavior of empty checkout. |
| 6 | Check that importing products returns the correct number. | Regression | It checks the previous incorrect import count. |
| 7 | Import and search through thousands of products repeatedly. | Slow | It checks application behavior under a large workload. |
| 8 | Perform a large number of user, cart, and checkout operations. | Slow | It checks whether the application can handle repeated operations. |

Some scenarios may belong to more than one test type. For example, a test can be both regression and slow if it checks an existing bug under a large workload.

---

## Part C — Test Execution Results

We used Pytest to execute our smoke, regression, and slow tests separately. We also ran the complete test suite to check the overall project.

### 1. Smoke Test Results

Command:

`python -m pytest -m smoke -v`

Result:

**6 passed, 23 deselected in 0.09s**

All six smoke tests passed. The results show that the main bookstore functions, including user registration, login, product searching, cart operations, checkout, and order history, worked correctly during this test run.

### 2. Regression Test Results

Command:

`python -m pytest -m regression -v`

Result:

**5 passed, 24 deselected in 0.07s**

All five collected regression tests passed. The tests checked the five previously investigated application problems.

### 3. Slow Test Results

Command:

`python -m pytest -m slow -v`

Result:

**8 passed, 21 deselected in 74.43s**

All eight slow tests passed. They checked large product imports, repeated catalog searches, user registration and login, checkout history, and random cart operations.

### 4. Full Test Suite Results

Command:

`python -m pytest -v`

Result:

**28 passed, 1 failed in 78.21s**

The full test suite included the team's tests, the AI review tests, and the worked-example tests.

The only failure was:

`ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results`

This test expected the catalog search to return no more than ten results. However, the application returned twenty matching products.

This failure belongs to the AI-generated test review. It does not mean that one of our five confirmed application bug fixes failed.

---

## Part D — AI-Generated Test Review

### 1. AI Tools Used

We used ChatGPT and Claude during the project.

We used these tools to help us understand the requirements, investigate possible bugs, suggest test cases, and review our findings.

However, we did not accept every AI suggestion automatically. We checked the suggestions against our application code and actual test results.

The detailed AI declaration and review are provided in the separate `AI_USAGE.md` file.

### 2. AI-Generated Test Execution

We executed the eight AI-generated tests separately.

Command:

`python -m pytest ai_review/test_ai_generated.py -v`

Result:

**7 passed, 1 failed in 0.13s**

Seven AI-generated tests passed. One test failed:

`test_search_is_limited_to_ten_results`

The test created twenty matching products and expected the search function to return ten or fewer results. The actual result contained twenty products.

### 3. Review of the Failed AI Test

We reviewed the failed test and found that its expectation was not clearly supported by the project requirements provided to us.

The test assumed that catalog search must limit results to ten products. However, our project requirements did not specify this limitation.

Therefore, we did not classify this failure as a confirmed application bug. It demonstrates that AI-generated tests can include assumptions that are not part of the actual requirements.

### 4. What We Learned from AI Testing

AI tools can help developers create test ideas and find possible problems more quickly. However, AI-generated tests still need to be reviewed.

A test can fail because the application has a real bug, but it can also fail because the test expects behavior that was never required.

We learned that we should always compare AI-generated tests with the project requirements, source code, and actual application behavior before accepting them.

---

## Part F — Team Reflection

### 1. What was the most difficult part of this project?

The most difficult part was finding bugs and understanding why the application did not behave as expected. Some problems were not easy to notice because the application could still run without showing an error.

We needed to read the source code, create test cases, and compare the actual results with the expected results.

### 2. How did testing help us improve the application?

Testing helped us identify problems in different parts of the bookstore application. For example, we found issues with password handling, catalog searching, cart total calculation, empty checkout, and product importing.

After identifying these problems, we worked on fixes and used regression tests to check whether the problems were solved.

### 3. What did we learn about teamwork?

We learned that dividing tasks among team members can make the work easier and faster. Each member could focus on different parts of the project, such as writing tests, investigating bugs, fixing code, and reviewing results.

We also learned that communication is important because changes made by one member can affect another member's work.

### 4. What did we learn about using AI tools?

We used ChatGPT and Claude to help us understand the project requirements, investigate possible bugs, and review test ideas.

However, AI-generated tests were not automatically accepted. We checked their assumptions against the project code and actual test results. Some AI suggestions were useful, while others expected behavior that was not clearly required by the project.

### 5. What would we improve next time?

Next time, we would start testing earlier and organize our test cases more carefully. We would also update Git more regularly so that every team member can work with the latest version.

We would run the full test suite after important code changes and keep clear records of test results.

---

## Conclusion

Through this project, we gained practical experience in automated software testing using Python and Pytest. We learned how to create smoke, regression, and slow tests, identify bugs, and check whether code changes fix the problems.

Our separate test runs showed that all six smoke tests, five regression tests, and eight slow tests passed. The full test suite reported 28 passed and one failed. The failed test came from the AI review and used a search-result limit that was not clearly specified in the project requirements.

We also learned that a test passing does not always mean that the application is completely correct. Test cases must have clear expected results and should be based on the actual project requirements.
