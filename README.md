# Tecta Stock API

- This project demonstrates a simple **FastAPI** backend that retrieves stock market data using `yfinance`, calculates basic statistics, and exposes it via a REST API. The backend is fully containerized using Docker.

---

## **Features**

- Retrieve historical price data for a given ticker symbol.
- Calculate basic key figures/statistics: `high`, `low`, `average`, `last_close`.
- Fetch data on demand from Yahoo Finance (`yfinance`).
- Fully containerized backend with Docker.

🔹 Caching

- This API implements in-memory caching to improve performance and reduce repeated calls to Yahoo Finance (yfinance).

- Cached data is stored per ticker and date range.

- Cache expiration time (TTL) is 5 minutes.


---

## **Installation & Setup**

### **1. Clone the repository**

```bash
git clone <https://github.com/abdo-elbeltagy/tecta-backend-task.git>
cd tecta

# Build Docker Image
docker build -t tecta-api .

# Run Container
docker run -d -p 8000:8000 --name tecta-container tecta-api

# API Example
GET http://localhost:8000/api/stats?ticker=MSFT&start=2023-01-01&end=2023-12-31

# Expected JSON response:

{
  "high": 250.0,
  "low": 240.0,
  "average": 245.3,
  "last_close": 247.0
}

# Stopping the container

docker stop tecta-container
docker rm tecta-container

# Running Tests
pytest

```

## CI/CD Pipeline Overview

This project uses a CI/CD pipeline to automate testing, building, and deployment of the Docker container. The pipeline can be implemented using GitHub Actions or a similar CI/CD tool.

---

### Continuous Integration (CI)

The CI workflow runs on every push or pull request. It ensures that the code is tested and the Docker image can be built successfully.

```yaml
on: [push, pull_request]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run automated tests
        run: pytest --maxfail=1 --disable-warnings -q

      - name: Build Docker image
        run: docker build -t tecta-api .
```

### Continuous Deployment (CD)

The CD workflow runs on merge to the main branch. It pushes the Docker image to a registry and deploys the container to a server or cloud environment.

```yaml
jobs:
  cd:
    runs-on: ubuntu-latest
    needs: ci
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Login to Docker Hub
        run: echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin

      - name: Push Docker image
        run: |
          docker tag tecta-api myusername/tecta-api:latest
          docker push myusername/tecta-api:latest

      - name: Deploy to server
        run: |
          ssh deployuser@myserver.com "docker pull myusername/tecta-api:latest && \
                                        docker stop tecta-api-container || true && \
                                        docker rm tecta-api-container || true && \
                                        docker run -d -p 8000:8000 --name tecta-api-container myusername/tecta-api:latest"


```

## **Requirements**


- Python 3.11+

- Docker 20+

- Internet connection (for yfinance API)

## **References**

- FastAPI Documentation

- yfinance Documentation

- Docker Documentation
