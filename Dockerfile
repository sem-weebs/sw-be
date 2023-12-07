FROM python:3-alpine AS builder
 
WORKDIR /
 
RUN python3 -m venv venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
COPY requirements.txt .
RUN pip install -r requirements.txt
 
# Stage 2
FROM python:3-alpine AS runner
 
WORKDIR /
 
COPY --from=builder /venv venv
COPY app.py app.py
COPY wsgi.py wsgi.py
COPY sparql.py sparql.py
COPY .enviro .enviro
 
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=/wsgi.py
 
EXPOSE 8080
 
CMD ["gunicorn", "--bind" , ":8080", "--workers", "2", "wsgi:app"]