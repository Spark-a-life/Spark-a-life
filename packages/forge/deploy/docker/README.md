# Docker

```bash
docker compose up                        # deterministic profile, internal network only
docker compose --profile sovereign up    # adds a local model runtime, still no egress
```

The image installs nothing at build time. The compose network is marked `internal: true`, so egress is absent rather than merely discouraged.
