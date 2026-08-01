FROM node:20-bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends chromium ca-certificates tini \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package.json package-lock.json* ./
COPY . .

ENV CHROMIUM_PATH=/usr/bin/chromium \
    CONTROL_HOST=0.0.0.0 \
    CONTROL_PORT=8787 \
    BROWSER_NO_SANDBOX=1

RUN useradd --create-home --uid 10001 appuser \
  && chown -R appuser:appuser /app
USER appuser

EXPOSE 8787
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["node", "src/cli.js", "serve"]
