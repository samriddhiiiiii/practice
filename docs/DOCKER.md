# Run the app with Docker

## Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop).
  - On Windows, enable the WSL 2 backend in Docker settings.

## Start
```bash
docker compose up --build
```

Open http://localhost:5000

## Notes
- The first build may take several minutes (TensorFlow/OpenCV).
- If port 5000 is busy, edit `docker-compose.yml` to map `"5001:5000"` and open http://localhost:5001.
- If the build fails due to low memory, consider switching to `tensorflow-cpu==2.13.0` in `requirements.txt` and rebuild.

## Production-style serving (optional)
Uncomment the `gunicorn -k eventlet` command in `docker-compose.yml` for a production-friendly WebSocket server.
