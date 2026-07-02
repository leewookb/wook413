Writeup by wook413

# Lab: SQL injection attack, listing the database contents on non-Oracle databases

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the `administrator` user.

---

Here's what the landing page looks like:

![image-20260701201914511](./lab5.assets/image-20260701201914511.png)

I clicked on the **Pets** category and started guessing the number of columns with the following query: `Pets' UNION SELECT 'wook', '413'-- `.

![image-20260701202044123](./lab5.assets/image-20260701202044123.png)

Normally, you'd have to guess both the number and type of columns through trial and error, but this time the payload happened to match on the first try. The response came back with a 200 status code instead of a database error.

![image-20260701202109924](./lab5.assets/image-20260701202109924.png)

I confirmed the application displayed my strings, **wook** and **413**.

![image-20260701202157162](./lab5.assets/image-20260701202157162.png)

Now that I had confirmed the number and type of columns, it was time to return all of the tables in the database and find which one might contain user information.

![image-20260701202620897](./lab5.assets/image-20260701202620897.png)

The query in the screenshot above successfully returned all of the tables in the databse.

![image-20260701202657340](./lab5.assets/image-20260701202657340.png)

At the bottom of the results, one table name stood out: `users_ytatxu`.

![image-20260701202737084](./lab5.assets/image-20260701202737084.png)

I modified the query to return the column names within the `users_ytatxu` table.

![image-20260701203002664](./lab5.assets/image-20260701203002664.png)

The application displayed three columns: `password_opcuny`, `username_zsklhk`, and `email`.

![image-20260701203215583](./lab5.assets/image-20260701203215583.png)

I modified the query once more to pull all usernames and passwords from `users_ytatxu`. I could have included the `email` column too, but since the query only supports two columns, and username/password were enough to login, I left it out.

![image-20260701203548050](./lab5.assets/image-20260701203548050.png)

The response returned the administrator's credentials along with those of other users.

![image-20260701203621804](./lab5.assets/image-20260701203621804.png)

I used the administrator's credentials to login.

![image-20260701203657221](./lab5.assets/image-20260701203657221.png)

### Solved!

![image-20260701203711531](./lab5.assets/image-20260701203711531.png)

