FROM continuumio/conda-ci-linux-64-python3.8@sha256:2a4a96ec883df5e2cf0c0ea75001aa79b7fbd4d0fb460f7335944528b9477614
USER root

RUN apt update \
    && apt install -y --no-install-recommends \
    bzip2 \
    build-essential \
    curl \
    gcc \
    git \
    wget \
    ca-certificates \
    curl \
    procps \
    gettext-base \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC


WORKDIR /workdir
SHELL ["/bin/bash", "-c"]


# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
ADD notebook/.jupyter /root/.jupyter

# Pip install
ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt



#ENV PATH /opt/conda/envs/inu_radar/bin:$PATH

ENV PYTHONPATH $PYTHONPATH:/workdir/tabooword:/workdir

WORKDIR /workdir