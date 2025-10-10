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

# Create a Workflow.
workflow = strongdm.Workflow(
    name = "Update Workflow Python Example",
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

# Update Workflow Name
workflow.name = "Update Workflow Python Example New Name"
update_response = client.workflows.update(workflow, timeout=30)
workflow = update_response.workflow

print("Successfully update Workflow Name.")
print("\tNew Name:", workflow.name)

# Update Workflow Description
workflow.description = "Workflow New Description Python Example"
update_response = client.workflows.update(workflow, timeout=30)
workflow = update_response.workflow

print("Successfully update Workflow Description.")
print("\tNew Description:", workflow.description)

# Update Workflow Weight
old_weight = workflow.weight
workflow.weight = old_weight + 20
update_response = client.workflows.update(workflow, timeout=30)
workflow = update_response.workflow

print("Successfully update Workflow Weight.")
print("\tNew Weight:", workflow.weight)

# Create an automatic grant approval flow
approval_flow = strongdm.ApprovalWorkflow(
    name = "Auto Grant Example",
    approval_mode = "automatic"
)
approval_flow_response = client.approval_workflows.create(approval_flow, timeout=30)

print("Successfully created ApprovalWorkflow.")
print("\tID:", approval_flow_response.approval_workflow.id)

# Update Workflow Approval Flow
workflow.approval_flow_id = approval_flow_response.approval_workflow.id
update_response = client.workflows.update(workflow, timeout=30)
workflow = update_response.workflow

print("Successfully update Workflow Approval Flow.")
print("\tApproval Flow ID:", workflow.approval_flow_id)

# Update Workflow Enabled
# To enable a workflow, an approval flow must be attached.
workflow.enabled = True
update_response = client.workflows.update(workflow, timeout=30)
workflow = update_response.workflow

print("Successfully update Workflow Enabled.")
print("\tEnabled:", workflow.enabled)


