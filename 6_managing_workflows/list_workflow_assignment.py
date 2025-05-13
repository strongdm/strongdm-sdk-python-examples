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

# Create a Resource - used for workflow assignments
postgres = strongdm.Postgres(
    name="Example Postgres Datasource for Python",
    hostname="example.strongdm.com",
    port=5432,
    username="example",
    password="example",
    database="example",
    port_override=19300,
)

resource_response = client.resources.create(postgres, timeout=30)
resource_id = resource_response.resource.id

# Create a Workflow
workflow = strongdm.Workflow(
    name = "List Workflow Assignment Python Example",
    description = "Workflow Description Python Example",
    access_rules = [{"ids": [ resource_id ]}]
)

workflow_response = client.workflows.create(workflow, timeout=30)
workflow = workflow_response.workflow
workflow_id = workflow.id

print("Successfully created Workflow.")
print("\tID:", workflow_id)

# List workflow assignments
list_resp = client.workflow_assignments.list("resource:?", resource_id)
print("List Workflow Assignments")
for l in list_resp:
    print("\tWorkflowAssignment Workflow ID: %s" % (l.workflow_id))

print("Successfully list WorkflowAssignment.")

