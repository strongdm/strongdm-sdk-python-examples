# Copyright 2023 StrongDM Inc
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

# Create a Workflow with initial Access Rule
workflow = strongdm.Workflow(
    name = "Create WorkflowApprover Python Example",
    description = "Workflow Description Python Example",
    access_rules = [
        {
            "tags": { "env": "dev" },
        },
    ]
)

workflow_response = client.workflows.create(workflow, timeout=30)
workflow_id = workflow_response.workflow.id

# Create an approver account - used for creating a workflow approver
user = strongdm.User(
    email="create-workflow-approver-python-example@example.com",
    first_name="Example",
    last_name="Approver",
)

approver_response = client.accounts.create(user, timeout=30)
approver_id = approver_response.account.id

# Create a WorkflowApprover
workflow_approver = strongdm.WorkflowApprover(
    workflow_id=workflow_id,
    account_id=approver_id,
)

workflow_approver_response = client.workflow_approvers.create(workflow_approver, timeout=30)

print("Successfully created WorkflowApprover.")
print("\tID:", workflow_approver_response.workflow_approver.id)