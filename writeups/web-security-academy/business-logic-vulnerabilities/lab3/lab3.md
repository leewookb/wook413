Write-up by wook413

# Lab: Inconsistent security controls

This lab's flawed logic allows arbitrary users to access administrative functionality that should only be available to company employees. To solve the lab, access the admin panel and delete the user `carlos`.

---

Unlike the previous labs, this lab has a **Register** button next to **My account**.

![image-20260806235101365](./lab3.assets/image-20260806235101365.png)

After clicking the **Register** button, I found a feature for creating a new account. At the top of the page, there was a message saying, "**If you work for DontWannaCry, please use your @dontwannacry.com email address.**"

![image-20260806235133791](./lab3.assets/image-20260806235133791.png)

Since I am obviously not an employee of DontWannaCry, I clicked on **Email Client** and used the provided email address, `attacker@exploit-0a030098047070e180e348c101e20038.exploit-server.net`, to register an account.

![image-20260806235438243](./lab3.assets/image-20260806235438243.png)

![image-20260806235509197](./lab3.assets/image-20260806235509197.png)

After clicking **Register**, I opened **Email Client** again and found an email in the inbox asking me to confirm my email address and complete the registration.

![image-20260806235536132](./lab3.assets/image-20260806235536132.png)

I clicked the link in the email, and the page displayed **"Account registration successful!"**.

![image-20260806235557219](./lab3.assets/image-20260806235557219.png)

I then navigated to the **My account** tab and successfully logged in as the `wook` user. I noticed that there was an **Update email** feature.

![image-20260806235622918](./lab3.assets/image-20260806235622918.png)

Just in case, I tried changing my email address to `wook@dontwannacry.com`.

![image-20260806235704639](./lab3.assets/image-20260806235704639.png)

Surprisingly, my email address was successfully changed to `wook@dontwannacry.com`, and an **Admin panel** tab appeared at the same time.

![image-20260806235725216](./lab3.assets/image-20260806235725216.png)

After clicking on the **Admin panel**, I could see a list of users.

![image-20260806235738935](./lab3.assets/image-20260806235738935.png)

Following the lab objective, I deleted the `carlos` user and successfully completed the lab.

### Solved!

![image-20260806235753291](./lab3.assets/image-20260806235753291.png)







