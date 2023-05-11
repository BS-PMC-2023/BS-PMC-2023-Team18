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
                dir('main/rewear/Rewear/rewear_project') { // change to the rewear_project directory
                    sh 'pipenv run python manage.py test'
                }
            }
        }
 //           post {
 //               always {
 //                   junit 'dashboard/tests.xml'
 //               }
//            }
        }
    }
}
