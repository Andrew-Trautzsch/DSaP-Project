CREATE TABLE healthcare (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each record
    first_name VARCHAR(50),             -- First name
    last_name VARCHAR(50),              -- Last name
    gender TEXT,                     -- TRUE for male, FALSE for female
    age TEXT,                            -- Age
    weight FLOAT,                       -- Weight in kg
    height FLOAT,                       -- Height in meters
    healthcarehealthcarehealth_history TEXT,                 -- Detailed health information
    data_hash VARCHAR(64)
);

CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL
);

INSERT INTO roles (role_name) VALUES ('H'), ('R');

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
