echo "BUILD START"
pip install -r requirements.txt
python manage.py collectstatic --no-input
# python install psycopg2
# python install psycopg2-binary
echo "BUILD END"