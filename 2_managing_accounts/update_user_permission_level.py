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

# Create an account
user = strongdm.User(
    email="update-permissions-example@strongdm.com",
    first_name="example",
    last_name="example",
    permission_level=strongdm.PermissionLevel.TEAM_LEADER
)
response = client.accounts.create(user, timeout=30)
print("Successfully created user.")
print("\tEmail:", response.account.email)
print("\tID:", response.account.id)
print("\tPermission Level:", response.account.permission_level)

# Get the account
get_response = client.accounts.get(response.account.id, timeout=30)
account = get_response.account

# Set fields
account.permission_level = strongdm.PermissionLevel.DATABASE_ADMIN

# Update the account
update_response = client.accounts.update(account, timeout=30)
print("Successfully updated permission level.")
print("\tID:", update_response.account.id)
print("\tPermission Level:", update_response.account.permission_level)
