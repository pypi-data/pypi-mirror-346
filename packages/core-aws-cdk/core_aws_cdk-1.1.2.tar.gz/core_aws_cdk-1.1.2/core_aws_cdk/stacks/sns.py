# -*- coding: utf-8 -*-

from typing import Optional

from aws_cdk.aws_sns import Topic

from core_aws_cdk.stacks.base import BaseStack


class BaseSnsStack(BaseStack):
    """ It contains the base elements to create SNS infrastructure on AWS """

    def create_sns_topic(
            self, topic_id: str, topic_name: Optional[str] = None,
            display_name: Optional[str] = None, fifo: Optional[bool] = None,
            content_based_deduplication: Optional[bool] = None,
            **kwargs) -> Topic:

        """
        It creates a new SNS topic...
        https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        """

        return Topic(
            self, topic_id, topic_name=topic_name,
            content_based_deduplication=content_based_deduplication,
            display_name=display_name,
            fifo=fifo, **kwargs)
