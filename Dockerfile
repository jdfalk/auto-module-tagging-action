FROM python:3.14-slim@sha256:5b3879b6f3cb77e712644d50262d05a7c146b7312d784a18eff7ff5462e77033

WORKDIR /repo

RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

COPY src/tag_modules.py /usr/local/bin/tag_modules.py

ENTRYPOINT ["python", "/usr/local/bin/tag_modules.py"]
