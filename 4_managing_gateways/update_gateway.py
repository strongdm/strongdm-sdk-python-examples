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

# Create a gateway
gateway = strongdm.Gateway(
    name="example-gateway",
    listen_address="gateway.example.com:5555",
)
create_response = client.nodes.create(gateway, timeout=30)
print("Successfully created gateway.")
print("\tID:", create_response.node.id)
print("\tName:", create_response.node.name)
print("\tToken:", create_response.token)

# Get the gateway
get_response = client.nodes.get(create_response.node.id, timeout=30)
gateway = get_response.node

# Set fields
gateway.name = "example-gateway-updated"

# Update the gateway
update_response = client.nodes.update(gateway, timeout=30)
print("Successfully updated gateway.")
print("\tID:", update_response.node.id)
print("\tName:", update_response.node.name)
