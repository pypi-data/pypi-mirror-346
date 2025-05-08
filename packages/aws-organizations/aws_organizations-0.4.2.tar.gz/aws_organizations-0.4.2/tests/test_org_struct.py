# -*- coding: utf-8 -*-

import os
import pytest
from boto_session_manager import BotoSesManager
from aws_organizations.better_boto.api import (
    ParentTypeEnum,
    Parent,
    ChildTypeEnum,
    Child,
    AccountStatusEnum,
    AccountJoinedMethodEnum,
    Account,
    OrganizationalUnit,
    Organization,
    ParentIterproxy,
    ChildIterproxy,
    AccountIterproxy,
    OrganizationUnitIterproxy,
    list_parents,
    list_children,
    get_root_id,
    list_organizational_units_for_parent,
    list_accounts_for_parent,
    describe_organization,
)
from aws_organizations.org_struct import (
    ROOT_NODE_NAME,
    NodeTypeEnum,
    OrgStructure,
)
from rich import print as rprint

IS_CI = "CI" in os.environ


def _run_test_case(org_struct: OrgStructure):
    # --------------------------------------------------------------------------
    # Root node
    # --------------------------------------------------------------------------
    root = org_struct.root
    assert (
        root.id == root.obj.id
    )  # root.id is the root_id, root.obj.id is the organization id
    assert root.name == ROOT_NODE_NAME
    assert root.type == NodeTypeEnum.ROOT.value

    assert org_struct.root_id == root.obj.root_id
    assert root.is_root is True
    assert root.obj.is_org() is True

    # --------------------------------------------------------------------------
    # Iterate account, ou
    # --------------------------------------------------------------------------
    # root account
    assert len(root.accounts) == 1
    assert root.accounts[0].name == "esc-admin"

    assert len(root.all_accounts) == 8
    assert len(root.all_org_units) == 4

    assert len(root.accounts) == len(root.accounts_names)
    assert len(root.org_units) == len(root.org_units_names)
    assert len(root.all_accounts) == len(root.all_accounts_names)
    assert len(root.all_org_units) == len(root.all_org_units_names)

    # App ou
    ou_app = org_struct.get_node_by_name("app")
    assert len(ou_app.accounts) == 5
    assert len(ou_app.org_units) == 0
    assert len(ou_app.all_accounts) == 5
    assert len(ou_app.all_org_units) == 0

    # --------------------------------------------------------------------------
    # is X in Y
    # --------------------------------------------------------------------------
    root_id = org_struct.root_id
    root_node = org_struct.get_node_by_id(root_id)
    org = root_node.obj

    for y in [root_id, root_node, org]:
        for x_node in [
            org_struct.get_node_by_name("app"),
            org_struct.get_node_by_name("esc-app-devops"),
        ]:
            assert org_struct.is_x_in_y(x_node, y) is True
            assert org_struct.is_x_in_y(x_node.id, y) is True
            assert org_struct.is_x_in_y(x_node.obj, y) is True

    assert (
        org_struct.is_x_in_y(
            org_struct.get_node_by_name("app"),
            org_struct.get_node_by_name("esc-infra"),
        )
        is False
    )


def _run_visualize(org_struct: OrgStructure):
    org_struct.visualize()
    org_struct.to_csv()
    # print(org_struct.visualize())
    # print(org_struct.to_csv())


def _run_better_boto(org_struct: OrgStructure, bsm: BotoSesManager):
    # --------------------------------------------------------------------------
    # list_children
    # --------------------------------------------------------------------------
    res = list_children(
        bsm=bsm,
        parent_id=org_struct.root_id,
        child_type=ChildTypeEnum.ORGANIZATIONAL_UNIT.value,
    ).all()
    assert len(res) == 4

    for child in res:
        res_ = list_children(
            bsm=bsm,
            parent_id=child.id,
            child_type=ChildTypeEnum.ACCOUNT.value,
        ).all()
        rprint(f"children of {child}:")
        rprint(res_)

    # --------------------------------------------------------------------------
    # list_organizational_units_for_parent
    # --------------------------------------------------------------------------
    res = list_organizational_units_for_parent(
        bsm=bsm,
        parent_id=org_struct.root_id,
    ).all()
    print(f"------ organization units in {org_struct.root_id!r}")
    rprint(res)

    # ------------------------------------------------------------------------------
    # list_accounts_for_parent
    # ------------------------------------------------------------------------------
    res = list_accounts_for_parent(
        bsm=bsm,
        parent_id=org_struct.root_id,
    ).all()
    print(f"------ accounts in {org_struct.root_id!r}")
    rprint(res)


@pytest.mark.skipif(IS_CI, reason="This test is not meant to run in CI")
def test():
    print("")
    bsm = BotoSesManager(profile_name="esc_admin_us_east_1")
    org_struct = OrgStructure.get_org_structure(bsm=bsm)
    _run_test_case(org_struct)
    _run_visualize(org_struct)
    _run_better_boto(org_struct, bsm)

    org_struct_data = org_struct.serialize()
    org_struct_parsed = OrgStructure.deserialize(org_struct_data)
    _run_test_case(org_struct_parsed)


if __name__ == "__main__":
    from aws_organizations.tests import run_cov_test

    run_cov_test(__file__, "aws_organizations.org_struct", preview=False)
