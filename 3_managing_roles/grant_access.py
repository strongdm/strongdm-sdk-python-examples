# Copyright 2020 StrongDM Inc
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
# https://www.strongdm.com/docs/admin-guide/api-credentials/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

# Create a datasource
postgres = strongdm.Postgres(
    name="Example Postgres Datasource for Python Access Rules",
    hostname="example.strongdm.com",
    port=5432,
    username="example",
    password="example",
    database="example",
    port_override=19306,
    tags = { "example": "grant-access" },
)

datasource_response = client.resources.create(postgres, timeout=30)

print("Successfully created Postgres datasource.")
print("\tName:", datasource_response.resource.name)
print("\tID:", datasource_response.resource.id)

# Create a role
role = strongdm.Role(
    name="Role for Python Grant Access Example",
    access_rules = [
        {
            "tags": { "example": "grant-access" },
        },
    ]
)

role_response = client.roles.create(role, timeout=30)

print("Successfully created role.")
print("\tID:", role_response.role.id)

# Create a user
user = strongdm.User(
    email="grant-access-example@example.com",
    first_name="example",
    last_name="example",
)

user_response = client.accounts.create(user, timeout=30)

print("Successfully created user.")
print("\tEmail:", user_response.account.email)
print("\tID:", user_response.account.id)

# Attach the user to the role
grant = strongdm.AccountAttachment(
    account_id=user_response.account.id,
    role_id=role_response.role.id
)

attachment_response = client.account_attachments.create(grant, timeout=30)

print("Successfully created account attachment.")
print("\tID:", attachment_response.account_attachment.id)
