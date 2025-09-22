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
"""
AccountsGroups CRUD - Complete CRUD operations for AccountsGroups

This example demonstrates:
- Create: Link accounts (users) to groups
- Read: List and filter account-group relationships
- Delete: Remove account-group relationships
- Creates prerequisite accounts and groups
- Includes complete resource cleanup
"""
import os
import strongdm

def main():
    print("=== AccountsGroups CRUD Example ===\n")

    # Load the SDM API keys from the environment.
    # If these values are not set in your environment,
    # please follow the documentation here:
    # https://www.strongdm.com/docs/api/api-keys/
    api_access_key = os.getenv("SDM_API_ACCESS_KEY")
    api_secret_key = os.getenv("SDM_API_SECRET_KEY")

    if not api_access_key or not api_secret_key:
        print("Error: SDM_API_ACCESS_KEY and SDM_API_SECRET_KEY must be provided")
        return

    client = strongdm.Client(api_access_key, api_secret_key)

    created_accounts = []
    created_groups = []
    created_account_groups = []

    try:
        # === CREATE PREREQUISITE RESOURCES ===
        print("=== CREATING PREREQUISITE RESOURCES ===")

        # Create test accounts
        print("Creating test accounts...")
        accounts_to_create = [
            {
                "email": "account-group-crud-user1@example.com",
                "first_name": "Test",
                "last_name": "User1"
            },
            {
                "email": "account-group-crud-user2@example.com",
                "first_name": "Test",
                "last_name": "User2"
            },
            {
                "email": "account-group-crud-user3@example.com",
                "first_name": "Test",
                "last_name": "User3"
            }
        ]

        for account_data in accounts_to_create:
            user = strongdm.User(
                email=account_data["email"],
                first_name=account_data["first_name"],
                last_name=account_data["last_name"]
            )

            response = client.accounts.create(user, timeout=30)
            created_accounts.append(response.account)

            print(f"  Created account: {response.account.email}")
            print(f"    ID: {response.account.id}")
            print()

        # Create test groups
        print("Creating test groups...")
        groups_to_create = [
            {
                "name": "AccountGroupCRUD-Group1",
                "description": "First group for AccountsGroups CRUD demonstration"
            },
            {
                "name": "AccountGroupCRUD-Group2",
                "description": "Second group for AccountsGroups CRUD demonstration"
            }
        ]

        for group_data in groups_to_create:
            group = strongdm.Group(
                name=group_data["name"],
                description=group_data["description"]
            )

            response = client.groups.create(group, timeout=30)
            created_groups.append(response.group)

            print(f"  Created group: {response.group.name}")
            print(f"    ID: {response.group.id}")
            print()

        print(f"Successfully created {len(created_accounts)} accounts and {len(created_groups)} groups.\n")

        # === CREATE ACCOUNT-GROUP RELATIONSHIPS ===
        print("=== CREATE OPERATIONS ===")
        print("Creating account-group relationships...")

        # Create multiple account-group relationships
        relationships_to_create = [
            {"account": created_accounts[0], "group": created_groups[0]},  # User1 -> Group1
            {"account": created_accounts[1], "group": created_groups[0]},  # User2 -> Group1
            {"account": created_accounts[1], "group": created_groups[1]},  # User2 -> Group2
            {"account": created_accounts[2], "group": created_groups[1]},  # User3 -> Group2
        ]

        for relationship in relationships_to_create:
            account_group = strongdm.AccountGroup(
                account_id=relationship["account"].id,
                group_id=relationship["group"].id
            )

            response = client.accounts_groups.create(account_group, timeout=30)
            created_account_groups.append(response.account_group)

            print(f"  Created relationship:")
            print(f"    ID: {response.account_group.id}")
            print(f"    Account: {relationship['account'].email} ({relationship['account'].id})")
            print(f"    Group: {relationship['group'].name} ({relationship['group'].id})")
            print()

        print(f"Successfully created {len(created_account_groups)} account-group relationships.\n")

        # === READ OPERATIONS ===
        print("=== READ OPERATIONS ===")

        # List all account-group relationships
        print("Listing all account-group relationships:")
        all_account_groups = client.accounts_groups.list('', timeout=30)

        count = 0
        for account_group in all_account_groups:
            count += 1
            print(f"  Relationship {count}: {account_group.account_id} -> {account_group.group_id}")
            print(f"    ID: {account_group.id}")

        print()

        # Filter by specific account ID
        if created_accounts:
            test_account_id = created_accounts[0].id
            print(f"Filtering relationships by account ID ({test_account_id}):")
            filtered_by_account = client.accounts_groups.list(f'accountid:"{test_account_id}"', timeout=30)

            for account_group in filtered_by_account:
                print(f"  Account {test_account_id} is in group: {account_group.group_id}")
                print(f"    Relationship ID: {account_group.id}")
            print()

        # Filter by specific group ID
        if created_groups:
            test_group_id = created_groups[0].id
            print(f"Filtering relationships by group ID ({test_group_id}):")
            filtered_by_group = client.accounts_groups.list(f'groupid:"{test_group_id}"', timeout=30)

            for account_group in filtered_by_group:
                print(f"  Group {test_group_id} contains account: {account_group.account_id}")
                print(f"    Relationship ID: {account_group.id}")
            print()

        # Get specific relationship by ID
        if created_account_groups:
            specific_id = created_account_groups[0].id
            print(f"Getting specific account-group relationship by ID ({specific_id}):")
            specific_relationship = client.accounts_groups.get(specific_id, timeout=30)
            print(f"  Retrieved relationship: {specific_relationship.account_group.account_id} -> {specific_relationship.account_group.group_id}")
            print(f"    ID: {specific_relationship.account_group.id}")
            print()

    except Exception as e:
        print(f"Error during CRUD operations: {e}")

    finally:
        # === CLEANUP (DELETE OPERATIONS) ===
        print("=== CLEANUP (DELETE OPERATIONS) ===")

        # Delete account-group relationships
        if created_account_groups:
            print(f"Deleting {len(created_account_groups)} account-group relationships...")
            for account_group in created_account_groups:
                try:
                    print(f"  Deleting relationship: {account_group.account_id} -> {account_group.group_id}")
                    client.accounts_groups.delete(account_group.id, timeout=30)
                    print(f"  Successfully deleted relationship ID: {account_group.id}")

                    # Verify deletion
                    try:
                        client.accounts_groups.get(account_group.id, timeout=30)
                        print(f"  Warning: Relationship {account_group.id} still exists after deletion")
                    except strongdm.NotFoundError:
                        print(f"  Confirmed: Relationship {account_group.id} no longer exists")
                    except Exception as verify_error:
                        print(f"  Error verifying deletion of relationship {account_group.id}: {verify_error}")

                except Exception as delete_error:
                    print(f"  Error deleting relationship {account_group.id}: {delete_error}")
                print()

        # Delete created groups
        if created_groups:
            print(f"Deleting {len(created_groups)} created groups...")
            for group in created_groups:
                try:
                    print(f"  Deleting group: {group.name} (ID: {group.id})")
                    client.groups.delete(group.id, timeout=30)
                    print(f"  Successfully deleted group: {group.name}")
                except Exception as delete_error:
                    print(f"  Error deleting group {group.name}: {delete_error}")
            print()

        # Delete created accounts
        if created_accounts:
            print(f"Deleting {len(created_accounts)} created accounts...")
            for account in created_accounts:
                try:
                    print(f"  Deleting account: {account.email} (ID: {account.id})")
                    client.accounts.delete(account.id, timeout=30)
                    print(f"  Successfully deleted account: {account.email}")
                except Exception as delete_error:
                    print(f"  Error deleting account {account.email}: {delete_error}")
            print()

        print("=== AccountsGroups CRUD Example Completed ===")

if __name__ == "__main__":
    main()