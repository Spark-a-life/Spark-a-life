FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
ENTRYPOINT ["wisegen-pip"]
CMD ["run", "examples/executive-brief/project.yaml"]
