
# remove previous releases
rm -rf build/ dist/ waybackmachine.egg-info/ __pycache__/
# compile
python setup.py sdist bdist_wheel
# publish
python -m twine upload dist/*