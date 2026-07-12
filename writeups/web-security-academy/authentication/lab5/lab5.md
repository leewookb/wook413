Write-up by wook413

# Lab: Username enumeration via response timing

This lab is vulnerable to username enumeration using its response times. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

- Your credentials `wiener:peter`
- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

### Hint

To add to the challenge, the lab also implements a form of IP-based brute-force protection. However, this can be easily bypassed by manipulating HTTP request headers.

---

After opening the lab, I went straight to the login page.

![image-20260712104315527](./lab5.assets/image-20260712104315527.png)

I sent the login request to Intruder.

![image-20260712104448269](./lab5.assets/image-20260712104448269.png)

I set the username parameter as the payload position and loaded the provided username wordlist as the payload set.

![image-20260712104555376](./lab5.assets/image-20260712104555376.png)

Almost every response came back with "**You have made too many incorrect login attempts. Please try again in 30 minute(s)**".

![image-20260712104743165](./lab5.assets/image-20260712104743165.png)

I took the request to Repeater to investigate further. I added an `X-Forwarded-For` header to the request, and the block message disappeared.

![image-20260712110831661](./lab5.assets/image-20260712110831661.png)

However, I found that after 3 invalid login attempts from the same `X-Forwarded-For` value, that "IP" got blocked again meaning I'd need to rotate the header value to keep bypassing the block.

![image-20260712110916576](./lab5.assets/image-20260712110916576.png)

With a way to bypass the block, my next step was finding a valid username. I first tried an invalid username `wook413`, which returned a response time of 203 ms.

![image-20260712111018377](./lab5.assets/image-20260712111018377.png)

I then tried the known-valid username `wiener`, which returned a response time of 158 ms.

![image-20260712111126585](./lab5.assets/image-20260712111126585.png)

When I significantly increased the length of the password value, the response time for `wiener` rose to 253 ms.

![image-20260712111212092](./lab5.assets/image-20260712111212092.png)

Increasing it further pushed the response time to 667 ms. This confirmed a timing pattern: for a valid username, the server takes measurably longer to process a long password (since it actually runs the password through the hashing function), while for an invalid username, the server short-circuits and skips that steps regardless of password length.

![image-20260712111240743](./lab5.assets/image-20260712111240743.png)

With a way to distinguish valid from invalid usernames, I went back to Intruder and switched the attack type to **Pitchfork**, since I now needed to vary both the username and the `X-Forwarded-For`  value simultaneously. I set the `X-Forwarded-for` payload to numbers 1-101, and used the provided username wordlist for the username field. I also set the password field to single very long value to maximize the timing difference.

![image-20260712111549942](./lab5.assets/image-20260712111549942.png)

I ran the attack, and it completed quickly. One payload stood out with a noticeably longer response time: `info`. Based on my earlier theory, this had to be the valid username.

![image-20260712111735139](./lab5.assets/image-20260712111735139.png)

With a candidate valid username, I switched the payload position from username to password and loaded the provided password wordlist. I again varied `X-Forwarded-For` to avoid getting blocked, this time using numbers 102-201.

![image-20260712111955305](./lab5.assets/image-20260712111955305.png)

I ran the attack and sorted the results by status code. Only one request returned a `302`, revealing the correct password for `info`.

![image-20260712112039013](./lab5.assets/image-20260712112039013.png)

![image-20260712112113716](./lab5.assets/image-20260712112113716.png)

I went back to the login page, entered `info:131313`, and intercepted the request. I added `X-Forwarded-For: 413` (an unused value) since my IP was still blocked from earlier attempts.

![image-20260712112257508](./lab5.assets/image-20260712112257508.png)

I forwarded the request and successfully authenticated as `info`.

### Solved!

![image-20260712112336103](./lab5.assets/image-20260712112336103.png)



