Write-up by wook413

# Lab: Password reset broken logic

This lab's password reset functionality is vulnerable. To solve the lab, reset Carlos' password then log in and access his "My account" page.

- Your credentials `wiener:peter`
- Victim's username: `carlos`

---

Since the lab indicated that the password reset functionality was vulnerable, I went straight to the login page and saw a "**Forgot password?**" button in the login form.

![image-20260711004458613](./lab3.assets/image-20260711004458613.png)

Clicking it prompted me to enter a username or email, so I typed in `wiener`.

![image-20260711004559884](./lab3.assets/image-20260711004559884.png)

It then told me to check my email inbox for a reset password link.

![image-20260711004709702](./lab3.assets/image-20260711004709702.png)

In the email client, I found an email containing the reset password link.

![image-20260711004733365](./lab3.assets/image-20260711004733365.png)

Clicking the link prompted me to enter a new password.

![image-20260711004852831](./lab3.assets/image-20260711004852831.png)

I confirmed I could log in with the new password.

![image-20260711005710387](./lab3.assets/image-20260711005710387.png)

After completing the password reset process, I went back to Burp Suite and reviewed the request and response for each step. I noticed the POST request for resetting the password included a `temp-forgot-password-token` parameter, along with the username and new password.

![image-20260711005145599](./lab3.assets/image-20260711005145599.png)

I tried removing the value of the `temp-forgot-password-token` parameter from both the URL and the request body, and the request still returned a 302 status code, indicating a successful password reset, which I confirmed.

![image-20260711010315238](./lab3.assets/image-20260711010315238.png)

Since the request succeeded even without the token value, I changed the username from `wiener` to `carlos` and sent the exact same request.

![image-20260711010340404](./lab3.assets/image-20260711010340404.png)

I tried logging in as `carlos` with the new password, and I was able to authenticate as `carlos`!

### Solved!

![image-20260711010403858](./lab3.assets/image-20260711010403858.png)



