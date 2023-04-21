FROM python:3.8.10

ENV OPEN_AI_ORG=org-Yc1kT2em67dJKrbB2H6yutDq
ENV OPEN_AI_KEY=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
ENV ELEVEN_LABS_API_KEY=8e3f0bf4dc1412e4339928c4bfe57731

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

