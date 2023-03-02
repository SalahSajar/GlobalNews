echo "BUILD START"
pip install -r requirements.txt
python manage.py collectstatic --no-input

echo "BUILD END"