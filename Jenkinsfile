pipeline {
    agent any

    tools {
        sonarScanner 'sonar-scanner'
    }

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
                    -Dsonar.sources=.
                    '''
                }
            }
        }
    }
}