Challenge:

>DEADFACE has taken responsibility for a partial database hack on a pharmacy tied to Aurora Pharmaceuticals. The hacked data consists of patient data, staff data, and information on drugs and prescriptions.
>We’ve managed to get a hold of the hacked data. Provide the first and last name of the patient that lives on a street called Hansons Terrace.

Given the database dump as a .sql file and the System Design Specifications

Opening up the Design Specs and going to Section 3.4 to see Table Design for Table names and information

See tehre is a Patients table and a street field that is common to multiple tables.

Create a blank database and import the data into it (googled how to use mysql cli)

```
sudo mysql testdb < aurora.sql
```

Open up mysql and query the tables to find the data we're looking for
```
sudo mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Server version: 8.0.34-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> use testdb;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```

Since we want the patient that lives on Hansons Terrace query the patients table to find that info
```
mysql> SELECT first_name, last_name
    -> FROM patients
    -> WHERE street LIKE '%Hansons Terrace';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| Sandor     | Beyer     |
+------------+-----------+
1 row in set (0.01 sec)

```

Therefore the answer is flag{Sandor Beyer}
