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

  options {
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('sample-app') {
          script {
            if (isUnix()) {
              sh "docker build -t ${IMAGE_FULL} ."
            } else {
              bat "docker build -t ${IMAGE_FULL} ."
            }
          }
        }
      }
    }

    stage('Trivy Security Scan') {
      steps {
        script {
          if (isUnix()) {
            sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL --exit-code 1 --no-progress ${IMAGE_FULL}"
          } else {
            bat "docker run --rm -v //var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL --exit-code 1 --no-progress ${IMAGE_FULL}"
          }
        }
      }
    }

    stage('Push To Docker Hub Private Repo') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
          script {
            if (isUnix()) {
              sh 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
              sh "docker push ${IMAGE_FULL}"
              sh 'docker logout'
            } else {
              bat 'echo %DOCKERHUB_PASS% | docker login -u %DOCKERHUB_USER% --password-stdin'
              bat "docker push ${IMAGE_FULL}"
              bat 'docker logout'
            }
          }
        }
      }
    }
  }

  post {
    always {
      script {
        if (isUnix()) {
          sh "docker image rm -f ${IMAGE_FULL} || true"
        } else {
          bat "docker image rm -f ${IMAGE_FULL}"
        }
      }
    }
    success {
      echo "Pipeline passed: image built, scanned, and pushed successfully."
    }
    failure {
      echo "Pipeline failed. Check Trivy and Docker stage logs for details."
    }
  }
}
