# Copyright 2025 StrongDM Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import strongdm
from datetime import timedelta

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

# Create an approver account - this account is designated as an approver in the approval workflow created below,
# allowing this user to grant approval
user = strongdm.User(
    email="create-approver-example@example.com",
    first_name="Example",
    last_name="Example",
)
account_response = client.accounts.create(user, timeout=30)
account_id = account_response.account.id
user2 = strongdm.User(
    email="create-approver-example@example.com",
    first_name="Example",
    last_name="Example",
)
account2_response = client.accounts.create(user2, timeout=30)
account2_id = account_response.account.id

# Create an approver role - this role is designated as an approver in the approval workflow created below,
# allowing any user in this role to grant approval
role = strongdm.Role(
    name="Approval Workflow Role Example",
)
role_response = client.roles.create(role, timeout=30)
role_id = role_response.role.id

approval_workflow = strongdm.ApprovalWorkflow(
    name="Approval Workflow Example",
    description="a test approval workflow",
    approval_mode="manual",
    approval_workflow_steps=[
        strongdm.ApprovalFlowStep(
            approvers=[
                strongdm.ApprovalFlowApprover(account_id=account_id),
                strongdm.ApprovalFlowApprover(role_id=role_id)
            ],
            quantifier="all",
        ),
        strongdm.ApprovalFlowStep(
            approvers=[
                strongdm.ApprovalFlowApprover(account_id=account2_id),
            ],
            quantifier="any",
            skip_after=timedelta(hours=1)
        )
    ],
)

response = client.approval_workflows.create(approval_workflow, timeout=30)
id = response.approval_workflow.id
name = response.approval_workflow.name
approval_mode = response.approval_workflow.approval_mode
num_approval_steps = len(response.approval_workflow.approval_workflow_steps)

print("Successfully created approval workflow.")
print("\tID:", id)
print("\tName:", name)
print("\tApproval Mode:", approval_mode)
print("\tNum Approval Steps:", num_approval_steps)
