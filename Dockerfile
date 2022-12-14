FROM csplink/ubuntu_ci:22.04

RUN apt-get update
RUN apt-get install -y p7zip-full git

ADD run.py /run.py

ENTRYPOINT ["python3", "/run.py"]
