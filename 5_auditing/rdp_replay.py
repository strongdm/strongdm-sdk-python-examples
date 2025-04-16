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
import base64
import datetime
import glob
import json
import os
import strongdm
import subprocess
import tempfile
import time

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key, "localhost:8888", True)

# The name of an RDP resource that has had queries made against it.
resource_name = "nebula"
resources = client.resources.list("name:?", resource_name)
resource = next(resources)

# Retrieve and display all queries made against this resource.
print("Queries made against %s" % resource_name)
queries = client.queries.list("resource_id:?", resource.id)

for query in queries:
    response = client.snapshot_at(query.timestamp).accounts.get(
        query.account_id)
    account = response.account

    if query.encrypted:
        print("Skipping encrypted query made by %s at %s" %
              (account.email, query.timestamp))
        print(
            "See encrypted_query_replay.py for an example of query decryption."
        )
    elif query.query_category == "rdp" and query.duration:
        print("Rendering query made by %s at %s" %
              (account.email, query.timestamp))

        replay_chunks = client.replays.list("id:?", query.id)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write out the query in node log format: https://www.strongdm.com/docs/admin/logs/references/post-start/
            data = f'{{"type":"postStart","uuid":"{query.id}","query":{json.dumps(query.query_body)}}}'
            print(f"query data: {data}")
            query_file = os.path.join(temp_dir, "relay.0000000000.log")
            with open(query_file, 'w') as f:
                f.write(data)

            chunk_id = 1
            for chunk in replay_chunks:
                events = []
                for event in chunk.events:
                    events.append({
                        "data": base64.b64encode(event.data).decode("utf-8"),
                        "duration": int(event.duration.total_seconds())
                    })
            
                # Write out the chunk in node log format: https://www.strongdm.com/docs/admin/logs/references/replay-chunks/
                chunk_data = (
                    f'{{"type":"chunk","uuid":"{query.id}","chunkId":"{chunk_id}","events":{json.dumps(events)}}}'
                )
                chunk_file = os.path.join(temp_dir, f"relay.{chunk_id:010}.log")
                with open(chunk_file, 'w') as f:
                    f.write(chunk_data)
                chunk_id += 1

            # Run the sdm CLI to render the RDP session, this must be in the path
            result = subprocess.run(["sdm", "replay", "rdp", query.id] + glob.glob(os.path.join(temp_dir, "*")), check=True, capture_output=True, text=True)
            for line in result.stdout.splitlines():
                # This line will contain the location of the rendered mp4
                if line.startswith("render complete:"):
                    print(line)
