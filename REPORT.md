# Automated Software Testing

## Midterm Project Report

**Instructor:** Arj. Doung Vu Xuan Quynh

**Group Name:** BaoTheGoat

### Members

- Shin Thant Aung — 6705140076
- Sai Lin Thant Maung — 6705140073
- Aung Thet Khine — 6705142032
- Zwe Naing Sett — 6705140077
- Hein Naing Soe — 6705140071

---

## Table of Contents

- [Part A — Test Types](#part-a--test-types)
- [Part B — Scenario Classification](#part-b--scenario-classification)
- [Part F — Team Reflection](#part-f--team-reflection)
- [Conclusion](#conclusion)

---

## Part A — Test Types

### 1. Smoke Testing

Smoke testing ensures that the primary application's functions are working. It is typically executed first after a new build, deployment, or code change to catch major issues.

**Bookstore examples:**

1. Test whether a new user can register and log in successfully.
2. Verify whether a customer can add a book to the cart and complete checkout with a non-empty cart.

### 2. Regression Testing

Regression testing checks whether features still perform as expected after changing code or fixing bugs. It should run after changes that could affect existing functionality and before major releases.

**Bookstore examples:**

1. After fixing the login bug, test that the registered password is accepted and an incorrect password is rejected.
2. After fixing the cart total bug, test whether the cart total includes all items.

### 3. Slow Testing

Slow testing checks application behaviour when a large workload is used or operations take a longer time. These tests are typically performed as part of planned CI/CD jobs, such as nightly runs, rather than after every small code change.

**Bookstore examples:**

1. Import 10 to 100,000 products and verify that the correct number is returned.
2. Perform many cart operations and check whether the application continues to function as expected.

---

## Part B — Scenario Classification

### Scenario 1: Verify that a password-reset email is delivered within one minute.

**Classification: Smoke testing**

This may be used as a smoke test because it checks whether an important function works within the required response time. It can run after deployment to identify a major problem with password reset. A more detailed email-delivery test may also be included in the regression suite.

### Scenario 2: Verify that a previously fixed bug in shipping-cost calculation has not returned.

**Classification: Regression testing**

This is regression testing because it verifies that a previously fixed bug does not return after a code change. The test should use input that caused the problem in the past and ensure that the shipping cost is calculated correctly.

### Scenario 3: Verify that a nightly job can generate a sales report from ten years of orders.

**Classification: Slow testing**

This is slow testing because processing ten years of order data can take significant time and resources. It is suitable for an automated nightly test because it processes a large amount of historical data.

### Scenario 4: Verify that the payment page loads after every deployment.

**Classification: Smoke testing**

This is a smoke test because it checks whether an important page is available after deployment. It should run early in the deployment pipeline so the team can detect a major problem before spending time on more detailed testing.

### Scenario 5: Verify that a refund issued twice does not credit the customer twice — a fault reported by a customer last quarter.

**Classification: Regression testing**

This is regression testing because it checks a previously reported defect. The test should generate the same refund request twice and ensure that the customer is credited only once. This helps prevent the same issue from occurring again.

### Scenario 6: Verify that the recommendation engine still responds when the catalogue holds one million titles.

**Classification: Slow testing**

This is slow testing because it checks system performance and behaviour with a very large catalogue. Preparing the data and running the test may require substantial time and resources. It is suitable for scheduled performance or load testing.

---

## Part F — Team Reflection

### 1. Why is running only regression tests before every commit inefficient?

The full regression suite might take a long time to run, particularly if some tests are slow. Smoke tests can validate the primary features quickly, while the full regression suite can run at an appropriate stage.

### 2. Why do smoke tests usually run first in a CI/CD pipeline?

Smoke tests usually take a short amount of time and check the most critical features. If a major feature is malfunctioning, the pipeline can stop early instead of spending time running many detailed tests.

### 3. What risks arise if slow tests are never run?

Some problems might only appear with large datasets or many operations. If slow tests are never run, the team may overlook performance problems, failures under heavy loads, or issues that do not appear during normal use.

### 4. Can one test belong to two categories? Give an example.

Yes. A single test may belong to two categories because the categories describe different characteristics. For example, a test that checks a previously fixed cart bug while processing a very large order can have both regression and slow-testing characteristics.

### 5. What does separating bug-finders and bug-fixers change about how a bug report must be written?

A bug report should be clear and detailed when different people find and fix bugs. It should describe how to reproduce the problem, the input provided, the actual output, the expected output, and any error messages. This helps the developer understand and resolve the issue without having to guess what happened.

---

## Conclusion

In this project, we learned about smoke testing, regression testing, and slow testing. We also classified different testing scenarios and discussed the importance of each testing type. This project helped us understand how testing can uncover bugs, prevent old bugs from returning, and improve software quality.
