# -*- coding: utf-8 -*-

from aws_organizations import api


def test():
    _ = api
    _ = api.ParentTypeEnum
    _ = api.Parent
    _ = api.ChildTypeEnum
    _ = api.Child
    _ = api.AccountStatusEnum
    _ = api.AccountJoinedMethodEnum
    _ = api.Account
    _ = api.OrganizationalUnit
    _ = api.Organization
    _ = api.ParentIterproxy
    _ = api.ChildIterproxy
    _ = api.AccountIterproxy
    _ = api.OrganizationUnitIterproxy
    _ = api.list_parents
    _ = api.list_children
    _ = api.get_root_id
    _ = api.list_organizational_units_for_parent
    _ = api.list_accounts_for_parent
    _ = api.describe_organization
    _ = api.ROOT_NODE_NAME
    _ = api.NodeTypeEnum
    _ = api.Node
    _ = api.OrgStructure


if __name__ == "__main__":
    from aws_organizations.tests import run_cov_test

    run_cov_test(__file__, "aws_organizations.api", preview=False)
