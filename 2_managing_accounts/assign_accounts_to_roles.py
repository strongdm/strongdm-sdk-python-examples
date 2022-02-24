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
import random
import strongdm as sdm

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/admin-guide/api-credentials/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

def create_example_resources(client):
  # Create a resource (e.g., Redis)
  redis = sdm.Redis(
    name = "exampleRedis-%s" % random.randint(0,100000),
    hostname = "example.com",
    port_override = random.randint(3000, 20000),
    tags = {"env": "staging"},
  )
  return client.resources.create(redis).resource

def create_example_role(client, access_rules):
  resp = client.roles.create(
    sdm.Role(
      name = "exampleRole-%s" % random.randint(0,100000),
      access_rules = access_rules,
    )
  )
  return resp.role

def create_and_update_access_rules(client):
  redis = create_example_resources(client)

  # Create a Role with initial Access Rule
  access_rules = [ {"ids": [redis.id]} ]
  role = create_example_role(client, access_rules)
  # Update Access Rules
  role.access_rules = [
    {
      "tags": {"env": "staging"}
    },
    {
      "type": "redis"
    }
  ]

  client.roles.update(role)

# Create a User
user = strongdm.User(
    email="example@strongdm.com",
    first_name="example",
    last_name="example",
)

user_response = client.accounts.create(user, timeout=30)

print("Successfully created user.")
print("\tEmail:", user_response.account.email)
print("\tID:", user_response.account.id)

# Assign the User to the Role
grant = strongdm.AccountAttachment(
    account_id=user_response.account.id,
    role_id=role_response.role.id
)

attachment_response = client.account_attachments.create(grant, timeout=30)

print("Successfully created account attachment.")
print("\tID:", attachment_response.account_attachment.id)
