Writeup by wook413

# Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

---

**Lab#4** is almost the same as the previous lab, **Lab#3**. This lab requires us to display the database version string via a SQL injection attack, but this time the database is MySQL.

![image-20260630215912837](./lab4.assets/image-20260630215912837.png)

Looking at the provided SQL injection cheat sheet, I learned that I can use `SELECT @@version` to query the version on Microsoft SQL Server and MySQL. Also, unlike Oracle, we do not need to specify a table to select from when using a `SELECT` statement.

![image-20260630220542908](./lab4.assets/image-20260630220542908.png)

I clicked on **Pets** category and my initial query to test was the following: `Pets' UNION SELECT 'wook', '413'-- `

![image-20260630220148950](./lab4.assets/image-20260630220148950.png)

It successfully displayed **wook** and **413** on the web application, confirming that my initial query worked.

![image-20260630220206543](./lab4.assets/image-20260630220206543.png)

I then changed my query to `Pets' UNION SELECT @@version, '413'-- ` to display the version of the database.

![image-20260630220334882](./lab4.assets/image-20260630220334882.png)

This time it displayed the database version string on the web application!

![image-20260630220354596](./lab4.assets/image-20260630220354596.png)

**Solved!**

![image-20260630220408746](./lab4.assets/image-20260630220408746.png)