Write-up by wook413

# Lab: Username enumeration via different responses

This lab is vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

---

From the main page of the lab, I clicked "My account."

![image-20260709210556972](./lab1.assets/image-20260709210556972.png)

I entered `wook:wook` in the username and password fields and clicked **Log in**.

![image-20260709210640340](./lab1.assets/image-20260709210640340.png)

In Burp, I saw the POST request I had just made, and the body clearly showed `username=wook&password=wook`

![image-20260709210812319](./lab1.assets/image-20260709210812319.png)

I sent that request to Intruder and marked the username value as the target position.

![image-20260709211447682](./lab1.assets/image-20260709211447682.png)

For payloads, I used the provided wordlist of usernames.

![image-20260709211048650](./lab1.assets/image-20260709211048650.png)

I ran the attack, which finished in a few seconds. Sorting the results by length, I noticed that one payload `archie` produced a response length different from all the others.

![image-20260709211614958](./lab1.assets/image-20260709211614958.png)

Looking at that response, it said "Incorrect password."

![image-20260709211641704](./lab1.assets/image-20260709211641704.png)

Every other response, by contrast, said "Invalid username." This difference confirms that the user archie exists.

![image-20260709211735166](./lab1.assets/image-20260709211735166.png)

Now that I knew archie was a valid username, I set up a new attack to find his password, this time marking the password field as the target position.

![image-20260709211853519](./lab1.assets/image-20260709211853519.png)

For payloads, I used the provided wordlist of passwords.

![image-20260709211931016](./lab1.assets/image-20260709211931016.png)

I ran the attack, which again finished quickly. One request stood out: it returned status code 302 with a response length of 188, while every other request returned length 3354.

![image-20260709212004091](./lab1.assets/image-20260709212004091.png)

The 302 status code indicated a redirect, meaning the login had succeeded, so the payload used for that request must be archie's correct password.

![image-20260709212027863](./lab1.assets/image-20260709212027863.png)

All the other responses simply contained "Incorrect password."

![image-20260709212054159](./lab1.assets/image-20260709212054159.png)

I logged in with archie and the identified password.

![image-20260709212123737](./lab1.assets/image-20260709212123737.png)

### Solved!

![image-20260709212135882](./lab1.assets/image-20260709212135882.png)



