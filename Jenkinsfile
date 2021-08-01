
pipeline {
    agent any
    stages {

        stage('new code') {
            steps {
                deleteDir()
                git branch: "docker", url: "https://github.com/kobe65218/Stock_analysis.git"
                sh 'ls -l'
                sh 'echo 123'
            }
        }

        stage('deploy') {
            steps {
                ansiblePlaybook(
                    disableHostKeyChecking: true,
                    credentialsId: 'aws_cd',
                    playbook: 'ansible_playbook.yaml',
                    inventory: '../host'
                    )
            }
        }



    }
}
