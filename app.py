import os
import logging
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Import routes
from routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
