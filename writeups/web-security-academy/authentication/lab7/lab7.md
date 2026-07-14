Write-up by wook413

# Lab: Username enumeration via account lock

This lab is vulnerable to username enumeration. It uses account locking, but this contains a logic flaw. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

---

I went straight to the login form and tried and invalid credential pair, `wook:wook`.

![image-20260713202428572](./lab7.assets/image-20260713202428572.png)

The server returned "**Invalid username or password.**" I sent the same request through Burp Repeater more than 10 times, but it kept returning the same message. No account lockout occurred.

![image-20260713202656096](./lab7.assets/image-20260713202656096.png)

I suspected the lockout logic was flawed and only triggered for valid usernames. To test this theory, I sent the request to Burp Intruder and set the attack type to **Cluster bomb**. I added a payload position on the `username` parameter, and a second, blank payload position after the `password` value.

![image-20260713203931977](./lab7.assets/image-20260713203931977.png)

For the second position, I set the payload type to `Null payloads` and configured it to generate 5 payloads. This effectively repeats each username 5 times in a row, letting me check whether any username triggers a lockout after repeated failed attempts.

![image-20260713204009469](./lab7.assets/image-20260713204009469.png)

I ran the attack, and only one payload group returned a different response length. `app01`.

![image-20260713204058543](./lab7.assets/image-20260713204058543.png)

Pulling it up, the server returned **"You have made too many incorrect login attempts. Please try again in 1 minute(s)."**

![image-20260713204140346](./lab7.assets/image-20260713204140346.png)

Every other request still returned **"Invalid username or password"**, confirming those usernames were invalid.

![image-20260713204208173](./lab7.assets/image-20260713204208173.png)

Now that I had a valid username, it was time to find the password. I switched the attack type back to **Sniper**, set the `password` parameter as the payload position, and loaded the provided password wordlist.

![image-20260713204308233](./lab7.assets/image-20260713204308233.png)

I ran the attack. All requests returned a **200 OK** status, as expected. One payload returns a distinct response length of 3266 with no error message. This is a strong indicator of success. Three payloads returned 3344, containing "**Invalid username or password,**" and the rest returned 3396, containing "**You have made too many incorrect login attempts. Please try again in 1 minute(s)**". This confirmed the account locks after 3 failed attempts: the first 3 wrong guesses return the standard error, and every attempt after that returns the lockout message instead until the successful attempt breaks the pattern.

![image-20260713204510322](./lab7.assets/image-20260713204510322.png)

I successfully authenticated as `app01` with the password.

### Solved!

![image-20260713204559212](./lab7.assets/image-20260713204559212.png)

