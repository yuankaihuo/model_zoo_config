FROM masidocker/public:deep_brain_seg_v1_1_0

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates

WORKDIR /app

COPY main.py /app/main.py

ENTRYPOINT ["/pythondir/miniconda/bin/python", "main.py"]