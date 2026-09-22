pipeline {
  agent any
  options { timestamps() }
  environment {
    IMAGE_REPOSITORY = 'registry.example.com/platform/order-api'
    IMAGE_TAG = "${env.GIT_COMMIT}"
  }
  stages {
    stage('Validate') {
      steps { sh 'python -m compileall app' }
    }
    stage('Build immutable image') {
      steps { sh 'docker build -t $IMAGE_REPOSITORY:$IMAGE_TAG .' }
    }
    stage('Security gates') {
      steps {
        sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_REPOSITORY:$IMAGE_TAG'
      }
    }
    stage('Publish') {
      steps { sh 'docker push $IMAGE_REPOSITORY:$IMAGE_TAG' }
    }
    stage('Deploy staging') {
      steps { sh 'kubectl -n staging set image deployment/order-api api=$IMAGE_REPOSITORY:$IMAGE_TAG' }
    }
  }
}
