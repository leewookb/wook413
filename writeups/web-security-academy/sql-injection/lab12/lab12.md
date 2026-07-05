Write-up by wook413

# Blind SQL injection with conditional errors

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

---

I clicked **My account** button on the main page.

![image-20260704221733780](./lab12.assets/image-20260704221733780.png)

I intercepted the request and sent it to **Burp Repeater**. As in the previous lab, we're assigned a cookie.

![image-20260704224012864](./lab12.assets/image-20260704224012864.png)

Unlike the previous lab, though, changing the cookie value to a random string doesn't produce an error. The server just returned a **200 OK**.

![image-20260704224104562](./lab12.assets/image-20260704224104562.png)

However, when I appended a single quote `'`, it returned a **500 Internal Server Error**.

![image-20260704224140758](./lab12.assets/image-20260704224140758.png)

![image-20260704224207711](./lab12.assets/image-20260704224207711.png)

As the lab title suggests, we need to exploit this using conditional errors. Referring to the provided SQL injection cheat sheet, I came up with the following payload: `6Ef8LW426dGFRB1P' AND (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE 'wook' END FROM dual) = 'wook'-- `

![image-20260704224730439](./lab12.assets/image-20260704224730439.png)

The logic here is: if the condition evaluates to true, the server tries to evaluate `TO_CHAR(1/0)`, which throws a **division-by-zero error**. If the condition is false, it returns a `'wook'` instead, which is then compared against the `'wook'` string outside the subquery. If they match, the overall expression is true; otherwise, false. 

I started with `1=2`, which is always false, so the subquery returns `'wook'`, which matches the outer `'wook'`, and the whole thing evaluates to true. It didn't error, as expected.

![image-20260704224714589](./lab12.assets/image-20260704224714589.png)

When I changed the condition to `1=1`, the server returned **a 500 error**, confirming the injection point works as intended.

![image-20260704224815091](./lab12.assets/image-20260704224815091.png)

Now that I'd validated the technique, I used it to find the length of the administrator's password:

```
`6Ef8LW426dGFRB1P' AND (SELECT CASE WHEN (LENGTH(password) > 1) THEN TO_CHAR(1/0) ELSE 'wook' END FROM users WHERE username = 'administrator') = 'wook' -- `
```

 This returned a 500 error, confirming the password length is greater than 1.

![image-20260704225354030](./lab12.assets/image-20260704225354030.png)

As a sanity check, I changed the `1` to `100`, and the server returned a 200 OK, confirming the password is shorter than 100 characters.

![image-20260704225427225](./lab12.assets/image-20260704225427225.png)

 I sent the request to Intruder and set `100` as the payload position, sweeping values from 1 to 30.

![image-20260704225547257](./lab12.assets/image-20260704225547257.png)

The attack finished within seconds. Looking at the results, the response length stayed at 2555 with a 500 status code up through payload **19** but at **20** the status flipped to 200 and the response length jumped to 3361. This confirmed the password length is 20 characters.

![image-20260704225656418](./lab12.assets/image-20260704225656418.png)

With the length known, I moved on to extracting the password character by character:

```
6Ef8LW426dGFRB1P' AND (SELECT CASE WHEN (SUBSTR(password, 1, 1) = 'a') THEN TO_CHAR(1/0) ELSE 'wook' END FROM users WHERE username = 'administrator') = 'wook' -- 
```

This returned a 200 OK, meaning the first character isn't `'a'`.

![image-20260704230033702](./lab12.assets/image-20260704230033702.png)

I sent the request to Intruder again, this time with two payload positions: one sweeping the character position from 1 to 20, and the other sweeping candidate characters from a-z and 0-9.

Since there are two independent payload sets, I used **Cluster Bomb mode** instead of **Sniper mode**.

![image-20260704230214294](./lab12.assets/image-20260704230214294.png)

![image-20260704230233562](./lab12.assets/image-20260704230233562.png)

![image-20260704230300305](./lab12.assets/image-20260704230300305.png)

This attack also completed in just a few seconds after I ran it. Sorting the results by response length and then status code, I found exactly 20 results with a response length of **2555** and status code **500** -- matching the password length exactly, which confirmed these were the correct characters. The extracted password was `5vjmmnpr8281md1bvksp`.

![image-20260704230428844](./lab12.assets/image-20260704230428844.png)

I logged in as the administrator using the password.

![image-20260704230514130](./lab12.assets/image-20260704230514130.png)

### Solved!

![image-20260704230530339](./lab12.assets/image-20260704230530339.png)

