# Copyright 2023 StrongDM Inc
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
import datetime
import os
import strongdm
import time

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/admin-guide/api-credentials/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

started_at = datetime.datetime.utcnow()

# Create an example Redis resource.
resource = strongdm.Redis(
    name="example-redis",
    hostname="example-redis",
    username="example-username",
)

response = client.resources.create(resource)
resource_id = response.resource.id

created_at = datetime.datetime.utcnow()

print("Created resource with ID %s at time %s" % (resource_id, created_at))

# Update the name of the resource.
response.resource.name = "example-redis-renamed"
client.resources.update(response.resource)

renamed_at = datetime.datetime.utcnow()

# Delete the resource.
client.resources.delete(resource_id)

deleted_at = datetime.datetime.utcnow()

# Audit records may take a few seconds to be processed.
time.sleep(2)

# At a time before its creation the resource does not exist
try:
    client.snapshot_at(started_at).resources.get(resource_id)
    raise Exception('Resource should not exist before its creation')
except strongdm.errors.NotFoundError:
    print("Resource does not exist at time %s" % started_at)

# At the time of its creation the resource was named "example-redis"
response = client.snapshot_at(created_at).resources.get(resource_id)
print("Resource had name %s at time %s" % (response.resource.name, created_at))

# At the time of its rename the resource was named "example-redis-renamed"
response = client.snapshot_at(renamed_at).resources.get(resource_id)
print("Resource had name %s at time %s" % (response.resource.name, renamed_at))

# At a time after its deletion the resource does not exist
try:
    client.snapshot_at(deleted_at).resources.get(resource_id)
    raise Exception('Resource should not exist after its deletion')
except strongdm.errors.NotFoundError:
    print("Resource does not exist at time %s" % deleted_at)

# The history of all changes to this resource and their associated activity
history = client.resources_history.list("id:?", resource_id)
for h in history:
    print("Resource had name %s at time %s" % (h.resource.name, h.timestamp))
    response = client.activities.get(h.activity_id)
    print("\t" + response.activity.description)
