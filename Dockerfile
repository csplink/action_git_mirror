FROM csplink/ubuntu_ci:22.04

RUN apt-get update
RUN apt-get install -y git openssh-client

ADD *.py /
ADD *.sh /

ENTRYPOINT ["python3", "/run.py"]
