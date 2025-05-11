# -*- coding: utf-8 -*-

from typing import Optional

import aws_cdk.aws_sqs as sqs
from aws_cdk import RemovalPolicy, Duration

from core_aws_cdk.stacks.base import BaseStack


class BaseSqsStack(BaseStack):
    """ It contains the base elements to create SQS infrastructure on AWS """

    def create_sqs_queue(
            self, queue_id: str, queue_name: Optional[str],
            receive_message_wait_time: Optional[Duration] = Duration.seconds(20),
            removal_policy: Optional[RemovalPolicy] = RemovalPolicy.DESTROY,
            visibility_timeout: Optional[Duration] = Duration.minutes(5), with_dlq: bool = False,
            dlq_id: str = None, dlq_name: str = None, max_receive_count: Optional[int] = 3,
            **kwargs) -> sqs.Queue:

        """
        It creates a new Amazon SQS queue...
        https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sqs/Queue.html
        """

        dead_letter_queue = None
        if with_dlq:
            dead_letter_queue = sqs.DeadLetterQueue(
                max_receive_count=max_receive_count,
                queue=sqs.Queue(
                    self, id=dlq_id, queue_name=dlq_name,
                    removal_policy=removal_policy)
                )

        return sqs.Queue(
            self, queue_id,
            queue_name=queue_name,
            receive_message_wait_time=receive_message_wait_time,
            visibility_timeout=visibility_timeout,
            dead_letter_queue=dead_letter_queue,
            removal_policy=removal_policy,
            **kwargs)
