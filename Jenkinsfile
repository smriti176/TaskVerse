
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Django System Check') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py check
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t smriti176/taskverse:latest .'
            }
        }
    }
}
