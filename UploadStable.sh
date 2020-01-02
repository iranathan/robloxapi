echo "Uploading stable version"

read -sp 'Password: ' PASSWORD
USERNAME=iranathan

#Make sdist
python setup.py sdist
echo "Created sdist"
twine upload dist/* -u $USERNAME -p $PASSWORD
echo "Uploaded to pypi"
rm -r ./dist
