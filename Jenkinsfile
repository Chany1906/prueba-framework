pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Repositorio conectado'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-local') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=otransfer-frontend \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=sqp_dc662a71bbe38ef376de8690183b3e7efe734d04
                    '''
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}