writeup by wook413

### APPRENTICE LEVEL

# Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:

```
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products.

---

![image.png](./../../../../../../../../Program Files/Typora/attachment:7f21b82f-fced-429d-ac3b-fd67297d152b:image.png)

![image.png](./../../../../../../../../Program Files/Typora/attachment:eae11dd5-e940-4e7d-914e-6ed4d01cc0ad:image.png)

![image.png](./../../../../../../../../Program Files/Typora/attachment:372ce4f0-85de-4f40-a09a-6db2a7a10316:image.png)

![image.png](./../../../../../../../../Program Files/Typora/attachment:33c00eab-7f55-4bbc-8a23-be0da1748a76:image.png)
