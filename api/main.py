#!/usr/bin/env python
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=4000, debug=True)
