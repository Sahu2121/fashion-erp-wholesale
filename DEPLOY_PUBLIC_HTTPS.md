# FASHION ERP WHOLESALE — Public HTTPS deployment

## Render deployment
1. Create a GitHub repository and upload this folder.
2. In Render, create a new **Web Service** from the repository.
3. Build command: `python -m py_compile app.py web_app.py`
4. Start command: `python web_app.py`
5. Render provides an HTTPS URL such as `https://fashion-erp-wholesale.onrender.com`.
6. Open that URL in Chrome.

Login:
- User ID: `admin`
- Password: `Admin@123`

Important: this build uses SQLite. On hosted services, local disk may be ephemeral. For production multi-user use, move the database to a managed persistent database/storage before relying on it for business records.
