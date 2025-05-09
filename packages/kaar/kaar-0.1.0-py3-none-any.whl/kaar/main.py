import subprocess
import boto3
import json
import time
import yaml
import tempfile
import os
import argparse
from datetime import datetime
import datetime as dt
from kaar.config import load_config
from kaar.utils import setup_logging

def run_k8sgpt(config):
    """Run k8sgpt analyze and capture output."""
    logger = config['logger']
    try:
        result = subprocess.run(['which', 'k8sgpt'], capture_output=True, text=True, check=True)
        logger.info(f"k8sgpt found at: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        logger.error("k8sgpt binary not found in PATH.")
        return "Error: k8sgpt binary not found in PATH."

    try:
        result = subprocess.run(['kubectl', 'get', 'nodes'], capture_output=True, text=True, check=True)
        logger.info(f"Kubernetes cluster accessible: {result.stdout}")
    except subprocess.CalledProcessError as e:
        error_msg = f"Error accessing Kubernetes cluster: {e.stderr}"
        logger.error(error_msg)
        return error_msg

    k8sgpt_cmd = ['k8sgpt', 'analyze', '--backend', config['k8sgpt']['backend']]
    if config['k8sgpt']['explain']:
        k8sgpt_cmd.append('--explain')

    try:
        result = subprocess.run(
            k8sgpt_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("k8sgpt executed successfully.")
        logger.info(f"Raw k8sgpt output:\n{result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"Error running k8sgpt: {e.stderr}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error running k8sgpt: {str(e)}"
        logger.error(error_msg)
        return error_msg

def parse_k8sgpt_output(output, config):
    """Parse k8sgpt output for issues."""
    logger = config['logger']
    if "Error running k8sgpt" in output:
        logger.error("Skipping parsing due to k8sgpt execution error.")
        return []

    issues = []
    lines = output.split('\n')
    current_issue = None
    in_solution = False

    logger.info("Parsing k8sgpt output line by line:")
    for line in lines:
        line = line.strip()
        logger.info(f"Line: '{line}'")
        if not line or line.startswith('(') or line.startswith('AI Provider'):
            logger.info("Skipping line (empty, starts with '(', or 'AI Provider')")
            continue
        if line[0].isdigit() and len(line) > 1 and line[1] == ':':
            if current_issue:
                logger.info(f"Appending issue: {json.dumps(current_issue, indent=2)}")
                issues.append(current_issue)
            issue_number = int(line.split(':')[0])
            current_issue = {
                'number': issue_number,
                'issue': line,
                'error_details': ''
            }
            in_solution = False
            logger.info(f"New issue detected: {current_issue['issue']}")
            continue
        if line.startswith('100%'):
            logger.info("Skipping progress line ('100%')")
            continue
        if line.startswith('- Error:') and current_issue:
            if current_issue['error_details']:
                current_issue['error_details'] += '\n'
            current_issue['error_details'] += line.replace('- Error:', '').strip()
            in_solution = False
            logger.info(f"Added error details: {current_issue['error_details']}")
            continue
        if line.startswith('- ') and current_issue and not in_solution:
            if 'details' not in current_issue:
                current_issue['details'] = ''
            current_issue['details'] = current_issue.get('details', '') + line[2:] + '\n'
            logger.info(f"Added details: {current_issue['details']}")
            continue
        if line.startswith('Error:') and current_issue:
            current_issue['error_explanation'] = line.replace('Error:', '').strip()
            in_solution = False
            logger.info(f"Added error explanation: {current_issue['error_explanation']}")
            continue
        if line.startswith('Solution:') and current_issue:
            current_issue['solution'] = ''
            in_solution = True
            logger.info("Starting solution section")
            continue
        if in_solution and current_issue:
            if line.startswith(tuple(f"{i}." for i in range(1, 10))) or line == '':
                if line:
                    current_issue['solution'] += line + '\n'
                    logger.info(f"Added solution line: {line}")
            else:
                in_solution = False
                logger.info("Ended solution section")

    if current_issue:
        logger.info(f"Appending final issue: {json.dumps(current_issue, indent=2)}")
        issues.append(current_issue)

    logger.info(f"Parsed issues: {json.dumps(issues, indent=2)}")
    return issues

def get_pod_events(namespace, pod_name, config):
    """Get pod events for debugging."""
    logger = config['logger']
    try:
        result = subprocess.run(
            f"kubectl describe pod {pod_name} -n {namespace}",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get events for pod {pod_name} in {namespace}: {e.stderr}")
        return f"Error: {e.stderr}"

def get_container_name(namespace, pod_name, config):
    """Get container name from pod."""
    logger = config['logger']
    try:
        result = subprocess.run(
            f"kubectl get pod {pod_name} -n {namespace} -o jsonpath={{.spec.containers[0].name}}",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        container_name = result.stdout.strip()
        logger.info(f"Container name for pod {pod_name} in {namespace}: {container_name}")
        return container_name
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get container name for pod {pod_name} in {namespace}: {e.stderr}")
        return pod_name  # Fallback to pod name

def remediate_pod_yaml(namespace, pod_name, container_name, issue_type, config):
    """Remediate pod by exporting YAML, modifying it, deleting, and recreating."""
    logger = config['logger']
    try:
        # Step 1: Export the pod's YAML
        export_cmd = f"kubectl get pod {pod_name} -n {namespace} -o yaml"
        export_result = subprocess.run(export_cmd, shell=True, capture_output=True, text=True, check=True)
        pod_yaml = yaml.safe_load(export_result.stdout)
        logger.info(f"Exported YAML for pod {pod_name} in namespace {namespace}")

        # Step 2: Modify the YAML based on the issue
        modified = False
        for container in pod_yaml['spec']['containers']:
            if container['name'] == container_name:
                if issue_type == 'OOMKilled':
                    # Update memory limit to 768Mi to accommodate 600MB workload
                    if 'resources' not in container:
                        container['resources'] = {}
                    if 'limits' not in container['resources']:
                        container['resources']['limits'] = {}
                    container['resources']['limits']['memory'] = '768Mi'
                    logger.info(f"Updated memory limit to 768Mi for container {container_name} in pod {pod_name}")
                    modified = True
                elif issue_type == 'CrashLoopBackOff':
                    # Fix the command (remove invalid command, use default nginx command)
                    if 'command' in container and container['command'] == ['invalid-command']:
                        container['command'] = ['nginx', '-g', 'daemon off;']
                        logger.info(f"Fixed command for container {container_name} in pod {pod_name} to use default nginx command")
                        modified = True
                break

        if not modified:
            logger.warning(f"No modifications applied to pod {pod_name} for issue {issue_type}")
            return {"command": "No changes applied", "output": "No modifications needed", "status": "skipped"}

        # Step 3: Save the modified YAML to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as temp_file:
            yaml.dump(pod_yaml, temp_file)
            temp_file_path = temp_file.name
        logger.info(f"Saved modified YAML to temporary file: {temp_file_path}")

        # Step 4: Delete the pod
        delete_cmd = f"kubectl delete pod {pod_name} -n {namespace}"
        subprocess.run(delete_cmd, shell=True, capture_output=True, text=True, check=True)
        logger.info(f"Deleted pod {pod_name} in namespace {namespace}")

        # Step 5: Recreate the pod with the modified YAML
        apply_cmd = f"kubectl apply -f {temp_file_path}"
        apply_result = subprocess.run(apply_cmd, shell=True, capture_output=True, text=True, check=True)
        logger.info(f"Recreated pod {pod_name} with updated YAML")

        # Clean up the temporary file
        os.remove(temp_file_path)
        logger.info(f"Cleaned up temporary file: {temp_file_path}")

        return {
            "command": "Pod YAML updated, deleted, and recreated",
            "output": apply_result.stdout,
            "status": "success"
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to remediate pod {pod_name}: {e.stderr}")
        return {"command": "Failed to remediate", "output": e.stderr, "status": "failed"}
    except Exception as e:
        logger.error(f"Unexpected error during pod remediation: {str(e)}")
        return {"command": "Failed to remediate", "output": str(e), "status": "failed"}

def generate_remediation_command(issue, config):
    """Use Bedrock to identify the issue and suggest a remediation strategy."""
    logger = config['logger']
    bedrock_client = config['bedrock_client']

    if 'ConfigMap' in issue.get('issue', ''):
        logger.info(f"Skipping remediation for ConfigMap: {issue['issue']}")
        return {"command": "No remediation command available", "output": "ConfigMap remediation skipped", "status": "skipped"}

    issue_text = issue.get('issue', '')
    error_details = issue.get('error_details', '')
    logger.info(f"Processing issue: {issue_text}, Error Details: {error_details}")

    # Extract pod info
    is_pod = 'Pod' in issue_text
    namespace = None
    name = None
    container_name = None
    if is_pod:
        resource_name = issue_text.split('Pod ')[1].strip().split('(')[0].strip()
        namespace = resource_name.split('/')[0] if '/' in resource_name else 'default'
        name = resource_name.split('/')[-1]
        container_name = get_container_name(namespace, name, config)
        pod_events = get_pod_events(namespace, name, config)
        logger.info(f"Pod {name} events:\n{pod_events}")
    else:
        logger.warning(f"Resource type not recognized as Pod: {issue_text}")
        return {"command": "No remediation command available", "output": "Resource not a pod", "status": "skipped"}

    # Bedrock remediation using Legacy API (invoke_model)
    prompt = f"""
\n\nHuman: You are a Kubernetes expert. Analyze the following K8sGPT issue for a pod and identify the issue type. The pod is in namespace '{namespace}'.

Issue: {issue_text}
Error Details: {error_details}
Container Name: {container_name}

Identify the issue type based on the following guidelines:
- If the issue involves 'ImagePullBackOff' or 'ErrImagePull', return 'ImagePullBackOff'.
- If the issue involves 'CrashLoopBackOff' or 'ContainerCannotRun' (including errors like 'executable file not found in $PATH'), return 'CrashLoopBackOff'.
- If the issue is 'OOMKilled', return 'OOMKilled'.
- If the issue is 'Pending' due to a scheduling failure (e.g., 'Unschedulable'), return 'Pending'.
- For any other issue, return 'Unknown'.
- If no remediation is possible, return 'No remediation possible'.

Provide only the issue type as a string. Do not include explanations, additional text, or backticks.
\n\nAssistant: """
    try:
        request_body = {
            "prompt": prompt,
            "max_tokens_to_sample": config['bedrock']['max_tokens'],
            "temperature": config['bedrock']['temperature']
        }
        logger.info(f"Bedrock Legacy API request: {json.dumps(request_body, indent=2)}")
        response = bedrock_client.invoke_model(
            modelId=config['bedrock']['model'],
            body=json.dumps(request_body)
        )
        response_body = json.loads(response['body'].read().decode('utf-8'))
        issue_type = response_body['completion'].strip()
        logger.info(f"Bedrock identified issue type: {issue_type}")

        # Prepare remediation based on issue type
        remediation = {
            "issue_type": issue_type,
            "namespace": namespace,
            "pod_name": name,
            "container_name": container_name,
            "command": "",
            "output": "",
            "status": "pending"
        }
        return remediation
    except Exception as e:
        logger.error(f"Bedrock invocation failed: {str(e)}")
        return {"command": "No remediation command available", "output": f"Bedrock error: {str(e)}", "status": "failed"}

def remediate_issue(remediation, config):
    """Execute remediation."""
    logger = config['logger']
    if remediation.get("command") == "No remediation command available":
        return remediation

    issue_type = remediation.get("issue_type", "Unknown")
    namespace = remediation.get("namespace")
    pod_name = remediation.get("pod_name")
    container_name = remediation.get("container_name")

    # Handle specific issues that require YAML modification
    if issue_type in ['OOMKilled', 'CrashLoopBackOff'] or 'executable file not found' in issue_type.lower():
        if 'executable file not found' in issue_type.lower():
            issue_type = 'CrashLoopBackOff'
            logger.info(f"Fallback: Treating issue type '{issue_type}' as 'CrashLoopBackOff'")
        return remediate_pod_yaml(namespace, pod_name, container_name, issue_type, config)

    # Handle other issues with a single kubectl command
    if issue_type == 'ImagePullBackOff':
        command = f"kubectl set image pod/{pod_name} {container_name}=nginx:latest -n {namespace}"
    elif issue_type == 'Pending':
        command = f"kubectl patch pod {pod_name} -n {namespace} -p '{{\"spec\":{{\"affinity\":{{\"nodeAffinity\":{{\"preferredDuringSchedulingIgnoredDuringExecution\":[{{\"weight\":1,\"preference\":{{\"matchExpressions\":[{{\"key\":\"kubernetes.io/hostname\",\"operator\":\"Exists\"}}]}}}}]}}}}}}}}'"
    else:
        logger.warning(f"No remediation strategy for issue type: {issue_type}")
        return {"command": "No remediation command available", "output": "Unknown issue type", "status": "skipped"}

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        logger.info(f"Remediation command executed: {command}")
        remediation['command'] = command
        remediation['output'] = result.stdout
        remediation['status'] = "success"
    except subprocess.CalledProcessError as e:
        logger.error(f"Remediation failed: {e.stderr}")
        remediation['command'] = command
        remediation['output'] = e.stderr
        remediation['status'] = "failed"
    return remediation

def verify_status(issue, config):
    """Verify pod status with detailed state checking."""
    logger = config['logger']
    max_attempts = config['remediation']['max_attempts']
    retry_interval = config['remediation']['retry_interval_seconds']

    is_pod = 'Pod' in issue.get('issue', '')
    if not is_pod:
        logger.info(f"Skipping verification for ConfigMap: {issue['issue']}")
        return {"name": issue['issue'].split('/')[-1], "namespace": issue['issue'].split('/')[0] if '/' in issue['issue'] else 'default', "status": "Skipped", "verified": False}

    issue_text = issue.get('issue', '')
    resource_name = issue_text.split('Pod ')[1].strip().split('(')[0].strip()
    namespace = resource_name.split('/')[0] if '/' in resource_name else 'default'
    name = resource_name.split('/')[-1]

    # Check if the pod exists
    try:
        result = subprocess.run(f"kubectl get pod {name} -n {namespace} --no-headers", shell=True, capture_output=True, text=True)
        if "NotFound" in result.stderr:
            logger.info(f"Pod {name} does not exist after remediation (likely deleted)")
            return {"name": name, "namespace": namespace, "status": "Deleted", "verified": False}
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check existence of pod {name}: {e.stderr}")
        return {"name": name, "namespace": namespace, "status": "Unknown", "verified": False}

    attempt = 1
    detailed_status = "Unknown"
    while attempt <= max_attempts:
        try:
            # Get pod phase
            phase_command = f"kubectl get pod {name} -n {namespace} -o jsonpath={{.status.phase}}"
            phase_result = subprocess.run(phase_command, shell=True, capture_output=True, text=True, check=True)
            phase = phase_result.stdout.strip()

            # Get detailed container status
            status_command = f"kubectl get pod {name} -n {namespace} -o json"
            status_result = subprocess.run(status_command, shell=True, capture_output=True, text=True, check=True)
            pod_info = json.loads(status_result.stdout)
            container_statuses = pod_info.get('status', {}).get('containerStatuses', [])
            detailed_status = phase
            for container in container_statuses:
                # Check waiting state
                waiting = container.get('state', {}).get('waiting', {})
                if waiting and waiting.get('reason') in ['ImagePullBackOff', 'ErrImagePull', 'CrashLoopBackOff']:
                    detailed_status = waiting.get('reason')
                    break
                # Check terminated state (e.g., OOMKilled)
                terminated = container.get('lastState', {}).get('terminated', {})
                if terminated and terminated.get('reason') == 'OOMKilled':
                    detailed_status = 'OOMKilled'
                    break

            logger.info(f"Pod {name} status (attempt {attempt}/{max_attempts}): {detailed_status}")
            if detailed_status == "Running":
                # Double-check that all containers are ready
                all_ready = all(cs.get('ready', False) for cs in container_statuses)
                if all_ready:
                    return {"name": name, "namespace": namespace, "status": detailed_status, "verified": True}
                else:
                    detailed_status = "NotReady"
            if detailed_status in ["Failed", "Unknown", "ImagePullBackOff", "ErrImagePull", "CrashLoopBackOff", "OOMKilled"]:
                return {"name": name, "namespace": namespace, "status": detailed_status, "verified": False}
            time.sleep(retry_interval)  # Wait before retrying
            attempt += 1
        except subprocess.CalledProcessError as e:
            logger.error(f"Verification failed for {name}: {e.stderr}")
            return {"name": name, "namespace": namespace, "status": "Unknown", "verified": False}
    logger.warning(f"Pod {name} did not reach Running state after {max_attempts} attempts. Final status: {detailed_status}")
    return {"name": name, "namespace": namespace, "status": detailed_status, "verified": False}

def send_sns_notification(issues, remediation_results, config):
    """Send notification via SNS."""
    logger = config['logger']
    sns_client = config['sns_client']
    logs_client = config['logs_client']
    log_group = config['aws']['log_group']
    log_stream = config['aws']['log_stream']
    sns_topic_arn = config['aws']['sns_topic_arn']

    if not issues:
        message = "KAAR Analysis: No issues found."
        logger.info(message)
    else:
        message = "KAAR Analysis - Kubernetes Cluster Issues Detected and Remediated:\n\n"
        for issue, result in zip(issues, remediation_results):
            message += f"Issue #{issue['number']}: {issue['issue']}\n"
            if 'error_details' in issue and issue['error_details']:
                message += f"Error Details: {issue['error_details']}\n"
            if 'details' in issue:
                message += f"Additional Details: {issue['details']}\n"
            if 'error_explanation' in issue:
                message += f"Error Explanation: {issue['error_explanation']}\n"
            if 'solution' in issue:
                message += f"Solution:\n{issue['solution']}\n"
            message += f"Remediation: {result['command']}\n"
            message += f"Remediation Output: {result['output']}\n"
            message += f"Status: {result['status']}\n"
            verification = verify_status(issue, config)
            message += f"Verification: {'Pod' if 'Pod' in issue['issue'] else 'ConfigMap'} {verification['name']} in {verification['namespace']} is {verification['status']}\n"
            message += "------------------------\n"

    # Log to CloudWatch
    logs_client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[
            {
                'timestamp': int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000),
                'message': message
            }
        ]
    )

    # Publish to SNS
    try:
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='KAAR Alert: Kubernetes Cluster Issues Remediated'
        )
        logger.info(f"Notification sent: {response['MessageId']}")
    except Exception as e:
        logger.error(f"Error sending SNS notification: {str(e)}")
        raise

def main():
    """Main function to run KAAR."""
    parser = argparse.ArgumentParser(description="Kubernetes AI-powered Analysis and Remediation (KAAR)")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')
    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return

    # Set up logging and AWS clients
    logger, logs_client = setup_logging(
        config['aws']['log_group'],
        config['aws']['log_stream'],
        config['aws']['region']
    )
    sns_client = boto3.client('sns', region_name=config['aws']['region'])
    bedrock_client = boto3.client('bedrock-runtime', region_name=config['aws']['region'])

    # Add clients and logger to config for easy access
    config['logger'] = logger
    config['sns_client'] = sns_client
    config['logs_client'] = logs_client
    config['bedrock_client'] = bedrock_client

    # Run the analysis and remediation flow
    output = run_k8sgpt(config)
    logger.info("k8sgpt Output:\n%s", output)

    issues = parse_k8sgpt_output(output, config)
    logger.info(f"Found {len(issues)} issues")

    remediation_results = []
    for issue in issues:
        remediation = generate_remediation_command(issue, config)
        remediation = remediate_issue(remediation, config)
        remediation_results.append(remediation)

    send_sns_notification(issues, remediation_results, config)

if __name__ == "__main__":
    main()
