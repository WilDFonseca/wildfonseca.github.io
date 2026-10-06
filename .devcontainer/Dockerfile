FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 dev \
    && useradd --uid 1000 --gid dev --create-home --shell /bin/bash dev

WORKDIR /workspace
USER dev

CMD ["sleep", "infinity"]
