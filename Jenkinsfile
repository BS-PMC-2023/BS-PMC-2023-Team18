pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-u root:root'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python manage.py test dashboard.tests'
            }
 //           post {
 //               always {
 //                   junit 'dashboard/tests.xml'
 //               }
//            }
        }
    }
}
