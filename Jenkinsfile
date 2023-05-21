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

        stage('Test') {
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
//                 dir('rewear/Rewear/rewear_project'){
//                     sh """
//                         # export DJANGO_SETTINGS_MODULE='Rewear.settings'
//                         coverage report
//                         """
//                 }
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
