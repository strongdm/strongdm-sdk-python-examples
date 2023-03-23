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
import base64
import datetime
import json
import os
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import strongdm

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

# Load the private key for query and replay decryption.
# This environment variable should contain the path to the private encryption
# key configured for StrongDM remote log encryption.
private_key_file = os.getenv("SDM_LOG_PRIVATE_KEY_FILE")
private_key = serialization.load_pem_private_key(open(private_key_file,
                                                      'rb').read(),
                                                 password=None)

# The name of an SSH resource that has had queries made against it.
resource_name = "example-ssh"
resources = client.resources.list("name:?", resource_name)
resource = next(resources)

# Retrieve and display all queries made against this resource.
print("Queries made against %s" % resource_name)
queries = client.queries.list("resource_id:?", resource.id)


# This method demonstrates how to decrypt encrypted query/replay data
def decrypt_query_data(encrypted_query_key, encrypted_data):
    # Use the organization's private key to decrypt the symmetric key
    symmetric_key = private_key.decrypt(
        base64.b64decode(encrypted_query_key),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ))
    # Use the symmetric key to decrypt the data
    iv = encrypted_data[:algorithms.AES.block_size // 8]
    ciphertext = encrypted_data[algorithms.AES.block_size // 8:]
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode().rstrip('\x00')


for query in queries:
    response = client.snapshot_at(query.timestamp).accounts.get(
        query.account_id)
    account = response.account

    if query.encrypted:
        print("Decrypting encrypted query")
        query.query_body = decrypt_query_data(
            query.query_key,
            base64.b64decode(query.query_body),
        )
        query.replayable = json.loads(query.query_body).get('type') == 'shell'

    if query.replayable:
        print("Replaying query made by %s at %s" %
              (account.email, query.timestamp))
        replay_parts = client.replays.list("id:?", query.id)
        for part in replay_parts:
            if query.encrypted:
                events = json.loads(
                    decrypt_query_data(query.query_key, part.data))
                part.events = [
                    strongdm.ReplayChunkEvent(
                        data=base64.b64decode(e['data']),
                        duration=datetime.timedelta(
                            milliseconds=e['duration']),
                    ) for e in events
                ]
            for event in part.events:
                print(event.data.decode(errors='replace'))
                time.sleep(event.duration.total_seconds())
    else:
        command = json.loads(query.query_body).get('command')
        print("Command run by %s at %s: %s" %
              (account.email, query.timestamp, command))
