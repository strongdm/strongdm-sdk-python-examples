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

# Create an auto grant Workflow with initial Access Rule. Note that this 
# workflow will be enabled.
workflow = strongdm.Workflow(
    name = "Create Auto Grant Workflow Python Example",
    description = "Workflow Description Python Example",
    auto_grant = True,
    enabled = True,
    access_rules = [
        {
            "tags": { "env": "dev" },
        },
    ]
)

workflow_response = client.workflows.create(workflow, timeout=30)

print("Successfully created Workflow.")
print("\tID:", workflow_response.workflow.id)