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
import sys
import os.path
sys.path += [
    os.path.normpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     '../../../generated/python'))
]
import os
import strongdm
from datetime import timedelta

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

req = strongdm.Token()
req.name = "mytoken_test_token_account_create"
req.account_type = "api"
req.duration = timedelta(hours=1)
req.permissions = ["role:list"]
resp = client.accounts.create(req, timeout=30)
account = resp.account

print("Successfully created token.")
print("\tEmail:", resp.account.name)
print("\tID:", resp.account.id)

# get old token by name
resp = client.accounts.list("name:" + account.name)
accounts = [account for account in resp]
if len(accounts) != 1 {
    print("Get token by name returned more than one or no results")
}
old_token = accounts[0]

old_id = old_token.id
old_permissions = old_token.permissions
old_name = old_token.name
old_token_type = old_token.account_type

# deprecate old token name
deprecated_name = old_name + "-deprecated"
account.name = deprecated_name
resp = client.accounts.update(account, timeout=30)
account = resp.account
print("Successfully updated old token name.")

# create new token
newReq = strongdm.Token()
newReq.name = old_name
newReq.account_type = old_token_type
newReq.duration = timedelta(hours=1)
newReq.permissions = old_permissions
resp = client.accounts.create(req, timeout=30)
account = resp.account
print("Successfully created new token")

# delete old token
client.accounts.delete(old_id, timeout=30)
print("Successfully rotated token.")
