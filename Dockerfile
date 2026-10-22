FROM python:3.10-slim

# Instala dependências de compilação do sistema e git
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clona e compila a biblioteca C liboqs
RUN git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs.git && \
    cd liboqs && \
    mkdir build && cd build && \
    cmake -DBUILD_SHARED_LIBS=ON .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig

# Instala as dependências de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o script de benchmark
COPY benchmark.py .

CMD ["python", "benchmark.py"]