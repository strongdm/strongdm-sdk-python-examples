# Copyright 2024 StrongDM Inc
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

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

# Create an approval workflow
approval_workflow = strongdm.ApprovalWorkflow(
    name = "Approval Workflow Example",
    approval_mode = "manual"
)

response = client.approval_workflows.create(approval_workflow, timeout=30)
approval_workflow = response.approval_workflow
flow_id = approval_workflow.id

# Create an approval workflow step
step = strongdm.ApprovalWorkflowStep(
    approval_flow_id = flow_id
)

response = client.approval_workflow_steps.create(step, timeout=30)
approval_workflow_step = response.approval_workflow_step
step_id = approval_workflow_step.id

# Create an approver account - used for creating an approval workflow approver
user = strongdm.User(
    email="delete-approver-example@example.com",
    first_name="Example",
    last_name="Example",
)

account_response = client.accounts.create(user, timeout=30)
account_id = account_response.account.id

# Create an approval workflow approver
approvalWorkflowApprover = strongdm.ApprovalWorkflowApprover(
    approval_flow_id = flow_id,
    approval_step_id = step_id,
    account_id = account_id,
)

response = client.approval_workflow_approvers.create(approvalWorkflowApprover, timeout=30)
approval_workflow_approver = response.approval_workflow_approver
approver_id = approval_workflow_approver.id

print("Successfully created approval workflow approver.")
print("\tID:", approver_id)

# Delete an approval workflow approver
client.approval_workflow_approvers.delete(approver_id, timeout=30)
print("Successfully deleted approval workflow approver.")