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
        sh '''
          set -e
          TRIVY_VERSION="0.57.1"

          if ! command -v trivy >/dev/null 2>&1; then
            curl -fsSL -o trivy.tar.gz "https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-64bit.tar.gz"
            tar -xzf trivy.tar.gz trivy
            chmod +x trivy
            mv trivy /usr/local/bin/trivy
            rm -f trivy.tar.gz
          fi

          docker save "${IMAGE_FULL}" -o image.tar
          trivy image --input image.tar --severity HIGH,CRITICAL --exit-code 1 --no-progress
          rm -f image.tar
        '''
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
