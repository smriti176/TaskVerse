pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Django System Check') {
            steps {
                bat 'python manage.py check'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python manage.py test'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t smriti176/taskverse:latest .'
            }
        }
    }
}