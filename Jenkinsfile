@Library('Logs_OPT')_
pipeline {
    agent any
    options {
        ansiColor('xterm')
    }
    stages {
        stage('Hello') {
            steps {
                script{
                    logs.echoStage("hello")
                }
            }
        }
    }
}
