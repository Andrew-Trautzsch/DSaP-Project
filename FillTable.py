import mysql.connector
import random
import Hash
import Encryption

# Database connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='database'
)

cursor = connection.cursor(dictionary=True)

# Sample data
firstNamesList = ['John', 'Jane', 'Jack', 'Jill', 'Joe', 'Jenny', 'Jerry', 'Judy', 'Jim', 'Jill']
lastNamesList = ['Smith', 'Jones', 'Brown', 'White', 'Black', 'Green', 'Blue', 'Red', 'Gray', 'Davis']
healthHistoriesList = ["N/A", "Heart Disease", "Diabetes", "Cancer", "Asthma", "Arthritis", "Alzheimer's", "Stroke", "Obesity", "Osteoporosis"]

# Insert 100 rows into the healthcare table
for i in range(100):
    firstName = random.choice(firstNamesList)
    lastName = random.choice(lastNamesList)
    gender = random.choice([True, False])
    age = random.randint(18, 100)
    weight = round(random.uniform(50.0, 120.0), 1)
    height = round(random.uniform(1.5, 2.0), 2)
    healthHistory = random.choice(healthHistoriesList)
    
    encryptedGender = Encryption.encryptData(gender)
    encryptedAge = Encryption.encryptData(age)
    
    # Prepare data for hashing
    newData = {
        "first_name": firstName,
        "last_name": lastName,
        "gender": encryptedGender,
        "age": encryptedAge,
        "weight": weight,
        "height": height,
        "health_history": healthHistory
    }
 
    # Compute data hash
    dataHash = Hash.computeDataHash(newData)
    
    # Insert record into the database
    query = """
        INSERT INTO healthcare (first_name, last_name, gender, age, weight, height, health_history, data_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (firstName, lastName, encryptedGender, encryptedAge, weight, height, healthHistory, dataHash)
    cursor.execute(query, values)

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("100 rows of data inserted successfully!")
