Write-up by wook413

# Lab: File path traversal, traversal sequences blocked with absolute path bypass

This lab contains a path traversal vulnerability in the display of product images.

The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.

To solve the lab, retrieve the contents of the `/etc/passwd` file.

---

This is what the landing page of the lab looks like.

![image-20260721205038292](./lab2.assets/image-20260721205038292.png)

According to the lab description, the application contains a path traversal vulnerability in the product image endpoint. To test this, I clicked on a random product, **Cheshire Cat Grin**.

![image-20260721205051911](./lab2.assets/image-20260721205051911.png)

I right-clicked product image and selected "**Open image in new tab.**" Notice that the URL changed and now includes a `filename` parameter.

`https://0a6e0037042d2814897913ee00c4007a.web-security-academy.net/image?filename=5.jpg`

![image-20260721205108697](./lab2.assets/image-20260721205108697.png)

As shown below, the GET request to `/image?filename=5.jpg` returns the binary data of the requested image.

![image-20260721205142777](./lab2.assets/image-20260721205142777.png)

Although the lab states that path traversal sequences are blocked, I tested them to observer the server's behavior. I supplied `../../../etc/passwd` as the `filename` parameter, and the server responded with **"No such file"**.

![image-20260721205235962](./lab2.assets/image-20260721205235962.png)

However, when I supplied `/etc/passwd` as an absolute path without using any traversal sequences, the server successfully returned the contents of the `/etc/passwd` file.

![image-20260721205258549](./lab2.assets/image-20260721205258549.png)

### Solved!

![image-20260721205314851](./lab2.assets/image-20260721205314851.png)