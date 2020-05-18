title get_me_some_data
cd C:\\Users\\rschuetz\\Downloads\\sport_lines (2)\\sport_lines\\sqlite3
REM TIMEOUT /T 10
sqlite3.exe sport_lines.db < "C:\Users\rschuetz\Downloads\sport_lines (2)\sport_lines\scripts\SQL\create_views.sql"
TIMEOUT /T 10