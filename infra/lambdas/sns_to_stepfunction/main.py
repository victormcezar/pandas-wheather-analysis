import os
import uuid
import json
import logging
import boto3

STATE_MACHINE_ARN = os.getenv("STATE_MACHINE_ARN")


def handler(event, context):
    setup_logging()
    logging.info(f"Starting State Machine: {STATE_MACHINE_ARN}")
    client = boto3.client('stepfunctions')
    for record in event['Records']:
        client.start_execution(stateMachineArn=STATE_MACHINE_ARN,
                               name=str(uuid.uuid4()),
                               input=json.dumps(record))


def setup_logging():
    root = logging.getLogger()
    if root.handlers:
        for h in root.handlers:
            root.removeHandler(h)
    logging.basicConfig(
        format='[%(asctime)s][%(name)s][%(funcName)s] %(message)s',
        level='INFO')
