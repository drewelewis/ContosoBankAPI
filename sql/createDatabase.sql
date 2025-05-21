    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    CREATE TABLE users (
        user_id uuid PRIMARY KEY NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL,
        username VARCHAR(100) NOT NULL,
        password_hash VARCHAR(150) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP,
        deleted_at TIMESTAMP
    );



