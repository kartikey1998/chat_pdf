FROM python:3.10

COPY requirements.txt .

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Copy your project code
COPY . .
EXPOSE 8501
# Specify the command to run when the container starts
CMD streamlit run app.py --server.port=8501