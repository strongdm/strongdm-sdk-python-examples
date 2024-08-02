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

policy = strongdm.Policy(name="forbid-everything",
                         description="Forbid everything",
                         policy="forbid ( principal, action, resource );")

create_resp = client.policies.create(policy)
print("Successfully created a policy to forbid all actions.")
print("\tID:", create_resp.policy.id)
print("\tName:", create_resp.policy.name)


# Note: The `policy` field in `create_resp` can also be used to make an
# update. However, we'll load it from the API to demonstrate `get`.
get_resp = client.policies.get(create_resp.policy.id)
print("Successfully retrieved policy.")
print("\tID:", get_resp.policy.id)
print("\tName:", get_resp.policy.name)

update_policy = get_resp.policy
update_policy.name = "forbid-one-thing"
update_policy.description = "forbid connecting to the bad resource"
update_policy.policy = """forbid (
     principal,
     action == StrongDM::Action::"connect",
     resource == StrongDM::Resource::"rs-123d456789"
);
"""

# Update the policy with new values
update_resp = client.policies.update(update_policy)
print("Successfully retrieved policy.")
print("\tID:", get_resp.policy.id)
print("\tName:", get_resp.policy.name)
print("\tDescription:", get_resp.policy.description)
print("\tPolicy:", get_resp.policy.policy)

# Delete the policy
client.policies.delete(create_resp.policy.id)

# Try to retrieve a deleted policy
try:
    client.policies.get(create_resp.policy.id)
except strongdm.errors.NotFoundError:
    pass
