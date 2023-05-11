pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
        }
        dir '/var/jenkins_home/workspace/Team-18/rewear_project'
    }



    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install pipenv') {
            steps {
                sh 'apt-get update' // Update package lists
                sh 'apt-get install -y python3-dev python3-pip' // Install Python and pip
                sh 'pip install pipenv' // Install pipenv
            }
        }

        stage('Build') {
            steps {
                sh 'pipenv install --skip-lock' // Create and activate virtual environment, install dependencies (skip lock)
                sh 'pipenv install -r requirements.txt' // Install dependencies from requirements.txt
            }
        }

        stage('Test') {
            steps {
                dir('rewear_project') { // change to the rewear_project directory
                    sh 'pipenv run python manage.py test'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'pipenv run python manage.py migrate' 
                sh 'nohup pipenv run python manage.py runserver & sleep 5' 
                sh 'pipenv run python manage.py test' 
                script {
                    def processIds = sh(script: "ps aux | grep 'python manage.py runserver' | grep -v grep | awk '{print \$2}'", returnStdout: true).trim()
                    if (processIds) {
                        sh "echo '${processIds}' | xargs -r kill -9"
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'find . -name "*.pyc" -delete' // Remove compiled Python files
            junit allowEmptyResults: true, testResults: '**/test-results/*.xml'
            cleanWs(cleanWhenNotBuilt: false, deleteDirs: true, disableDeferredWipeout: true, notFailBuild: true, patterns: [[pattern: '.gitignore', type: 'INCLUDE'],  [pattern: '.propsfile', type: 'EXCLUDE']])
        }

        success {
            echo 'Build successful!' // Display success message
        }

        failure {
            echo 'Build failed!' // Display failure message
        }
    }
}
