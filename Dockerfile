ARG ARCH=
FROM ${ARCH}python:3.13-slim AS build-env

COPY . /tmp
WORKDIR /app
RUN chown 1000 .
USER 1000

# Run pip to install all dependencies into the virtualenv.
RUN pip install -r /tmp/requirements.txt --prefix=/app

# Add the application source code.
FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
COPY --from=build-env /tmp/*.py /tmp/version /app

EXPOSE 8080:8080
CMD [ "/app/debug.py" ]
