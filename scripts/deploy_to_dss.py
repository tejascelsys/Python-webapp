
import dataikuapi
import time, os
from pathlib import Path

# ---------------- CONFIG ----------------
DSS_URL = "https://design-node.labs.csi-infra.com"
API_KEY = os.environ["DSS_API_KEY"]   # from GitHub secret
PROJECT_KEY = "ADMIN_CLEANUP_PROJECT"
WEBAPP_ID = "X1kdb8M"
BACKEND_FILE = Path("backend/python.py")
# ----------------------------------------

# Read backend code from GitHub repo
backend_code = BACKEND_FILE.read_text()

# Add timestamp to force reload & avoid Flask caching
timestamp = int(time.time())
backend_code = f"# Update ID: {timestamp}\n\n{backend_code}"

client = dataikuapi.DSSClient(DSS_URL, API_KEY)
project = client.get_project(PROJECT_KEY)
webapp = project.get_webapp(WEBAPP_ID)

# Update backend
settings = webapp.get_settings()
raw_settings = settings.get_raw()
raw_settings["params"]["python"] = backend_code
settings.save()

print("✅ Backend code uploaded")

# Restart backend
print("🔄 Restarting WebApp backend...")
future = webapp.start_or_restart_backend()
future.wait_for_result()

print("🚀 WebApp backend restarted successfully")
