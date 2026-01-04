FROM python:3.12-slim@sha256:a75662dfec8d90bd7161c91050be2e0a9b21d284f3b7a7253d5db25f7d583fb3

WORKDIR /repo

RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

COPY src/tag_modules.py /usr/local/bin/tag_modules.py

ENTRYPOINT ["python", "/usr/local/bin/tag_modules.py"]
