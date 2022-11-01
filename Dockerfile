# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

FROM python:3.10-bullseye AS builder

ARG src_dir='/tmp/cryptonite'
ARG PIP_NO_CACHE_DIR=0

COPY . "$src_dir"

RUN python3 -m venv /opt/pyenv --upgrade
RUN /opt/pyenv/bin/pip3 install "$src_dir"

FROM python:3.10-slim-bullseye AS final
COPY --from=builder /opt/pyenv /opt/pyenv

ENV VIRTUAL_ENV=/opt/pyenv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN cryptonite --help
RUN cryptonite --version

ENTRYPOINT [ "cryptonite" ]

# https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys
LABEL org.opencontainers.image.authors='Roberto Rossini <roberros@uio.no>'
LABEL org.opencontainers.image.url='https://github.com/robomics/2022-sbi-ci-workshop'
LABEL org.opencontainers.image.documentation='https://github.com/robomics/2022-sbi-ci-workshop'
LABEL org.opencontainers.image.source='https://github.com/robomics/2022-sbi-ci-workshop'
LABEL org.opencontainers.image.licenses='MIT'
LABEL org.opencontainers.image.title='2022-sbi-ci-workflow-cryptonite'
