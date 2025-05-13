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
import sys
import os.path
sys.path += [
    os.path.normpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     '../../../generated/python'))
]
import os
import strongdm

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

user = strongdm.User(
    email="create-user-example@example.com",
    first_name="example",
    last_name="example",
    permission_level=strongdm.PermissionLevel.TEAM_LEADER
)

response = client.accounts.create(user, timeout=30)

print("Successfully created user.")
print("\tEmail:", response.account.email)
print("\tID:", response.account.id)


# Assign user as manager for another user
user2 = strongdm.User(
    email="create-user2@example.com",
    first_name="example2",
    last_name="example2",
    manager_id=response.account.id
)

response2 = client.accounts.create(user2, timeout=30)
created_user2 = response2.account

print("Successfully created user with manager assignment.")
print(f"\tID: {created_user2.id}")
print(f"\tManagerID: {created_user2.manager_id}")

# Get resolved_manager_id of user and SCIM metadata if present.
# resolved_manager_id will be set to the manager ID of the user, if present,
# and will be resolved from manager information from SCIM metadata otherwise.
# If no manager information can be resolved from SCIM metadata and manager ID is not set, 
# resolved_manager_id will have no value.
get_resp = client.accounts.get(created_user2.id, timeout=30)
got_user = get_resp.account

print("Successfully fetched user.")
print(f"\tID: {got_user.id}")
print(f"\tManagerID: {got_user.manager_id}")
print(f"\tResolvedManagerID: {got_user.resolved_manager_id}")
print(f"\tSCIM Metadata: {got_user.scim}")

# Update the user to clear out the manager assignment
got_user.manager_id = ""
update_resp = client.accounts.update(got_user, timeout=30)
updated_user = update_resp.account

print("Successfully updated user.")
print(f"\tID: {updated_user.id}")
print(f"\tManagerID: {updated_user.manager_id}")