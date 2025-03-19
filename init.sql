DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'devops') THEN 
        CREATE USER devops WITH PASSWORD 'devops24';
        ALTER USER devops WITH SUPERUSER;
    END IF; 
END $$;

CREATE DATABASE user_service;
CREATE DATABASE booking_service;
GRANT ALL PRIVILEGES ON DATABASE user_service TO devops;
GRANT ALL PRIVILEGES ON DATABASE booking_service TO devops;