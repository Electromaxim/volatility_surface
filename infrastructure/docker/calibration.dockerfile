FROM nvcr.io/nvidia/pytorch:22.12-py3
WORKDIR /app

# Install Swiss financial stack
RUN pip install quantlib-python swissfinancials==1.4.0

# Install project dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# FINMA-approved memory limits
ENV OMP_NUM_THREADS=8
ENV CUDA_MEM_LIMIT="12GB"

# Entrypoint for calibration job
CMD ["python", "pricing/main.py", "--run-calibration"]