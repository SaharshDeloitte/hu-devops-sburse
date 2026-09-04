pipeline {
  agent any

  triggers {
    cron('H/5 * * * *')
  }

  environment {
    DOCKERHUB_REPO = 'sah642/hu_devops'
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    IMAGE_FULL = "${DOCKERHUB_REPO}:${IMAGE_TAG}"
  }

  stages {
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ${IMAGE_FULL} sample-app'
      }
    }

    stage('Trivy Security Scan') {
      steps {
        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL --exit-code 1 --no-progress ${IMAGE_FULL}'
      }
    }

    stage('Push To Docker Hub Private Repo') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
          sh 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
          sh 'docker push ${IMAGE_FULL}'
          sh 'docker logout'
        }
      }
    }
  }

  post {
    always {
      sh 'docker image rm -f ${IMAGE_FULL} || true'
    }
  }
}
