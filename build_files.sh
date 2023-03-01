echo "BUILD START"
# python manage.py collectstatic --noinput
pip install -r requirements.txt
python manage.py collectstatic
echo "BUILD END"