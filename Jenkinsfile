pipeline {
    agent {
        docker {
            image 'python:3.9' // Docker image to use
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root' // Add -u root option for elevated permissions
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'pip install pipenv'
                sh 'pipenv install'
            }
        }

        stage('Test') {
            steps {
                sh 'pipenv run pytest'
            }
        }
    }
}
