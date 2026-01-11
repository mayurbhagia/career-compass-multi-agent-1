FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app
COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

COPY agentcore_simple_demo.py.

EXPOSE 8080
CMD ["python", "agentcore_simple_demo.py"]