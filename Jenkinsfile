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
                pytest --alluredir=allure-results --junitxml=pytest-results.xml
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

        stage('Import Results to Xray') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'xray-creds',
                    usernameVariable: 'XRAY_CLIENT_ID',
                    passwordVariable: 'XRAY_CLIENT_SECRET'
                )]) {
                    sh '''
                    cd tests/selenium

                    XRAY_TOKEN=$(curl -s -X POST \
                    -H "Content-Type: application/json" \
                    -d "{\\"client_id\\": \\"$XRAY_CLIENT_ID\\", \\"client_secret\\": \\"$XRAY_CLIENT_SECRET\\"}" \
                    https://xray.cloud.getxray.app/api/v2/authenticate | tr -d '"')

                    curl -X POST \
                    -H "Content-Type: text/xml" \
                    -H "Authorization: Bearer $XRAY_TOKEN" \
                    --data @pytest-results.xml \
                    "https://xray.cloud.getxray.app/api/v2/import/execution/junit?testExecKey=DSO-7"
                    '''
                }
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

        stage('Test Jira Connection') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'jira-creds',
                    usernameVariable: 'JIRA_USER',
                    passwordVariable: 'JIRA_TOKEN'
                )]) {
                    sh '''
                    curl -u $JIRA_USER:$JIRA_TOKEN \
                    -X GET \
                    -H "Content-Type: application/json" \
                    https://sitio-pruebas.atlassian.net/rest/api/3/project
                    '''
                }
            }
        }
    }
}