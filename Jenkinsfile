pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install -e .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m unittest discover tests
                    http-request-builder --ci --ci-config examples/example_requests.json --report jenkins_report.html
                '''
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: '*.html',
                    reportName: 'HTTP Tests Report'
                ])
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
