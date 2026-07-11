Write-up by wook413

# Lab: Username enumeration via subtly different responses

This lab is subtly vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate  passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

---

Since the lab directly told me what functionality is vulnerable on this application, I went straight to the "My account" page and typed in random credentials `wook:wook`.

![image-20260711085036440](./lab4.assets/image-20260711085036440.png)

In Burp, I saw that I made a POST request to the `/login` endpoint and got a 200 OK, but the response body said "**Invalid username or password.**"

![image-20260711085135922](./lab4.assets/image-20260711085135922.png)

I sent this request to Intruder and marked the username value as the target position, then pasted the provided wordlist of usernames as the payload.

![image-20260711085228918](./lab4.assets/image-20260711085228918.png)

I ran the attack, it finished quickly, but when I sorted the results by length, no single response stood out as different from the rest.

![image-20260711085644194](./lab4.assets/image-20260711085644194.png)

I pulled up one of the responses and saw it contained "**Invalid username or password.**" in the body, just like when I typed in `wook:wook`.

![image-20260711085712255](./lab4.assets/image-20260711085712255.png)

I copy-pasted that exact sentence into the response filter and tried to filter out responses that didn't match it.  I checked "**Case sensitive**" and **"Negative search"** so it would only show me responses that differed.

![image-20260711085731405](./lab4.assets/image-20260711085731405.png)

When I clicked **Apply**, it displayed only one result.

![image-20260711085756722](./lab4.assets/image-20260711085756722.png)

I pulled it up and noticed the response for the username **arizona** returned "**Invalid username or password**" without a period at the end. I was confident this was the valid username, since there was no other reason for this one response to differ.

![image-20260711085816808](./lab4.assets/image-20260711085816808.png)

Now that I had the username, I moved on to finding the password. I marked the password value as the target position and used the provided wordlist of passwords as the payload.

![image-20260711085925614](./lab4.assets/image-20260711085925614.png)

The attack finished quickly, and unlike the username results, the difference was obvious when I sorted by length. One payload had a noticeably smaller response length and a 302 status code, while every other response was a 200 OK.

![image-20260711090001599](./lab4.assets/image-20260711090001599.png)

I authenticated as **arizona** using that password.

![image-20260711090037251](./lab4.assets/image-20260711090037251.png)

### Solved!

![image-20260711090049187](./lab4.assets/image-20260711090049187.png)