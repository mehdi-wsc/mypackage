General Tagging Strategy
------------------------

Purpose of tagging
~~~~~~~~~~~~~~~~~~~


Tagging has multiple purposes.

Filtering
^^^^^^^^^

We use tags to filter resources:
- to explore or search resources.
- to select resources for dashboarding, alerting.
- to parameter monitoring systems (retention, log level).

Reporting
^^^^^^^^^

We use tags to report costs, usage on organisational or technical dimensions.

Permission
^^^^^^^^^^

We use tags to help allowing access or operational rights to resources.

Automation
^^^^^^^^^^

We use tags to automate generic actions such as:

- powering on or off servers.
- destroying resources.
- performing backups, updates.

.. _general-tagging-strategy-1:

General Tagging Strategy
~~~~~~~~~~~~~~~~~~~~~~~~

The following tags apply:


+------------------+-----------------+----------+-----------------------+------------------------------------------+-----------------------+-----------------+------------------------------------+
| Tag Name         | Requisiteness   | Format   | Sample values         | Remarks                                  | Cost Allocation tag   | Applicable on   | Purpose                            |
+==================+=================+==========+=======================+==========================================+=======================+=================+====================================+
| owner            | mandatory       | string   | Wescale               | The actual owner of the account          |                       | all resources   | reporting, filtering               |
+------------------+-----------------+----------+-----------------------+------------------------------------------+-----------------------+-----------------+------------------------------------+
| account          | mandatory       | string   | {group}-{env}         | see reference in AWS Naming convention   | Yes                   | all resources   | reporting, filtering, permission   |
+------------------+-----------------+----------+-----------------------+------------------------------------------+-----------------------+-----------------+------------------------------------+
| createdBy        | mandatory       | string   | {user-id}             |                                          |                       | all resources   | reporting, filtering               |
+------------------+-----------------+----------+-----------------------+------------------------------------------+-----------------------+-----------------+------------------------------------+
| taggingVersion   | mandatory       | string   | 1.0.0                 |                                          |                       | all resources   | reporting, filtering               |
+------------------+-----------------+----------+-----------------------+------------------------------------------+-----------------------+-----------------+------------------------------------+

Reference to AWS Naming convention:

:doc: `Naming convention <./naming.html>`_

