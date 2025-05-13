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

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

# Create an auto grant Workflow with initial Access Rule.
workflow = strongdm.Workflow(
    name = "Create Manual Workflow Python Example",
    description = "Workflow Description Python Example",
    access_rules = [
        {
            "tags": { "env": "dev" },
        },
    ]
)

workflow_response = client.workflows.create(workflow, timeout=30)
workflow = workflow_response.workflow
workflow_id = workflow.id

print("Successfully created Workflow.")
print("\tID:", workflow_id)

# To allow users access to the resources managed by this workflow, you must
# add workflow roles to the workflow.
# Two steps are needed to add a workflow role:
# Step 1: create a Role
# Step 2: create a WorkflowRole

# Create a Role - used for creating a workflow role
role = strongdm.Role(
    name="Role for Manual Workflow Python Example",
)

role_response = client.roles.create(role, timeout=30)
role_id = role_response.role.id

# Create a WorkflowRole
workflow_role = strongdm.WorkflowRole(
    workflow_id=workflow_id,
    role_id=role_id,
)

workflow_role_response = client.workflow_roles.create(workflow_role, timeout=30)

print("Successfully created WorkflowRole.")
print("\tID:", workflow_role_response.workflow_role.id)

# To manually enable this workflow, you must add workflow approvers
# to this workflow.
# Two steps are needed to add a workflow approver:
# Step 1: create an Account
# Step 2: create a WorkflowApprover

# Create a approver - used for creating a workflow approver
user = strongdm.User(
    email="create-workflow-python-example@example.com",
    first_name="Example",
    last_name="Approver",
)

approver_response = client.accounts.create(user, timeout=30)
approver_id = approver_response.account.id

# Create a WorkflowApprover
workflow_approver = strongdm.WorkflowApprover(
    workflow_id=workflow_id,
    approver_id=approver_id,
)

workflow_approver_response = client.workflow_approvers.create(workflow_approver, timeout=30)

print("Successfully created WorkflowApprover.")
print("\tID:", workflow_approver_response.workflow_approver.id)

# You can enable this workflow after adding workflow approvers.
# Update Workflow Enabled
workflow.enabled = True
workflow_update_response = client.workflows.update(workflow, timeout=30)
workflow = workflow_update_response.workflow

print("Successfully updated Workflow Enabled.")
print("\tEnabled:", workflow.enabled)