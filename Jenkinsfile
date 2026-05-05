pipeline {
    agent any

    tools {
        sonarRunner 'sonar-scanner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Repositorio conectado'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-local') {
                    bat '''
                    sonar-scanner ^
                    -Dsonar.projectKey=otransfer-frontend ^
                    -Dsonar.sources=.
                    '''
                }
            }
        }
    }
}