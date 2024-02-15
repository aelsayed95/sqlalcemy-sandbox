FROM python:3.11

WORKDIR /code
COPY requirements.txt requirements.txt
# RUN PIP_INDEX_URL="https://artlondon.dev.bloomberg.com/artifactory/api/pypi/bloomberg-pypi/simple" pip3 install -r requirements.txt
# RUN PIP_INDEX_URL="https://artlondon.dev.bloomberg.com/artifactory/api/pypi/bloomberg-pypi/simple" pip3 install -r requirements.txt
RUN pip install -r requirements.txt

COPY mysvc.py mysvc.py
CMD ["python", "-u", "mysvc.py"]
