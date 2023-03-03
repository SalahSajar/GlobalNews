echo "BUILD START"
pip install -r requirements.txt
python manage.py collectstatic --no-input
pip install psycopg2
pip install psycopg2-binary
echo "BUILD END"