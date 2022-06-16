FROM python:3.9.5

EXPOSE 8501

# PYTHONBUFFERED true

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD streamlit run src/app.py
