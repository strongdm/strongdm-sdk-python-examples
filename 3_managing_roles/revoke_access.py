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
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

# Create a datasource
postgres = strongdm.Postgres(
    name="Example Postgres Datasource for Python Revoke Test",
    hostname="example.strongdm.com",
    port=5432,
    username="example",
    password="example",
    database="example",
    port_override=19307,
    tags = { "example": "revoke-access" },
)

postgres = client.resources.create(postgres, timeout=30).resource

print("Successfully created Postgres datasource.")
print("\tName:", postgres.name)
print("\tID:", postgres.id)

# Create a role
role = strongdm.Role(
    name="Role for Python Revoke Access Example",
    access_rules = [
        {
            "tags": { "example": "revoke-access" },
        },
    ]
)

role = client.roles.create(role, timeout=30).role

print("Successfully created role.")
print("\tID:", role.id)

# Create a user
user = strongdm.User(
    email="revoke-access-example@example.com",
    first_name="example",
    last_name="example",
)

user = client.accounts.create(user, timeout=30).account

print("Successfully created user.")
print("\tEmail:", user.email)
print("\tID:", user.id)

# Attach the user to the role
grant = strongdm.AccountAttachment(
    account_id=user.id,
    role_id=role.id
)

grant = client.account_attachments.create(grant, timeout=30).account_attachment

print("Successfully created account attachment.")
print("\tID:", grant.id)

# Option 1: delete access rules
role.access_rules = []
role = client.roles.update(role, timeout=30).role
print("Successfully deleted access rules.")

# Option 2: delete account attachment
client.account_attachments.delete(grant.id, timeout=30)
print("Successfully deleted account attachment.")

# Option 3: remove tag from resource
postgres.tags = {}
postgres = client.resources.update(postgres, timeout=30).resource
print("Successfully removed tag from resource.")