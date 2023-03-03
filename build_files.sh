echo "BUILD START"
pip install -r requirements.txt
python manage.py collectstatic --no-input
pip install --upgrade setuptools
echo "BUILD END"