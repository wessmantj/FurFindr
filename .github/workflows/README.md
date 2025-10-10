# Removed GitHub Actions workflows
# 
# These workflows were trying to run ETL in GitHub Actions and commit the database.
# This doesn't work because:
# 1. db/app.db is in .gitignore
# 2. SQLite databases shouldn't be in version control
# 3. Streamlit Cloud uses its own database (not from git)
#
# For production ETL:
# - Run locally with cron (see ETL_EMAIL_SETUP_GUIDE.md)
# - OR deploy to Heroku with Scheduler
# - OR use cloud database (PostgreSQL) with scheduled jobs
