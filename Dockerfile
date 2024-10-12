FROM python:3.10 AS base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install pip and poetry
RUN python -m pip install --upgrade pip && \
    pip install poetry

# Create a virtual environment
RUN python -m venv /venv

# Copy the project files
COPY pyproject.toml poetry.lock README.md ./

# Install wheel
RUN pip install wheel

# Install dependencies
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

# Copy the rest of the project files
COPY . .

# Build and install the wheel
RUN poetry build -f wheel && /venv/bin/pip install dist/*.whl

# Place the contacts.vcf file in the /app directory
RUN cp /venv/lib/python3.10/site-packages/tests/data/contactlookup_sample_contacts.vcf \
    /app/contacts.vcf

# Remove everything except the run.sh file and the contacts.vcf file
RUN rm -rf contactlookup \
    pyproject.toml \
    poetry.lock \
    README.md \
    tests \
    dist

# Remove the installed tests directory
RUN rm -rf /venv/lib/python3.10/site-packages/tests

# Run the application with the contacts.vcf file as the default argument
ENV PATH="/venv/bin:${PATH}"
CMD ["contactlookup", "-f", "contacts.vcf"]
