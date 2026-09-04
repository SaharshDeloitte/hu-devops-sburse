# Question 1 - Jenkins CI Pipeline (Beginner Guide)

This project contains a complete sample for:
1. Build Docker image
2. Trivy scan (fail on HIGH/CRITICAL)
3. Push to private Docker Hub repo
4. Trigger manually and every 5 minutes

## Project structure

- `question1/Jenkinsfile`
- `question1/sample-app/app.py`
- `question1/sample-app/requirements.txt`
- `question1/sample-app/Dockerfile`

## Step 0 - Create GitHub repository with proper name

Use your assignment naming format:
- `HU-DevOps-<deloitte-id>`

Example:
- `HU-DevOps-abc123`

## Naming pattern checklist

Use these names consistently in your submission:

1. Jenkins Job Name:
- `<deloitte-id>-docker-trivy-pipeline-q1`

2. Commit Message Pattern:
- `feat(q1-jenkins): <what changed>`
- `fix(q1-jenkins): <issue resolved>`

3. Pull Request Title Pattern:
- `Q1 Jenkins | <deloitte-id> | Docker build + Trivy + Docker Hub push`

## Step 1 - Prerequisites (on Jenkins agent machine)

Install:
- Docker
- Git

Quick check commands:

```bash
docker --version
git --version
```

Expected output:
- command prints installed version numbers

## Step 2 - Push this code to your GitHub repo

```bash
git init
git add .
git commit -m "feat(q1-jenkins): add docker build trivy gate and dockerhub push"
git branch -M main
git remote add origin https://github.com/<your-user>/HU-DevOps-<deloitte-id>.git
git push -u origin main
```

Expected output:
- repository created and files pushed to `main`

## Step 3 - Create private Docker Hub repository

1. Login to Docker Hub
2. Create a new repository
3. Set visibility to Private
4. Copy repo name in this format:
   - `<dockerhub-username>/<private-repo-name>`

Example:
- `myuser/hu-devops-private`

## Step 4 - Update Jenkinsfile values

Open `question1/Jenkinsfile` and replace:
- `DOCKERHUB_REPO = 'sah642/hu_devops'`
with your actual private repo.

Example:
- `myuser/hu-devops-private`

## Step 5 - Add Docker Hub credentials in Jenkins

In Jenkins UI:
1. Manage Jenkins
2. Credentials
3. Add Credentials
4. Kind: Username with password
5. Username: your Docker Hub username
6. Password: Docker Hub password or access token
7. ID: `dockerhub-creds`
8. Save

This ID must exactly match the Jenkinsfile.

## Step 6 - Create Jenkins Pipeline job

1. New Item
2. Enter name: `<deloitte-id>-docker-trivy-pipeline-q1`
3. Select Pipeline
4. In Pipeline section:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: your GitHub repo URL
   - Branch: `*/main`
   - Script Path: `question1/Jenkinsfile`
5. Save

## Step 7 - Validate manual trigger

1. Click Build Now
2. Open build logs

Expected stage flow:
1. Checkout
2. Build Docker Image
3. Quality Gate - Trivy
4. Push To Private Docker Hub

If Trivy finds HIGH/CRITICAL vulnerabilities:
- Build fails at Trivy stage (this is expected behavior)

If no HIGH/CRITICAL vulnerabilities:
- Build succeeds
- Image is pushed to private Docker Hub repo

## Step 8 - Validate scheduled trigger every 5 minutes

The Jenkinsfile includes:

```groovy
triggers {
  cron('H/5 * * * *')
}
```

Meaning:
- Pipeline runs automatically every 5 minutes
- `H/5` spreads jobs to reduce server load

Expected output:
- new builds appear automatically in Build History

## Step 9 - Important code explanation

### Environment variables
- `DOCKERHUB_REPO`: private Docker Hub repo path
- `IMAGE_TAG`: uses Jenkins build number
- `IMAGE_FULL`: final image name and tag

Example:
- `myuser/hu-devops-private:12`

### Trivy gate command

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL --exit-code 1 --no-progress <image>
```

What it does:
- scans image for vulnerabilities
- looks only for HIGH and CRITICAL
- returns exit code 1 if found
- pipeline stops and fails

### Docker push stage
- logs in to Docker Hub using Jenkins credentials
- pushes image to private repo
- logs out

## Step 10 - Common issues and fixes

1. `docker: command not found`
- Fix: install Docker CLI on the Jenkins agent and ensure daemon access

2. `Cannot connect to the Docker daemon`
- Fix: ensure Docker daemon is running and Jenkins user has Docker permission

3. `unauthorized: incorrect username or password`
- Fix: re-check `dockerhub-creds` username/password/token

4. `name unknown: repository does not exist`
- Fix: ensure private repo exists and name is exact in Jenkinsfile

5. Pipeline does not run every 5 minutes
- Fix: verify Jenkins timezone and confirm job is saved after Jenkinsfile update

6. Trivy image pull fails (rate limit or network issue)
- Fix: verify internet egress from Jenkins agent and pre-pull `aquasec/trivy:latest` if needed

## Step 11 - Screenshot checklist (for assignment submission)

Capture screenshots of:
1. Jenkinsfile with cron + stages
2. Jenkins credentials (`dockerhub-creds`) setup page (hide password)
3. Manual build success
4. Scheduled build execution in Build History
5. Trivy failure example (if vulnerability found)
6. Trivy success after issue fix
7. Private Docker Hub repo showing pushed image tag
8. PR page showing required PR naming pattern
9. Commit history showing required commit naming pattern

Save these under:
- `question1/screenshots/` (see `question1/screenshots/README.md` for exact filenames)

