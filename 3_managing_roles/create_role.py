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
      access_rules = access_rules
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