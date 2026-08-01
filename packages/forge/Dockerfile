# WiseGen Forge, sovereign image: no package installs, no network at build or run.
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    FORGE_NETWORK=deny \
    FORGE_ESTATE=docker

WORKDIR /app

# Run as a non-root identity. The agent runtime never needs elevation.
RUN useradd --create-home --uid 10001 forge

COPY --chown=forge:forge . /app

USER forge

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python3 -m wisegen_forge.cli doctor || exit 1

ENTRYPOINT ["python3", "-m", "wisegen_forge.cli"]
CMD ["--help"]
