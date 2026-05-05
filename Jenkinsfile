pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Repositorio conectado'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'

                    withSonarQubeEnv('sonar-local') {
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=otransfer-frontend \
                        -Dsonar.sources=. \
                        -Dsonar.exclusions=**/venv/**,**/.scannerwork/**,**/allure-report/**,**/allure-results/**,**/reports/**,**/__pycache__/**
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Selenium Tests') {
            steps {
                sh '''
                cd tests/selenium
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install allure-pytest
                pytest --alluredir=allure-results
                '''
            }
        }

        stage('Allure Report') {
            steps {
                allure([
                    commandline: 'Allure',
                    includeProperties: false,
                    results: [[path: 'tests/selenium/allure-results']]
                ])
            }
        }

        stage('OWASP ZAP Scan') {
            steps {
                sh '''
                    mkdir -p reports/zap
                    chmod -R 777 reports/zap

                    docker run --rm \
                    -u root \
                    -v $(pwd)/reports/zap:/zap/wrk \
                    ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
                    -t https://otransfer.chimera.pe \
                    -r zap-report.html || true
                '''
            }
        }
    }
}