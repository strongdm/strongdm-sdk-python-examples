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
import json
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

# The name of an SSH resource that has had queries made against it.
resource_name = "example-ssh"
resources = client.resources.list("name:?", resource_name)
resource = next(resources)

# Retrieve and display all queries made against this resource.
print("Queries made against %s" % resource_name)
queries = client.queries.list("resource_id:?", resource.id)

for query in queries:
    response = client.snapshot_at(query.timestamp).accounts.get(query.account_id)
    account = response.account

    if query.replayable:
        print("Replaying query made by %s at %s" % (account.email, query.timestamp))
        replay_parts = client.replays.list("id:?", query.id)
        for part in replay_parts:
            for event in part.events:
                print(event.data.decode(errors='replace'))
                time.sleep(event.duration.total_seconds())
    else:
        command = json.loads(query.query_body).get('command')
        print("Command run by %s at %s: %s" % (account.email, query.timestamp, command))
