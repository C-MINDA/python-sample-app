pipeline {
    agent any
    
    environment {
        SONAR_TOKEN = credentials('sonarqube-token')
        BUILD_NUMBER = "${env.BUILD_NUMBER}"
        SONAR_PROJECT_KEY = 'Python-Sample-App'
        SONAR_PROJECT_NAME = 'Python Sample App'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "=== CHECKOUT STAGE ==="
                    echo "Repository: ${env.GIT_URL}"
                    echo "Commit: ${env.GIT_COMMIT}"
                    echo "Build: #${BUILD_NUMBER}"
                    
                    sh 'ls -la'
                    sh 'git log --oneline -3'
                }
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    echo "=== ENVIRONMENT SETUP ==="
                    sh '''
                        echo "Python version:"
                        python3 --version || python --version
                        
                        echo "Project files:"
                        ls -la
                        
                        echo "SonarQube configuration:"
                        cat sonar-project.properties
                    '''
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo "=== SONARQUBE ANALYSIS ==="
                    echo "Analyzing project: ${SONAR_PROJECT_KEY}"
                    
                    withSonarQubeEnv('SonarQube-Local') {
                        def scannerHome = tool name: 'SonarQube-Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                        
                        sh """
                            export PATH="${scannerHome}/bin:\$PATH"
                            echo "Scanner path: ${scannerHome}"
                            
                            # Test SonarQube connectivity
                            curl -I http://sonarqube:9000 || curl -I http://localhost:9000 || curl -I http://host.docker.internal:9000
                            
                            sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.projectName="${SONAR_PROJECT_NAME}" \
                            -Dsonar.projectVersion=1.0.${BUILD_NUMBER} \
                            -Dsonar.sources=. \
                            -Dsonar.exclusions="**/*test*.py,**/venv/**,**/__pycache__/**" \
                            -Dsonar.host.url=\${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_TOKEN} \
                            -Dsonar.scm.provider=git \
                            -Dsonar.qualitygate.wait=true \
                            -Dsonar.qualitygate.timeout=300
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    script {
                        echo "=== QUALITY GATE EVALUATION ==="
                        
                        def qg = waitForQualityGate()
                        
                        echo "Quality Gate Status: ${qg.status}"
                        echo "Project: ${SONAR_PROJECT_KEY}"
                        echo "Build: #${BUILD_NUMBER}"
                        
                        if (qg.status != 'OK') {
                            echo "❌ Quality Gate Failed!"
                            echo "Failed conditions:"
                            
                            if (qg.conditions) {
                                qg.conditions.each { condition ->
                                    if (condition.status != 'OK') {
                                        echo "  • ${condition.metricKey}: ${condition.actualValue} vs threshold ${condition.errorThreshold}"
                                    }
                                }
                            }
                            
                            // Mark as unstable for learning purposes
                            echo "⚠️  Marking build as UNSTABLE due to quality gate failure"
                            currentBuild.result = 'UNSTABLE'
                            
                        } else {
                            echo "✅ Quality Gate Passed!"
                        }
                    }
                }
            }
        }
        
        stage('Results Summary') {
            steps {
                script {
                    echo "=== SECURITY ANALYSIS SUMMARY ==="
                    echo "🔍 Expected security issues in codebase:"
                    echo "  • SQL injection vulnerabilities"
                    echo "  • Hardcoded credentials and secrets"
                    echo "  • Weak MD5 hashing algorithm"
                    echo "  • Command injection potential"
                    echo "  • Information disclosure in logging"
                    echo ""
                    echo "📊 View detailed results:"
                    echo "🔗 SonarQube: http://localhost:9000/dashboard?id=${SONAR_PROJECT_KEY}"
                    echo "🔧 Jenkins: ${env.BUILD_URL}"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "=== PIPELINE COMPLETION ==="
                echo "Repository: ${env.GIT_URL}"
                echo "Build: #${BUILD_NUMBER}"
                echo "Duration: ${currentBuild.durationString}"
                echo "Result: ${currentBuild.result ?: 'SUCCESS'}"
                echo ""
                echo "📊 SonarQube Dashboard: http://localhost:9000/dashboard?id=${SONAR_PROJECT_KEY}"
            }
        }
        success {
            echo "✅ Pipeline completed successfully!"
            echo "🎉 Code analysis completed - review results in SonarQube"
        }
        unstable {
            echo "⚠️  Pipeline completed with quality issues"
            echo "🔍 Review failed quality gate conditions in SonarQube"
            echo "📋 Address security vulnerabilities identified in analysis"
        }
        failure {
            echo "❌ Pipeline failed!"
            echo "🛠️  Check build logs for error details"
        }
    }
}
