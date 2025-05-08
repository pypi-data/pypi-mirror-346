FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    cmake \
    patchelf \ 
    libffi-dev \
    libssl-dev \
    libpoppler-glib-dev \   
    libpoppler-cpp-dev \   
    libpoppler-dev \         
    libpoppler-private-dev \ 
    clang \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    pkg-config \
    libglib2.0-dev \
    libcairo2-dev \
    libjpeg-dev \          
    libopenblas-dev \       
    liblapack-dev \         
    gfortran \               
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Rust with default toolchain
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"

# Install maturin with latest version
RUN pip install --upgrade pip && \
    pip install maturin==0.14.1  # Pinned version for stability

# Create app directory
WORKDIR /app

# Copy your code
COPY . .

# Build the Python extension with all optimizations
RUN maturin build --release --strip -o dist --features=pyo3/extension-module

RUN pip install dist/*.whl