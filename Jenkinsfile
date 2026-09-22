pipeline {
    agent any

    options {
        timestamps()
    }

    parameters {
        booleanParam(
            name: 'RUN_SECURITY_SCAN',
            defaultValue: false,
            description: 'Run Trivy image security scan'
        )

        booleanParam(
            name: 'PUBLISH_IMAGE',
            defaultValue: false,
            description: 'Push image to the configured container registry'
        )

        booleanParam(
            name: 'DEPLOY_STAGING',
            defaultValue: false,
            description: 'Deploy the image to the Kubernetes staging namespace'
        )
    }

    environment {
        IMAGE_REPOSITORY = 'registry.example.com/platform/order-api'
        IMAGE_TAG = ''
        TEST_IMAGE = 'order-api:test'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse HEAD',
                        returnStdout: true
                    ).trim()

                    echo "Building Git commit: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Validate') {
            steps {
                sh 'python -m compileall app'
            }
        }

        stage('Quality Gate') {
            steps {
                sh '''
                    docker build \
                      --target test \
                      -t ${TEST_IMAGE} \
                      .
                '''
            }
        }

        stage('Build Immutable Image') {
            steps {
                sh '''
                    docker build \
                      --target runtime \
                      -t ${IMAGE_REPOSITORY}:${IMAGE_TAG} \
                      .
                '''
            }
        }

        stage('Verify Image') {
            steps {
                sh '''
                    docker image inspect \
                      ${IMAGE_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }

        stage('Security Gates') {
            when {
                expression {
                    params.RUN_SECURITY_SCAN
                }
            }

            steps {
                sh '''
                    trivy image \
                      --exit-code 1 \
                      --severity HIGH,CRITICAL \
                      ${IMAGE_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }

        stage('Publish') {
            when {
                expression {
                    params.PUBLISH_IMAGE
                }
            }

            steps {
                sh '''
                    docker push \
                      ${IMAGE_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy Staging') {
            when {
                expression {
                    params.DEPLOY_STAGING
                }
            }

            steps {
                sh '''
                    kubectl -n staging set image \
                      deployment/order-api \
                      api=${IMAGE_REPOSITORY}:${IMAGE_TAG}

                    kubectl -n staging rollout status \
                      deployment/order-api
                '''
            }
        }
    }

    post {
        success {
            echo "CI pipeline succeeded for commit ${IMAGE_TAG}"
        }

        failure {
            echo "CI pipeline failed. Investigate the failed stage and console logs."
        }

        always {
            echo "Jenkins build: ${BUILD_NUMBER}"
            echo "Git commit: ${IMAGE_TAG}"
        }
    }
}
