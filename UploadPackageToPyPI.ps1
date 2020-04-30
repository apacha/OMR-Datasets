# Before running these command,
# - check __init__.py for the right version number,
# - update release notes in CHANGES.md
# - Optionally check setup.py if descriptions need adaption
python setup.py sdist
twine upload --repository pypi dist/*

# Remove the dist directory to avoid conflicts with later uploads
rmdir dist /S /Q
rmdir omrdatasettools.egg-info /S /Q
