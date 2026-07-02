Writeup by wook413

# Lab: SQL injection attack, listing the database contents on Oracle

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the `administrator` user.

---

This lab is very similar to the previous one, except this time we're attacking an Oracle database.

![image-20260702000720904](./lab6.assets/image-20260702000720904.png)

Just like the previous lab, I guessed the number and type of columns using the strings **'wook'** and **'413'**. I made sure to specify the `dual` table at the end, since Oracle requires you to specify a table to query from.

![image-20260702000923425](./lab6.assets/image-20260702000923425.png)

The web application displayed the strings **'wook'** and **'413'**, confirming that the number and type of columns were correct.

![image-20260702000953127](./lab6.assets/image-20260702000953127.png)

Next, I listed all the table names using the following query, based on a hint from the provided cheat sheet.

![image-20260702001440195](./lab6.assets/image-20260702001440195.png)

One table in the returned list caught my attention: `USERS_JEMMUO`.

![image-20260702001527488](./lab6.assets/image-20260702001527488.png)

I then modified the query to list all the column names in the `USERS_JEMMUO` table.

![image-20260702001812129](./lab6.assets/image-20260702001812129.png)

There were three columns: `EMAIL`, `PASSWORD_NEMKWF`, and `USERNAME_GPIWZO`.

![image-20260702001847991](./lab6.assets/image-20260702001847991.png)

I modified the query again to retrieve all the usernames and passwords from the table.

![image-20260702001949855](./lab6.assets/image-20260702001949855.png)

I found three sets of credentials: `administrator`, `carlos`, and `wiener`.

![image-20260702002017587](./lab6.assets/image-20260702002017587.png)

I logged in as `administrator`.

![image-20260702002035234](./lab6.assets/image-20260702002035234.png)

### Solved!

![image-20260702002049324](./lab6.assets/image-20260702002049324.png)