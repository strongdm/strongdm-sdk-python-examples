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

print("Successfully created approval workflow step.")
print("\tID:", approval_workflow_step.id)
print("\tApproval Workflow ID:", approval_workflow_step.approval_flow_id)



