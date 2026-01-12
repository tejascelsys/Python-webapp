import os
import dataikuapi

# Configuration from Environment Variables
DSS_URL = os.getenv("DSS_URL")
API_KEY = os.getenv("DSS_API_KEY")
PROJECT_KEY = "ADMIN_CLEANUP_PROJECT"
WEBAPP_ID = "X1kdb8M"
FILE_PATH = "backend/python.py"  # The file in your repo containing the code

client = dataikuapi.DSSClient(DSS_URL, API_KEY)
project = client.get_project(PROJECT_KEY)
webapp = project.get_webapp(WEBAPP_ID)

# 1. Read the code from the repo file
with open(FILE_PATH, "r") as f:
    repo_code = f.read()

# 2. Update Dataiku
settings = webapp.get_settings()
settings.get_raw()['params']['python'] = repo_code
settings.save()
print(f"Successfully synced {FILE_PATH} to Dataiku.")

# 3. Restart Backend
webapp.start_or_restart_backend().wait_for_result()
print("Web app restarted.")
