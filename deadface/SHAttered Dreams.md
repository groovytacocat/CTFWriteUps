Challenge:

>DEADFACE is on the brink of selling a patient's credit card details from the Aurora database to a dark web buyer. Investigate Ghost Town for potential leads on the victim's identity.
Submit the flag as flag{Firstname Lastname}. Example: flag{John Smith}.
Use the database dump from Aurora Compromise.


Looking at the GhostTown forum there are 2 posts to note
>I’ll let him know! I told him to put this SHA1 hash in the notes of the transaction so we have a record of what was sold: 911d1fc5930fa5025dbc2d3953c94de9e4773584

and

>No I’m actually including almost the full billing and patient data. I’m just concatenating the following:

    card number
    expiration
    CCV
    patient_id
    patient first name
    patient last name
    patient middle initial
    patient sex
    patient email
    patient address (street, city, state, zip)
    patient dob

Using this information, create a file with every billing record concatenated in the above format
```
SELECT CONCAT(b.card_num, b.exp, b.ccv, p.patient_id, p.first_name, p.last_name, p.middle, p.sex, p.email, p.street, p.city, p.state, p.zip, p.dob)
FROM billing b
INNER JOIN patients p
ON b.patient_id = p.patient_id
INTO OUTFILE '/path/to/file.txt'
```

Once this file is created hash all the lines (I used this https://gist.github.com/pcorpet/dd8432ec3bcc2ee8bb26f376c5c73464) 
```
python3 hashctf.py file.txt output.txt
```

Probably an easier/better way to do this but once the output file is generated used vim to search the file for the above hash from Lilith
>Line is 8164

Go back to mysql and run the same query as earlier with the addition of LIMIT to get that specific row (0-index so use 8163)
```
mysql> SELECT CONCAT(b.card_num, b.exp, b.ccv, p.patient_id, p.first_name, p.last_name, p.middle, p.sex, p.email, p.street, p.city, p.state, p.zip, p.dob), b.patient_id FROM billing b INNER JOIN patients p ON b.patient_id = p.patient_id LIMIT 8163,1;
+----------------------------------------------------------------------------------------------------------------------------------------------+------------+
| CONCAT(b.card_num, b.exp, b.ccv, p.patient_id, p.first_name, p.last_name, p.middle, p.sex, p.email, p.street, p.city, p.state, p.zip, p.dob) | patient_id |
+----------------------------------------------------------------------------------------------------------------------------------------------+------------+
| 50483743238485412026-0498316314BertonLuchettiXMalebluchetti6ar@taobao.com39 Meadow Ridge TerraceClevelandOH441251964-10-29                   |      16314 |
+----------------------------------------------------------------------------------------------------------------------------------------------+------------+
1 row in set (0.01 sec)
```

From the concatenated string we can see Berton Luchetti is the name of the patient.
