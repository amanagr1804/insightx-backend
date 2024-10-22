import os

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your_google_client_id")

# MongoDB URI (DocumentDB)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
