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

postgres = strongdm.Postgres(
    name="Example Postgres Datasource for Update Test",
    hostname="example.strongdm.com",
    port=5432,
    username="example",
    password="example",
    database="example",
    port_override=19303,
)

create_response = client.resources.create(postgres, timeout=30)

print("Successfully created Postgres datasource.")
print("\tName:", create_response.resource.name)
print("\tID:", create_response.resource.id)

# Load the datasource to update
get_response = client.resources.get(create_response.resource.id, timeout=30)
resource = get_response.resource

# Update the fields to change
resource.name = "Example Name Updated for Python"

# If your organization has Virtual Networking Mode enabled,
# you can automatically allocate an IP to that resource via the ResourceIPAllocationMode.VNM constant...
resource.bind_interface = strongdm.ResourceIPAllocationMode.VNM

# ...Or fallback to the default behavior for your organization...
resource.bind_interface = strongdm.ResourceIPAllocationMode.DEFAULT

# ...Or if there is a specific IP to bind to, you can specify it directly.
# For more details on Virtual Networking Mode see documentation here:
# https://docs.strongdm.com/admin/clients/client-networking/virtual-networking-mode
resource.bind_interface = "127.0.0.1"

# Update `port_override` to `-1` to auto-allocate a different available port.
resource.port_override = -1

# Update the datasource
update_response = client.resources.update(resource, timeout=30)

print("Successfully updated Postgres datasource.")
print("\tID:", update_response.resource.id)
print("\tName:", update_response.resource.name)
print("\tBindInterface:", update_response.resource.bind_interface)
print("\tPortOverride:", update_response.resource.port_override)
