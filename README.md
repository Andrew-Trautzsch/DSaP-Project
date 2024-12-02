# DSaP-Project

To run project

First install MySQL from https://dev.mysql.com/downloads/ and run setup

Also install dependancies in Dependancies.txt (pip install -r Dependancies.txt)

Upon setup, please set information to be correct in the code:

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="database"
)

Upon establishing connection, run SQL code in Schema.SQL
And run FillTable.py to populate healthcare table

from there open http://127.0.0.1:5000 to use the website
