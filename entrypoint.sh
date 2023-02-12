set -e
export FLASK_APP=main
flask db upgrade
gunicorn -b 0.0.0.0:8070 main