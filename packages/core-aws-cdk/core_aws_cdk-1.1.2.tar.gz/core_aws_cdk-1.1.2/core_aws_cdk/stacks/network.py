# -*- coding: utf-8 -*-

from typing import Optional, List

from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2


class NetworkStack(Stack):
    """ It contains elements related to networks """

    def create_vpc(
            self, vpc_id: str, availability_zones: List[str] = None, cidr: Optional[str] = None,
            subnet_configuration: Optional = None, max_azs: Optional[int] = None,
            **kwargs) -> ec2.Vpc:

        """
        Define an AWS Virtual Private Cloud...
        https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ec2/Vpc.html
        """

        return ec2.Vpc(
            self, vpc_id,
            cidr=cidr,
            availability_zones=availability_zones,
            subnet_configuration=subnet_configuration,
            max_azs=max_azs,
            **kwargs)
