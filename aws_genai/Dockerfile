# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
#RUN curl -sSL https://install.python-poetry.org | python3 -
RUN curl -sSL https://install.python-poetry.org | python3 -

#ENV PATH="${PATH}:/root/.poetry/bin"


# Copy the project configuration files
COPY pyproject.toml poetry.lock* /app/

# Disable virtualenv creation and interactive prompts
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install poetry

# Install project dependencies
#RUN poetry install --no-dev
RUN poetry install --no-dev --no-root


# Copy the rest of the project
COPY . /app

# Configure Streamlit environment variables
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLE_CORS=false

# Run the Streamlit application
CMD ["poetry", "run", "streamlit", "run", "adidas_aws_genai/src/app.py"]