# Repository Notes

## Default Environment

- Backend Python environment is `conda` env `shop`
- Python version target is `3.11`
- Backend commands should prefer `conda run -n shop python ...`
- Frontend uses local Node.js and `npm`

## Backend Commands

- Install dependencies: `conda run -n shop python -m pip install -r backend/requirements.txt`
- Django check: `conda run -n shop python .\backend\manage.py check`
- Run server: `conda run -n shop python .\backend\manage.py runserver`
- Run tests: `conda run -n shop python -m pytest ...`

## Testing Notes

- `pytest.ini` defines `DJANGO_SETTINGS_MODULE = config.settings`
- Use the `shop` environment for all Django and pytest commands
