# PROJECT SETUP
uv self update

uv init
uv venv
source .venv/bin/activate

uv add fastapi
uv add uvicorn
uv add python-dotenv
uv pip freeze > requirements.txt

uvicorn app.main:app --reload --port 8001

which python
python -V

## DOCKER
# CLEAR SYSTEM
docker system prune -a --volumes

# DOCKER BUILD (CHECK IF BUILD IS OK)
docker build --platform linux/amd64 -t tomcity/fastapi:latest . --no-cache
docker run -it --rm tomcity/fastapi:latest sh
ls -R

# DOCKER BUILD
docker build --platform linux/amd64 -t tomcity/fastapi:latest .

# DOCKER PUSH TO HUB
docker push tomcity/fastapi:latest

# DOCKER RUN
docker run -dp 8001:8001 tomcity/fastapi:latest


# SET UP ENV VARS IN COOLIFY
services:
  fastapi:
    container_name: fastapi
    image: 'tomcity/fastapi:latest'
    restart: unless-stopped
    environment:
      - 'FASTAPI_KEY=${FASTAPI_KEY}'
    healthcheck:
      test:
        - CMD-SHELL
        - 'curl -f http://127.0.0.1:8001/health || exit 1'
      interval: 5s
      timeout: 20s
      retries: 10