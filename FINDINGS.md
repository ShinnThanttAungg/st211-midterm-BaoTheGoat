# Bug-Hunt Findings Log

Fill in one entry per bug you find, AS YOU FIND IT (before doing the AI
comparison). Write in your own words, like a detective's notebook. Show the real
path -- including things you tried that did not work.

Group: <BaoTheGoat>
Members: <Aung Thet Khine - 6705142032>
         
---

## Bug 1: Login Accepts Incorrect Password



- **Module / function:** <users.py → login()>
- **What we suspected and why:** < We noticed that the login function removed special characters from the entered password before checking it. We suspected this could allow users to log in with an incorrect password.>
- **What we did:** < We registered a user named student1 with the password hello123. Then we tried to log in using hello@123. We also wrote a regression test using pytest to check whether the incorrect password was rejected.>
- **What we observed (the wrong result):** < The original login function returned True even though the entered password was incorrect. Our test failed with AssertionError: assert True is False.>
- **What we expected instead:** < The function should return False because hello@123 is different from hello123. A user should only be able to log in when the password matches exactly.>
- **The fix we made:** < We removed the password-cleaning code and changed the function to compare the entered password directly with the stored password. After making the change, we ran the regression test again and it passed.>
- **Author of this finding:** < Aung Thet Khine >

---

## Bug 2: Product Search Is Case-Sensitive



- **Module / function: catalog.py** < catalog.py → search()>
- **What we suspected and why** < We noticed that the search function compared the keyword directly with the product title. We suspected that searching with different uppercase or lowercase letters would not find the correct product.>
- **What we did:** < We added a product with ID 1, title Python Programming, and price 500. Then we searched for the product using the lowercase keyword python. We wrote a regression test to check the result.>
- **What we observed (the wrong result):** < The original search function returned an empty list [] instead of finding the product. Our test failed with AssertionError: assert 1 in [].>
- **What we expected instead:** < The search function should return [1] because the keyword python matches the title Python Programming, regardless of uppercase or lowercase letters.>
- **The fix we made:** < We used .lower() on both the keyword and product title before comparing them. After fixing the function, we ran the regression test again and it passed.>
- **Author of this finding:** < Aung Thet Khine >

---

## Bug 3

(copy the block above for each additional bug you find)
