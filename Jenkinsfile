
pipeline {
    agent any
    stages {
        // pull ansible_playbook
        stage('pull new code') {
            steps {
                deleteDir()
                git branch: "docker", url: "https://github.com/kobe65218/Stock_analysis.git"
            }
        }

        // 執行 ansible_playbook
        stage('deploy') {
            steps {
                ansiblePlaybook(
                    disableHostKeyChecking: true,
                    credentialsId: 'gwc_cd',
                    playbook: 'ansible_playbook/ansible_playbook.yaml',
                    inventory: '../host'
                    )
            }
        }



    }
}
