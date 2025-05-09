import logging
import boto3

def setup_logging(log_group, log_stream, region):
    """Set up logging to CloudWatch Logs."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('KAAR')
    logger.setLevel(logging.INFO)

    # Initialize CloudWatch Logs client
    logs_client = boto3.client('logs', region_name=region)

    # Ensure CloudWatch Log Group and Stream exist
    try:
        logs_client.create_log_group(logGroupName=log_group)
    except logs_client.exceptions.ResourceAlreadyExistsException:
        pass
    try:
        logs_client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
    except logs_client.exceptions.ResourceAlreadyExistsException:
        pass

    return logger, logs_client
