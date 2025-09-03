CREATE SCHEMA IF NOT EXISTS open_engage_ph_schema;

-- 3. Check the exact database you're connected to
SELECT current_database();

SELECT EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_schema = 'public'  -- ← Change to public
    AND table_name = 'admin'
);

SELECT * FROM end_user;
SELECT * FROM base_users;