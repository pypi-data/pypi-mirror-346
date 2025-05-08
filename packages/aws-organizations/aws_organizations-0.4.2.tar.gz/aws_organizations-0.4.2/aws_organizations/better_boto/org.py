# -*- coding: utf-8 -*-

"""
Organization related boto3 API enhancement.
"""

import typing as T

from .model import (
    Organization,
)

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager


def describe_organization(
    bsm: "BotoSesManager",
) -> Organization:
    """
    Get the details of the organization.
    """
    response = bsm.organizations_client.describe_organization()
    return Organization(
        id=response["Organization"]["Id"],
        arn=response["Organization"]["Arn"],
        feature_set=response["Organization"]["FeatureSet"],
        master_account_arn=response["Organization"]["MasterAccountArn"],
        master_account_id=response["Organization"]["MasterAccountId"],
        master_account_email=response["Organization"]["MasterAccountEmail"],
        available_policy_types=response["Organization"]["AvailablePolicyTypes"],
    )
