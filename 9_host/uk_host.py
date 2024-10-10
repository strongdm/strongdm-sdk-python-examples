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

# Configure a client to communicate with the UK host.
# If the host value is not provided, it will default to the US control plane (api.strongdm.com:443)
client = strongdm.Client(api_access_key, api_secret_key, host=strongdm.APIHost.UK)

# Create a Postgres Datasource for example
postgres = strongdm.Postgres(
    name="Example Postgres Datasource for Python",
    hostname="example.strongdm.com",
    port=5432,
    username="example",
    password="example",
    database="example",
    port_override=19300,
)

response = client.resources.create(postgres, timeout=30)

print("Successfully created Postgres datasource.")
print("\tName:", response.resource.name)
print("\tID:", response.resource.id)
