# Build stage: build the wheel and pin dependencies from poetry.lock
FROM python:3.11-slim AS build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /src
RUN pip install poetry poetry-plugin-export

COPY pyproject.toml poetry.lock README.md ./
# --without-hashes: export leaves uvloop out of this lock file, and pip's hash
# mode refuses to install anything not listed (uvicorn[standard] pulls it in)
RUN poetry export --without dev --without-hashes -f requirements.txt -o requirements.txt

COPY contactlookup ./contactlookup
COPY tests/data ./tests/data
RUN poetry build -f wheel


# Runtime stage: just the app, no poetry, running as a normal user
FROM python:3.11-slim
LABEL org.opencontainers.image.title="contactlookup" \
      org.opencontainers.image.description="Self-hosted contacts API for searching a VCF file" \
      org.opencontainers.image.authors="Bryan Wodi" \
      org.opencontainers.image.source="https://github.com/talk2bryan/contactlookup" \
      org.opencontainers.image.licenses="GPL-3.0"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    CONTACTLOOKUP_HOST=0.0.0.0 \
    CONTACTLOOKUP_PORT=8000

COPY --from=build /src/requirements.txt /src/dist/*.whl /tmp/
RUN pip install -r /tmp/requirements.txt \
    && pip install --no-deps /tmp/*.whl \
    && rm -rf /tmp/* \
    # the wheel ships the sample data as a top-level "tests" package; drop it
    && rm -rf "$(python -c 'import site; print(site.getsitepackages()[0])')/tests"

# /app holds the contacts file and the log file, so the app user needs to own it
RUN useradd --uid 10001 --create-home app && mkdir /app && chown app:app /app
WORKDIR /app
COPY --from=build --chown=app:app /src/tests/data/contactlookup_sample_contacts.vcf /app/contacts.vcf

USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["contactlookup", "--file", "/app/contacts.vcf"]
