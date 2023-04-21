FROM python:3.8.10

ENV OPEN_AI_ORG=org-Yc1kT2em67dJKrbB2H6yutDq
ENV OPEN_AI_KEY=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
ENV ELEVEN_LABS_API_KEY=8e3f0bf4dc1412e4339928c4bfe57731

WORKDIR /src

ADD ./ /src

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]