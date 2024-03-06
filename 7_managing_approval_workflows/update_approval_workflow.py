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
    approval_mode = "automatic"
)

response = client.approval_workflows.create(approval_workflow, timeout=30)
approval_workflow = response.approval_workflow
id = approval_workflow.id
name = approval_workflow.name

print("Successfully created approval workflow.")
print("\tID:", id)

# Update the approval workflow name
approval_workflow.name = "Example New Name"
update_response = client.approval_workflows.update(approval_workflow, timeout=30)
approval_workflow = update_response.approval_workflow

print("Successfully update approval workflow name.")
print("\tNew Name:", approval_workflow.name)

# Update the approval workflow description
approval_workflow.description = "Example New Description"
update_response = client.approval_workflows.update(approval_workflow, timeout=30)
approval_workflow = update_response.approval_workflow

print("Successfully update approval workflow description.")
print("\tNew Description:", approval_workflow.description)

# Update the approval workflow approval mode
approval_workflow.approval_mode = "manual"
update_response = client.approval_workflows.update(approval_workflow, timeout=30)
approval_workflow = update_response.approval_workflow

print("Successfully update approval workflow approval mode.")
print("\tNew Approval Mode:", approval_workflow.approval_mode)

