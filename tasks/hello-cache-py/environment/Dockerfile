# Pin by digest in a real task:
#   FROM python@sha256:<digest>
# The tag below keeps the example readable; `scripts/validate-task.sh` will warn.
FROM python:3.12-slim

ENV PYTHONPATH=/task/src \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /task

# Copy only what the participant needs. reference/ and evaluation/ are never
# copied into the image — that separation is checked by the validator.
COPY src/ /task/src/

CMD ["sleep", "infinity"]
