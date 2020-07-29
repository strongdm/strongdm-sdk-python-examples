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

postgres = strongdm.Postgres(
    name="Example Postgres Datasource",
    hostname="example.strongdm.com",
    port=5432,
    username="example",
    password="example",
    database="example",
    port_override=19999,
)

create_response = client.resources.create(postgres, timeout=30)

print("Successfully created Postgres datasource.")
print("\tName: ", create_response.resource.name)
print("\tID: ", create_response.resource.id)

# Load the datasource to update
get_response = client.resources.get(create_response.resource.id, timeout=30)
resource = get_response.resource

# Update the fields to change
resource.name = "Example Name Updated"

# Update the datasource
update_response = client.resources.update(resource, timeout=30)

print("Successfully updated Postgres datasource.")
print("    ID:", update_response.resource.id)
print("  Name:", update_response.resource.name)
