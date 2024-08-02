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


example_policies = [
    strongdm.Policy(
        name="default-permit-policy",
        description="a default permit policy",
        policy="permit (principal, action, resource);"
    ),
    strongdm.Policy(
        name="permit-sql-select-policy",
        description="a permit sql select policy",
        policy="""permit (principal, action == SQL::Action::"select", resource == Postgres::Database::"*");"""
    ),
    strongdm.Policy(
        name="default-forbid-policy",
        description="a default forbid policy",
        policy="forbid (principal, action, resource);"
    ),
    strongdm.Policy(
        name="forbid-connect-policy",
        description="a forbid connect policy",
        policy="""forbid (principal, action == StrongDM::Action::"connect", resource);"""
    ),
    strongdm.Policy(
        name="forbid-sql-delete-policy",
        description="a forbid delete policy on all resources",
        policy="""forbid (principal, action == SQL::Action::"delete", resource == Postgres::Database::"*");"""
      )
]

# Keep track of created policies so we can delete them at the end.
policies_to_cleanup = []


# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

# Create our example policies to search through
for p in example_policies:
    create_resp = client.policies.create(p)
    print("Successfully created Policy.")
    print("\tID:", create_resp.policy.id)
    print("\tName:", create_resp.policy.name)
    policies_to_cleanup.append(create_resp.policy)


# Find policies related to `sql` by Name
print("Finding all Policies with a name containing 'sql'")
for p in client.policies.list("name:*sql*"):
    print("\tID: {}\tName:{}".format(p.id, p.name))

print("Finding all Policies that forbid")
# Find policies that forbid based on the Policy
for p in client.policies.list("policy:forbid*"):
    print("\tID: {}\tName:{}".format(p.id, p.name))

# Cleanup the policies we created
for p in policies_to_cleanup:
    client.policies.delete(p.id)
