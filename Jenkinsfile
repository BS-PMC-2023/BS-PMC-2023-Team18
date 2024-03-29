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

        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt' // Install dependencies from requirements.txt
            }
        }

        stage('Unit testing') {
            steps {
                dir('rewear/Rewear/rewear_project'){
                 // Change to the rewear_project directory
//                     sh 'pipenv run python manage.py test' // Specify the path to manage.py
                    sh """
                        # export DJANGO_SETTINGS_MODULE='Rewear.settings'
                        python manage.py test
                        """
                }
            }
        }
        
        stage('integration testing') {
            steps {
                dir('rewear/Rewear/rewear_project'){
                 // Change to the rewear_project directory
//                     sh 'pipenv run python manage.py test' // Specify the path to manage.py
                    sh """
                        # export DJANGO_SETTINGS_MODULE='Rewear.settings'
                        python manage.py test
                        """
                }
            }
        }
        
       
        stage('Metrics 1 - Defect Density ') {
            steps {
                dir('rewear/Rewear/rewear_project'){
                    sh """
                        # export DJANGO_SETTINGS_MODULE='Rewear.settings'
                        python defect_density.py
                        """
                }
            }
        }
        
        stage('Metrics 2 - Covrage ') {
            steps {
                dir('rewear/Rewear/rewear_project'){
                    sh """
                        # export DJANGO_SETTINGS_MODULE='Rewear.settings'
                        coverage run manage.py test
                        coverage report 
                        """
                }
            }
        }
        
        stage('Metrics 3 - Code Complexity ') {
            steps {
                dir('rewear/Rewear/rewear_project'){
                    sh """
                        # export DJANGO_SETTINGS_MODULE='Rewear.settings'
                        pip install radon
                        radon cc --show-complexity --total-average .
                        """
                }
            }
        }
        
        stage('Metrics 4 - Maintainability Index ') {
            steps {
                dir('rewear/Rewear/rewear_project'){
                    sh """
                        # export DJANGO_SETTINGS_MODULE='Rewear.settings'
                        pip install radon
                        radon mi .
                        """
                }
            }
        }
    
    
    } // closing stages

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
