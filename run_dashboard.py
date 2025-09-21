# This script is the entry point for running the dashboard.
# It imports the app from the dashboard module and runs it.

from src.dashboard.app import app

if __name__ == '__main__':
    # Running the app with host='0.0.0.0' makes it accessible from
    # outside the container, which is useful for development.
    # The port is set to 8080.
    app.run(host='0.0.0.0', port=8080, debug=True)
