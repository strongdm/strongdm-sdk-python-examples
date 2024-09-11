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

# Create an account
# Setting a password when creating an account is not supported
user = strongdm.User(
    email="set-password-example@strongdm.com",
    first_name="example",
    last_name="example",
    permission_level=strongdm.PermissionLevel.USER
)
response = client.accounts.create(user)
print("Successfully created user.")
print("\tEmail:", response.account.email)
print("\tID:", response.account.id)

# Password is a write-only field
# The current password is never returned in any responses
assert response.account.password == ''

# Get the account
get_response = client.accounts.get(response.account.id)
account = get_response.account
assert account.password == ''

# Set new password according to organization password complexity requirements
account.password = 'correct horse battery staple'

# Update the account with the new password
update_response = client.accounts.update(account)
assert update_response.account.password == ''
print("Successfully updated password.")
print("\tID:", update_response.account.id)
print("\tNew password:", account.password)