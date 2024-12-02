from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import Hash
import Encryption

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="database"
)

cursor = db.cursor(dictionary=True)


# Helper function: Authenticate user
def authenticate(username, password):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user and Hash.verifyPassword(password, user["password_hash"]):
        return user
    return None


# Home/Login page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate(username, password)
        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role_id"] = user["role_id"]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials", 403

    return render_template("login.html")


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role_id = request.form.get("role_id")

        if not username or not password or not role_id:
            return "All fields are required", 400

        try:
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return "Username already exists", 400

            # Hash the password and insert the new user into the database
            hashedPassword = Hash.hashPassword(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, role_id) VALUES (%s, %s, %s)",
                (username, hashedPassword, role_id),
            )
            db.commit()
            return redirect(url_for("home"))  # Redirect to login after registration

        except mysql.connector.Error as error:
            return f"Database error: {error}", 500

    return render_template("register.html")


# Dashboard (view and add data)
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))

    role_id = session["role_id"]

    # Add new data for healthcare admin
    if request.method == "POST" and role_id == 1:  # Only admins can add data
        newData = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "gender": Encryption.encryptData(request.form.get("gender")),  # Encrypt gender
            "age": Encryption.encryptData(request.form.get("age")),  # Encrypt age
            "weight": request.form.get("weight"),
            "height": request.form.get("height"),
            "health_history": request.form.get("health_history"),
        }

        # Compute data hash
        dataHash = Hash.computeDataHash(newData)

        cursor.execute(
            """INSERT INTO healthcare (first_name, last_name, gender, age, weight, height, health_history, data_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                newData["first_name"],
                newData["last_name"],
                newData["gender"],
                newData["age"],
                newData["weight"],
                newData["height"],
                newData["health_history"],
                dataHash,
            ),
        )
        db.commit()
        return redirect(url_for("dashboard"))  # Refresh the dashboard

    # Fetch data from the database
    cursor.execute("SELECT * FROM healthcare")  # Fetch all fields for verification
    fullDataSet = cursor.fetchall()

    # Verify single data item integrity
    verifiedData = []
    for data in fullDataSet:
        # Use all data fields for hash verification
        dataFields = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "gender": data.get("gender"),
            "age": data.get("age"),
            "weight": data.get("weight"),
            "height": data.get("height"),
            "health_history": data.get("health_history"),
        }
        if Hash.verifyDataHash(dataFields, data["data_hash"]):
            verifiedData.append(data)
        else:
            print(f"Data integrity failed for record ID: {data['id']}")

    # Compute query completeness hash
    completenessHash = Hash.computeDatasetHash(verifiedData)

    # Compare with the last known completeness hash
    last_completeness_hash = session.get("completenessHash")
    if last_completeness_hash and last_completeness_hash != completenessHash:
        print("Query completeness verification failed!")

    # Update session with the current completeness hash
    session["completenessHash"] = completenessHash

    # Prepare displayed data
    displayedData = []
    for data in verifiedData:
        if role_id == 1:  # Admin: Decrypt all fields except `data_hash`
            displayedData.append({
                "id": data["id"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "gender": Encryption.decryptData(data["gender"]),
                "age": Encryption.decryptData(data["age"]),
                "weight": data["weight"],
                "height": data["height"],
                "health_history": data["health_history"],
            })
        elif role_id == 2:  # Restricted: Decrypt only restricted fields
            displayedData.append({
                "id": data["id"],
                "gender": Encryption.decryptData(data["gender"]),
                "age": Encryption.decryptData(data["age"]),
                "weight": data["weight"],
                "height": data["height"],
                "health_history": data["health_history"],
            })

    return render_template(
        "dashboard.html",
        dataSet=displayedData,  # Pass displayed data to the template
        role_id=role_id
    )


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

