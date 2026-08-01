FROM node:20-alpine
WORKDIR /app
COPY . .
RUN chmod +x bin/wisegen
USER node
CMD ["node", "src/cli.mjs", "verify"]
