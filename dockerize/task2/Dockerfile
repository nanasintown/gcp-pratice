ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

RUN apt-get update

RUN if [ "$PYTHON_VERSION" = "3.10" ]; then \
  apt-get install -y python3.10 python3-distutils curl && \
  curl  https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3.10 get-pip.py; fi 

RUN if [ "$PYTHON_VERSION" = "3.11" ]; then \
  apt install -y curl python3-pip gcc pylint \
  && curl -o python3_11.tar.gz https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz \
  && tar -xzf python3_11.tar.gz && rm python3_11.tar.gz \
  && cd Python-3.11.0 \
  && ./configure --with-ensurepip=install \
  && make -j 8 \
  && make install \
  && cp /usr/local/bin/python3.11 /usr/bin/python3 \
  && cp /usr/local/bin/pip3.11 /usr/bin/pip3; fi

RUN pip3 install wheel pytest pylint nbmake
