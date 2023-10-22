Challenge:

>Turbo Tactical wants you to determine how many credit cards are still potentially at risk of being used by DEADFACE. How many credit cards in the Aurora database are NOT expired as of Oct 2023?
>Submit the flag as flag{#}.
>Use the database dump from Aurora Compromise.

Going back to the design specs from the Aurora write up we see there is a Billing table with an "exp" field. 
Query the table to see the date format for expiration (only a portion of the table is shown)

```
mysql> SELECT * FROM billing;
|      14432 |      18531 |              2 | 5048378471577216 | 2026-04 | 707 |
|      14433 |      18532 |              3 | 5048370651304297 | 2023-08 | 626 |
|      14434 |      18533 |              1 | 5108759981217962 | 2025-11 | 934 |
|      14435 |      18534 |              2 | 5108750774567820 | 2025-01 | 403 |
|      14436 |      18535 |              1 | 5048377097626092 | 2023-07 | 242 |
|      14437 |      18536 |              3 | 5048373913468835 | 2023-12 | 501 |
|      14438 |      18537 |              2 | 5048373532496126 | 2027-12 | 109 |
|      14439 |      18538 |              3 | 5108756548124475 | 2024-12 | 730 |
|      14440 |      18539 |              2 | 5048373933148201 | 2026-08 | 497 |
|      14441 |      18540 |              1 | 5048377633656348 | 2023-02 | 436 |
|      14442 |      18541 |              1 | 5108756191160065 | 2025-05 | 476 |
+------------+------------+----------------+------------------+---------+-----+
```
Seeing the YYYY-MM format query for cards that are not expired as of Oct 2023
```
mysql> SELECT COUNT(*) FROM billing WHERE exp >= '2023-10';
+----------+
| COUNT(*) |
+----------+
|     8944 |
+----------+
```

This was incorrect, I realized I was including cards that expired in Oct 2023
```
mysql> SELECT COUNT(*) FROM billing WHERE exp > '2023-10';
+----------+
| COUNT(*) |
+----------+
|     8785 |
+----------+
```

Therefore answer is flag{8785}
