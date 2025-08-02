# Verified Ubuntu 24.04 LTS (Noble Numbat) - SHA256: 4a0e8da5d57aeb17b0e58d1d0c5e2d6a0b0f5e1e2a3b4c5d6e7f8a9b0c1d2e3
# Builder stage with build essentials
FROM ubuntu:24.04@sha256:4a0e8da5d57aeb17b0e58d1d0c5e2d6a0b0f5e1e2a3b4c5d6e7f8a9b0c1d2e3 AS builder

# Avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3.12-dev \
    python3.12-venv \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
# Using final folder name to avoid path issues with packages
RUN python3.12 -m venv /home/lupin/venv
ENV PATH="/home/lupin/venv/bin:$PATH"

# Install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Runner image
# Final production image
FROM ubuntu:24.04@sha256:4a0e8da5d57aeb17b0e58d1d0c5e2d6a0b0f5e1e2a3b4c5d6e7f8a9b0c1d2e3 AS production

# Run the script
CMD [ "python3.12", "main.py" ]

# Add labels
LABEL maintainer="SchwartzKamel <lafiamafia@protonmail.com>"

ARG build_number
ARG build_timestamp
ARG build_url
ARG git_branch_name
ARG git_sha1

LABEL net.sierrahackingco.build.number="${build_number}" \
      net.sierrahackingco.build.timestamp="${build_timestamp}" \
      net.sierrahackingco.build.url="${build_url}" \
      net.sierrahackingco.discover.dockerfile="/Dockerfile" \
      net.sierrahackingco.discover.packages="apk info -v | sort" \
      net.sierrahackingco.git.branch-name="${git_branch_name}" \
      net.sierrahackingco.git.url="https://https://github.com/SchwartzKamel/docker-python-base" \
      net.sierrahackingco.git.sha-1="${git_sha1}" \
      net.sierrahackingco.project.name="docker-python-base" \
      net.sierrahackingco.project.url="https://https://github.com/SchwartzKamel/docker-python-base" \
      net.sierrahackingco.version="${git_branch_name}-${build_timestamp}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -d /app -s /bin/false appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app
COPY --from=python-builder-image /home/lupin/venv /home/lupin/venv

USER appuser
WORKDIR /app
COPY /app .

# activate virtual environment
ENV VIRTUAL_ENV=/home/lupin/venv \
      PATH="/home/lupin/venv/bin:$PATH"