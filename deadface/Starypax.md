Challenge: 

>Starypax (street name STAR) is a controlled substance and is in high demand on the Dark Web. DEADFACE might leverage this database to find out which patients currently carry STAR.
How many patients in the Aurora database have an active prescription for Starypax as of Oct 20, 2023? And whose prescription expires first?
Submit the flag as flag{#_firstname lastname}.
Use the database dump from Aurora Compromise.

Looking at the aurora dump db there are 3 tables that wil give all the info necessary (I starred the important ones)

```
+--------------------+
| Tables_in_testdb   |
+--------------------+
| billing            |
| credit_types       |
| drugs              |*****
| facilities         |
| insurors           |
| inventory          |
| orders             |
| patients           |*****
| positions          |
| positions_assigned |
| prescriptions      |*****
| staff              |
| suppliers          |
| transactions       |
+--------------------+
```

Looking at the drugs and prescriptions tables since we all we'll need patients for is the names.
```
mysql> describe drugs; describe prescriptions;
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| drug_id     | int           | NO   | PRI | NULL    | auto_increment |
| drug_name   | varchar(56)   | NO   | UNI | NULL    |                |
| description | varchar(4096) | NO   |     | NULL    |                |
| supplier_id | int           | NO   | MUL | NULL    |                |
| cost        | float         | YES  |     | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+
5 rows in set (0.01 sec)

+-----------------+---------------+------+-----+---------+----------------+
| Field           | Type          | Null | Key | Default | Extra          |
+-----------------+---------------+------+-----+---------+----------------+
| prescription_id | int           | NO   | PRI | NULL    | auto_increment |
| patient_id      | int           | NO   | MUL | NULL    |                |
| drug_id         | int           | NO   | MUL | NULL    |                |
| doctor_id       | int           | NO   | MUL | NULL    |                |
| date_prescribed | date          | NO   |     | NULL    |                |
| instructions    | varchar(4096) | YES  |     | NULL    |                |
| refills         | int           | NO   |     | NULL    |                |
| expiration      | date          | NO   |     | NULL    |                |
+-----------------+---------------+------+-----+---------+----------------+
```

Obtain the drug id for Starypax from the drugs table
```
mysql> SELECT drug_id
    -> FROM drugs
    -> WHERE drug_name = 'Starypax';
+---------+
| drug_id |
+---------+
|      26 |
+---------+
```

Now using this, query the prescriptions table for the names and expiration dates of patients with this drug
```
mysql> SELECT p.patient_id, t.first_name, t.last_name, p.expiration
    -> FROM prescriptions p
    -> INNER JOIN patients t
    -> ON p.patient_id = t.patient_id
    -> WHERE p.drug_id = 26 AND p.expiration >= '2023-10-20'
    -> ORDER BY p.expiration desc;
+------------+------------+-----------+------------+
| patient_id | first_name | last_name | expiration |
+------------+------------+-----------+------------+
|      14322 | Lenci      | Springett | 2023-12-19 |
|      13779 | Appolonia  | Benda     | 2023-11-26 |
|      18086 | Chic       | Abrashkov | 2023-11-20 |
|      11367 | Rodi       | Godfery   | 2023-11-04 |
|      10482 | Eolanda    | Maciaszek | 2023-10-31 |
|      12013 | Chrissie   | Hargraves | 2023-10-28 |
|      10042 | Renae      | Allum     | 2023-10-26 |
+------------+------------+-----------+------------+
7 rows in set (0.00 sec)
```
Therefore the answer is flag{7_Renae Allum}
