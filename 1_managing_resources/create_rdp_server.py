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

# Set `port_override` to `-1` to auto-generate a port if Port Overrides is enabled.
rdp_server = strongdm.RDP(
    name="Example RDP Server for Python",
    hostname="example.strongdm.com",
    username="example",
    password="example",
    port=3389,
    port_override=19301
)

response = client.resources.create(rdp_server, timeout=30)

print("Successfully created RDP server.")
print("\tName:", response.resource.name)
print("\tID:", response.resource.id)
