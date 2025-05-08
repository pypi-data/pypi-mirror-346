.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.4.2 (2025-05-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Removed not used dependency ``func_args``.


0.4.1 (2024-11-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Changes**

- Rework the API and documentation.
- Now the public APIs are:
    - ``aws_organizations.api.ParentTypeEnum``
    - ``aws_organizations.api.Parent``
    - ``aws_organizations.api.ChildTypeEnum``
    - ``aws_organizations.api.Child``
    - ``aws_organizations.api.AccountStatusEnum``
    - ``aws_organizations.api.AccountJoinedMethodEnum``
    - ``aws_organizations.api.Account``
    - ``aws_organizations.api.OrganizationalUnit``
    - ``aws_organizations.api.Organization``
    - ``aws_organizations.api.ParentIterproxy``
    - ``aws_organizations.api.ChildIterproxy``
    - ``aws_organizations.api.AccountIterproxy``
    - ``aws_organizations.api.OrganizationUnitIterproxy``
    - ``aws_organizations.api.list_parents``
    - ``aws_organizations.api.list_children``
    - ``aws_organizations.api.get_root_id``
    - ``aws_organizations.api.list_organizational_units_for_parent``
    - ``aws_organizations.api.list_accounts_for_parent``
    - ``aws_organizations.api.describe_organization``
    - ``aws_organizations.api.ROOT_NODE_NAME``
    - ``aws_organizations.api.NodeTypeEnum``
    - ``aws_organizations.api.Node``
    - ``aws_organizations.api.OrgStructure``

**Features and Improvements**

- Add support to dump organization structure to mermaid format.


0.3.1 (2023-03-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``OrgStructure.serialize`` and ``OrgStructure.deserialize``. now you can cache the org structure data in JSON.
- add ``OrgStructure.get_node_by_id``
- add ``OrgStructure.get_node_by_name``
- add ``Node.organization_or_account_or_organizational_unit``.
- add ``Node.parent_id``.
- add ``Node.accounts``.
- add ``Node.org_units``.
- add ``Node.all_accounts``.
- add ``Node.all_org_units``.
- add ``Node.accounts_names``.
- add ``Node.org_units_names``.
- add ``Node.all_accounts_names``.
- add ``Node.all_org_units_names``.


0.2.1 (2023-03-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``Node.iter_org_units`` and ``Node_iter_accounts`` methods.
- add ``OrgStructure`` class to represent the organization structure tree.
- drop ``get_org_structure``, add ``OrgStructure.get_org_structure`` method.
- add ``OrgStructure.visualize`` method.
- add ``OrgStructure.to_csv`` method.
- add ``OrgStructure.is_x_in_y`` method.


0.1.1 (2023-03-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- add data model for ``Organization``, ``OrganizationUnit``, ``Account``
- add ``get_org_structure`` method to get the organization structure tree.
