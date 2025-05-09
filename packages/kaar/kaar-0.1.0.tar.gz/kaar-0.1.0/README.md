Kubernetes AI-powered Analysis and Remediation (KAAR)
KAAR is a tool that automates the monitoring, analysis, and remediation of Kubernetes cluster issues using Amazon Bedrock and K8sGPT. It identifies problems in your cluster, suggests fixes powered by AI, applies the remediation, verifies the results, and notifies you via AWS SNS.
Features

Automated Monitoring: Uses K8sGPT to analyze Kubernetes clusters.
AI-Powered Remediation: Leverages Amazon Bedrock to identify issue types and suggest fixes.
Actionable Fixes: Automatically applies remediation strategies (e.g., adjusting memory limits, fixing pod commands).
Verification: Ensures the fixes work by checking pod status.
Notifications: Sends results via AWS SNS and logs to CloudWatch.

Prerequisites

An AWS account with access to Amazon Bedrock, SNS, and CloudWatch Logs.
A Kubernetes cluster (e.g., EKS, Minikube).
K8sGPT installed and configured to use Amazon Bedrock (k8sgpt auth set-default amazonbedrock).
AWS credentials configured with permissions for:
bedrock:InvokeModel
sns:Publish
logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents



Installation

Install KAAR via pip:pip install kaar


Copy the default config.yaml file to your working directory:cp $(python -c "import kaar; print(kaar.__path__[0])")/../config.yaml .


Edit config.yaml with your AWS details (e.g., SNS Topic ARN, region).

Usage
Run KAAR with the default configuration:
kaar --config config.yaml

Configuration
Edit config.yaml to customize KAAR:

aws.region: AWS region (e.g., us-east-1).
aws.sns_topic_arn: Your SNS Topic ARN.
aws.log_group and aws.log_stream: CloudWatch Logs settings.
bedrock.model: Bedrock model to use (e.g., anthropic.claude-v2:1).
k8sgpt.backend: AI backend for K8sGPT (e.g., amazonbedrock).

Example

Create a pod with an issue (e.g., OOMKilled):kubectl run oom-pod --image=nginx --requests='memory=50Mi' --limits='memory=100Mi' -- /bin/sh -c "while true; do echo consuming memory; done"


Run KAAR:kaar --config config.yaml


Check the SNS notification or CloudWatch Logs for the remediation report.

Contributing
Contributions are welcome! Please see CONTRIBUTING.md for details.
License
This project is licensed under the MIT License - see the LICENSE file for details.

