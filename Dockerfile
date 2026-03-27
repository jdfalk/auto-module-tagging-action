FROM python:3.14-slim@sha256:486b8092bfb12997e10d4920897213a06563449c951c5506c2a2cfaf591c599f

WORKDIR /repo

RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

COPY src/tag_modules.py /usr/local/bin/tag_modules.py

ENTRYPOINT ["python", "/usr/local/bin/tag_modules.py"]
