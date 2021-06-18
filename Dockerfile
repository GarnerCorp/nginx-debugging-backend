FROM python:3-slim AS build-env
ADD . /app
WORKDIR /app

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --prefix=/app

# Add the application source code.
FROM gcr.io/distroless/python3
COPY --from=build-env /app /app

EXPOSE 8080:8080
CMD [ "/app/debug.py" ]
