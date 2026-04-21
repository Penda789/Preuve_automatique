FROM coqorg/coq:8.19

USER root
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

USER coq
RUN opam update && opam install -y coq-serapi

ENV PATH=/home/coq/.opam/default/bin:$PATH
WORKDIR /workspace
