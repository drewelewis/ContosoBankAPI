@echo off
echo Setting up ContosoBankAPI database...
echo.

echo Step 1: Ensuring Docker containers are running...
docker-compose up -d postgres
echo Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak > nul

echo.
echo Step 2: Creating database tables...
python database/create_database.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to create database tables!
    pause
    exit /b 1
)

echo.
echo Step 3: Seeding database with test data...
python database/seed_database.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to seed database!
    pause
    exit /b 1
)

echo.
echo ✅ Database setup completed successfully!
echo   - Database created (if needed)
echo   - Tables created
echo   - Test data seeded
echo.
pause
