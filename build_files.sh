echo "BUILD START"
python manage.py collectstatic --noinput
pip install -r requirements.txt
echo "BUILD END"