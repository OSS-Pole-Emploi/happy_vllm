

FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04 AS builder

COPY prebuildfs /
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install python common
RUN install_packages software-properties-common

RUN add-apt-repository -d -y 'ppa:deadsnakes/ppa'
RUN install_packages python3.11 python3.11-dev python3.11-venv python3-pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=true

ENV APP_NAME="happy_vllm"
ENV API_ENTRYPOINT="/happy_vllm/rs/v1"

LABEL maintainer="Agence Data Services"
LABEL description="Service REST happy_vllm"

RUN python -m venv /opt/venv \
    && pip install --upgrade pip
ENV VIRTUAL_ENV="/opt/venv" PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

# Install package
COPY pyproject.toml pyproject.toml
COPY setup.py setup.py
COPY src/ src/
COPY requirements.txt requirements.txt
COPY version.txt version.txt

RUN python -m pip install -r requirements.txt && python -m pip install .

FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

COPY prebuildfs /
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install python common
RUN install_packages software-properties-common

RUN add-apt-repository -d -y 'ppa:deadsnakes/ppa'
RUN install_packages python3.11 python3.11-dev python3.11-venv python3-pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=true

ENV APP_NAME="happy_vllm"
ENV API_ENTRYPOINT="/happy_vllm/rs/v1"

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY launch.sh /app

# Start API
EXPOSE 8000
CMD ["python", "/app/launch.py"]
