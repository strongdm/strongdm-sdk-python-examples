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
import random
import strongdm

def create_example_resources(client):
  # Create a resource (e.g., Redis)
  redis = strongdm.Redis(
    name = "exampleRedis-%s" % random.randint(0,100000),
    hostname = "example.com",
    port_override = random.randint(3000, 20000),
    tags = {"env": "staging"},
  )
  return client.resources.create(redis).resource

def create_example_role(client, access_rules):
  resp = client.roles.create(
    strongdm.Role(
      name = "exampleRole-%s" % random.randint(0,100000),
      access_rules = access_rules
    )
  )
  return resp.role

def	create_role_grant_via_access_rules(client):
  resource1 = create_example_resources(client)
  resource2 = create_example_resources(client)
  role = create_example_role(client, [{"ids": [ resource1.id ]}])

  # Add Resource2's ID to the Role's Access Rules
  if len(role.access_rules) == 0:
    role.access_rules = [{"ids":[]}]
  role.access_rules[0]["ids"].append(resource2.id)
  role = client.roles.update(role).role


def delete_role_grant_via_access_rules(client):
  resource1 = create_example_resources(client)
  resource2 = create_example_resources(client)
  role = create_example_role(client, [{"ids": [ resource1.id, resource2.id ]}])

  # Remove the ID of the second resource
  role.access_rules[0]["ids"].remove(resource2.id)
  if len(role.access_rules[0]["ids"]) == 0:
    role.access_rules = []
  role = client.roles.update(role)

def list_role_grants_via_access_rules(client):
  resource = create_example_resources(client)
  role = create_example_role(client, [{"ids": [ resource.id ]}])

  # role.access_rules contains each Access Rule associated with the Role
  print(role.access_rules[0]["ids"])


# role_grant_migration.py demonstrates how to emulate Role Grants using Access Rules
# usage:
# python3 role_grant_migration.py
def main():
  client = strongdm.Client(os.getenv("SDM_API_ACCESS_KEY"), os.getenv("SDM_API_SECRET_KEY"))

 	# The RoleGrants API has been deprecated in favor of Access Rules.
 	# When using Access Rules, the best practice is to grant Resources access based on type and tags.
	# If it is _necessary_ to grant access to specific Resources in the same way as Role Grants did,
	# you can use Resource IDs directly in Access Rules as shown in the following examples.

  create_role_grant_via_access_rules(client)
  delete_role_grant_via_access_rules(client)
  list_role_grants_via_access_rules(client)


if __name__ == "__main__":
  main()