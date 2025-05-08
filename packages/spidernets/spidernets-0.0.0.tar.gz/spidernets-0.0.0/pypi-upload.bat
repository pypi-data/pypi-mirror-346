uv build
twine check dist/*
twine upload --skip-existing dist/*
pause
