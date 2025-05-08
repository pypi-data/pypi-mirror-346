# OptiSpend

Estimate cloud savings plan commitments using historical billing data.

## 📦 Installation

```bash
pip install optispend
```

## 🚀 Usage

```bash
optispend --profile default --commitment 0.8
optispend --profile default --optimize
```

## 🐳 Docker

```bash
docker build -t optispend .
docker run --rm -v ~/.aws:/home/optispend/.aws:ro optispend --optimize
```

## 🛠 Usage with Makefile

### Install locally
```bash
make install
```

### Build Docker image
```bash
make build
```

### Run OptiSpend using Docker
```bash
make run
```

### Clean up build artifacts
```bash
make clean
```
