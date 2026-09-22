pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
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
        TEST_IMAGE = 'order-api:test'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                sh 'git rev-parse HEAD'
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

        stage('Validate') {
            steps {
                sh '''
                    docker run --rm \
                      ${TEST_IMAGE} \
                      python -m compileall app
                '''
            }
        }

        stage('Build Immutable Image') {
            steps {
                sh '''
                    docker build \
                      --target runtime \
                      -t ${IMAGE_REPOSITORY}:${GIT_COMMIT} \
                      .
                '''
            }
        }

        stage('Verify Image') {
            steps {
                sh '''
                    docker image inspect \
                      ${IMAGE_REPOSITORY}:${GIT_COMMIT}
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
                      ${IMAGE_REPOSITORY}:${GIT_COMMIT}
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
                      ${IMAGE_REPOSITORY}:${GIT_COMMIT}
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
                      api=${IMAGE_REPOSITORY}:${GIT_COMMIT}

                    kubectl -n staging rollout status \
                      deployment/order-api
                '''
            }
        }
    }

    post {
        success {
            echo "CI pipeline succeeded for commit ${env.GIT_COMMIT}"
        }

        failure {
            echo "CI pipeline failed. Investigate the failed stage and console logs."
        }

        always {
            echo "Jenkins build: ${env.BUILD_NUMBER}"
            echo "Git commit: ${env.GIT_COMMIT}"
        }
    }
}
