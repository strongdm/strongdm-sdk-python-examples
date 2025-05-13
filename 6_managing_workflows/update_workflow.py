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

# Update Workflow AutoGrant
auto = workflow.auto_grant
workflow.auto_grant = not auto
update_response = client.workflows.update(workflow, timeout=30)
workflow = update_response.workflow

print("Successfully update Workflow AutoGrant.")
print("\tAutoGrant:", workflow.auto_grant)

# Update Workflow Enabled
# The requirements to enable a workflow are that the workflow must be either set
# up for with auto grant enabled or have one or more WorkflowApprovers created for
# the workflow.
workflow.auto_grant = True
workflow.enabled = True
update_response = client.workflows.update(workflow, timeout=30)
workflow = update_response.workflow

print("Successfully update Workflow Enabled.")
print("\tEnabled:", workflow.enabled)


