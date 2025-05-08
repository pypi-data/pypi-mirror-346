# -*- coding: utf-8 -*-

"""
AWS Organizations data model definitions.

This module provides dataclass-based models representing AWS Organizations
core entities like Organization, OrganizationalUnit, and Account. It includes
enums for valid types and statuses, as well as proxy classes for iteration.
"""

import typing as T
import enum
import dataclasses
from datetime import datetime

from iterproxy import IterProxy


@dataclasses.dataclass
class BaseModel:
    """
    Base model providing dict serialization/deserialization.
    """

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class ParentTypeEnum(str, enum.Enum):
    """
    Valid parent types in AWS Organizations.
    """

    ROOT = "ROOT"
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT"


@dataclasses.dataclass
class Parent(BaseModel):
    """
    Represents a parent entity in AWS Organizations.
    """

    id: str = dataclasses.field()
    type: str = dataclasses.field()

    def is_root(self) -> bool:  # pragma: no cover
        """
        Check if this parent entity is a root.
        """
        return self.type == ParentTypeEnum.ROOT.value

    def is_ou(self) -> bool:  # pragma: no cover
        """
        Check if this parent entity is an organizational unit.
        """
        return self.type == ParentTypeEnum.ORGANIZATIONAL_UNIT.value


class ChildTypeEnum(str, enum.Enum):
    """
    Valid child types in AWS Organizations.
    """

    ACCOUNT = "ACCOUNT"
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT"


@dataclasses.dataclass
class Child(BaseModel):
    """
    Represents a child entity in AWS Organizations.
    """

    id: str = dataclasses.field()
    type: str = dataclasses.field()

    def is_account(self) -> bool:  # pragma: no cover
        """
        Check if this child entity is an account.
        """
        return self.type == ChildTypeEnum.ACCOUNT.value

    def is_ou(self) -> bool:  # pragma: no cover
        """
        Check if this child entity is an organizational unit.
        """
        return self.type == ChildTypeEnum.ORGANIZATIONAL_UNIT.value


class AccountOrOrgUnitOrOrg:
    """
    Mixin class for Account, OrganizationalUnit and Organization.

    Provides type-checking interface across organization entities.
    """

    def is_account(self) -> bool:  # pragma: no cover
        """
        Check if this entity is an account.
        """
        return False

    def is_ou(self) -> bool:  # pragma: no cover
        """
        Check if this entity is an organizational unit.
        """
        return False

    def is_org(self) -> bool:  # pragma: no cover
        """
        Check if this entity is an organization.
        """
        return False


class AccountStatusEnum(str, enum.Enum):
    """
    Valid AWS account statuses.
    """

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING_CLOSURE = "PENDING_CLOSURE"


class AccountJoinedMethodEnum(str, enum.Enum):
    """
    Valid methods for how an account joined the organization.
    """

    INVITED = "INVITED"
    CREATED = "CREATED"


@dataclasses.dataclass
class Account(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    """
    Represents an AWS Account.

    :param id: Account ID (12-digit)
    :param arn: Account ARN
    :param name: Account name use alpha digits and hyphen only, don't use underscore
    :param email: Account email
    :param status: Account status
    :param joined_method: How account joined organization
    :param joined_timestamp: When account joined
    :param root_id: Organization root ID
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    email: T.Optional[str] = dataclasses.field(default=None)
    status: T.Optional[str] = dataclasses.field(default=None)
    joined_method: T.Optional[str] = dataclasses.field(default=None)
    joined_timestamp: T.Optional[datetime] = dataclasses.field(default=None)

    root_id: T.Optional[str] = dataclasses.field(default=None)

    def is_account(self) -> bool:  # pragma: no cover
        """
        Check if this entity is an account.
        """
        return True


@dataclasses.dataclass
class OrganizationalUnit(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    """
    Represents an AWS Organization Unit.

    :param id: OU ID
    :param arn: OU ARN
    :param name: OU name
    :param root_id: Organization root ID
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)

    root_id: T.Optional[str] = dataclasses.field(default=None)

    def is_ou(self) -> bool:  # pragma: no cover
        """
        Check if this entity is an organizational unit.
        """
        return True


@dataclasses.dataclass
class Organization(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    """
    Represents an AWS Organization.

    :param id: Organization ID
    :param arn: Organization ARN
    :param feature_set: Enabled feature set
    :param master_account_arn: Management account ARN
    :param master_account_id: Management account ID
    :param master_account_email: Management account email
    :param available_policy_types: Available policy types
    :param root_id: Organization root ID
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    feature_set: T.Optional[str] = dataclasses.field(default=None)
    master_account_arn: T.Optional[str] = dataclasses.field(default=None)
    master_account_id: T.Optional[str] = dataclasses.field(default=None)
    master_account_email: T.Optional[str] = dataclasses.field(default=None)
    available_policy_types: T.List[dict] = dataclasses.field(default_factory=list)

    root_id: T.Optional[str] = dataclasses.field(default=None)

    def is_org(self) -> bool:  # pragma: no cover
        """
        Check if this entity is an organization.
        """
        return True


# ------------------------------------------------------------------------------
# Iterproxy
# ------------------------------------------------------------------------------
class ParentIterproxy(IterProxy[Parent]):
    """"""

    pass


class ChildIterproxy(IterProxy[Child]):
    """"""

    pass


class AccountIterproxy(IterProxy[Account]):
    """"""

    pass


class OrganizationUnitIterproxy(IterProxy[OrganizationalUnit]):
    """"""

    pass
