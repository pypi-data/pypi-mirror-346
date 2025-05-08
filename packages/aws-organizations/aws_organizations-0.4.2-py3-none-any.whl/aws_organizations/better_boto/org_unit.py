# -*- coding: utf-8 -*-

"""
Organizational unit related boto3 API enhancement.

This module provides helper functions for interacting with AWS Organizations API,
with focus on organizational units, parent-child relationships, and account management.
Includes pagination handling and type-safe iterators.
"""

import typing as T

from .model import (
    Parent,
    Child,
    OrganizationalUnit,
    Account,
    ParentIterproxy,
    ChildIterproxy,
    OrganizationUnitIterproxy,
    AccountIterproxy,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from boto_session_manager import BotoSesManager


def _list_parents(
    bsm: "BotoSesManager",
    child_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[Parent]:
    paginator = bsm.organizations_client.get_paginator("list_parents")
    for response in paginator.paginate(
        ChildId=child_id,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("Parents", []):
            yield Parent(
                id=dct["Id"],
                type=dct["Type"],
            )


def list_parents(
    bsm: "BotoSesManager",
    child_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> ParentIterproxy:
    """
    List all parents of a child entity with pagination support.
    """
    return ParentIterproxy(
        _list_parents(
            bsm=bsm,
            child_id=child_id,
            page_size=page_size,
            max_results=max_results,
        )
    )


def _list_children(
    bsm: "BotoSesManager",
    parent_id: str,
    child_type: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[Child]:
    paginator = bsm.organizations_client.get_paginator("list_children")
    for response in paginator.paginate(
        ParentId=parent_id,
        ChildType=child_type,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("Children", []):
            yield Child(
                id=dct["Id"],
                type=dct["Type"],
            )


def list_children(
    bsm: "BotoSesManager",
    parent_id: str,
    child_type: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> ChildIterproxy:
    """
    List all children of a parent entity with pagination support.
    """
    return ChildIterproxy(
        _list_children(
            bsm=bsm,
            parent_id=parent_id,
            child_type=child_type,
            page_size=page_size,
            max_results=max_results,
        )
    )


def get_root_id(
    bsm: "BotoSesManager",
    aws_account_id: str,
) -> str:
    """
    Recursively going up to find the AWS Organizations root id.

    :param bsm: Boto session manager instance
    :param aws_account_id: AWS account ID to start traversal from

    :return: Root organization ID
    """
    for parent in list_parents(bsm=bsm, child_id=aws_account_id):
        if parent.is_root():
            return parent.id
    raise ValueError("Could not find root id")


def _list_organizational_units_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[OrganizationalUnit]:
    paginator = bsm.organizations_client.get_paginator(
        "list_organizational_units_for_parent"
    )
    for response in paginator.paginate(
        ParentId=parent_id,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("OrganizationalUnits", []):
            yield OrganizationalUnit(
                id=dct["Id"],
                arn=dct["Arn"],
                name=dct["Name"],
            )


def list_organizational_units_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> OrganizationUnitIterproxy:
    """
    List all organizational units under a parent with pagination support.
    """
    return OrganizationUnitIterproxy(
        _list_organizational_units_for_parent(
            bsm=bsm,
            parent_id=parent_id,
            page_size=page_size,
            max_results=max_results,
        )
    )


def _list_accounts_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[Account]:
    paginator = bsm.organizations_client.get_paginator("list_accounts_for_parent")
    for response in paginator.paginate(
        ParentId=parent_id,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("Accounts", []):
            yield Account(
                id=dct["Id"],
                arn=dct["Arn"],
                name=dct["Name"],
                email=dct["Email"],
                status=dct["Status"],
                joined_method=dct["JoinedMethod"],
                joined_timestamp=dct["JoinedTimestamp"],
            )


def list_accounts_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> AccountIterproxy:
    """
    List all accounts under a parent with pagination support.
    """
    return AccountIterproxy(
        _list_accounts_for_parent(
            bsm=bsm,
            parent_id=parent_id,
            page_size=page_size,
            max_results=max_results,
        )
    )
