# Local Jenkins setup

This folder starts Jenkins using the requested image:
- `ghcr.io/imagegenius/jenkins:latest`

## Start Jenkins

From this folder run:

```cmd
docker compose up -d
```

## Check container status

```cmd
docker ps
docker logs q1-jenkins
```

## Open Jenkins

Open in browser:
- `http://localhost:8080`

## Stop Jenkins

```cmd
docker compose down
```

## Notes

- Jenkins data is stored in the named volume `jenkins_home`.
- Docker socket is mounted so Jenkins can try to run Docker commands from the pipeline.
- If this image does not contain the Docker CLI, the pipeline's Docker build and Trivy stages will fail. In that case, keep the same Jenkins image and attach a separate Jenkins agent that has Docker installed, or switch to a Jenkins image that includes Docker CLI.
