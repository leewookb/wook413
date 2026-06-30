Writeup by wook413

# Lab: SQL injection vulnerability allowing login bypass

This lab contains a SQL injection vulnerability in the login function. To solve the lab, perform a SQL injection attack that logs in to the application as the `administrator` user.

---

This is what you see when you first arrive at the main page.

![image-20260629224554916](./lab2.assets/image-20260629224554916.png)

Clicking on **My account** button takes you to the login page.

![image-20260629224732991](./lab2.assets/image-20260629224732991.png)

Enter `administrator' or 1=1-- ` in the **Username** field and any random characters in the **Password** field. This payload bypasses the password check because the SQL query always evaluates to true.

![image-20260629224919988](./lab2.assets/image-20260629224919988.png)

**Solved!**

![image-20260629224850919](./lab2.assets/image-20260629224850919.png)