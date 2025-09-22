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
Groups CRUD - Complete CRUD operations for Groups

This example demonstrates:
- Create: Create new groups
- Read: List and filter groups
- Update: Modify group properties
- Delete: Remove groups
- Includes resource cleanup after demonstration
"""
import os
import strongdm

def main():
    print("=== Groups CRUD Example ===\n")

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

    created_groups = []

    try:
        # === CREATE ===
        print("=== CREATE OPERATION ===")
        print("Creating sample groups...")

        # Create multiple groups with different properties
        groups_to_create = [
            {
                "name": "ExampleGroup1",
                "description": "First example group for CRUD demonstration",
                "tags": {"environment": "demo", "team": "engineering", "purpose": "crud-example", "index": "1"}
            },
            {
                "name": "ExampleGroup2",
                "description": "Second example group for CRUD demonstration",
                "tags": {"environment": "demo", "team": "marketing", "purpose": "crud-example", "index": "2"}
            },
            {
                "name": "ExampleGroup3",
                "description": "Third example group for CRUD demonstration",
                "tags": {"environment": "demo", "team": "sales", "purpose": "crud-example", "index": "3"}
            }
        ]

        for group_data in groups_to_create:
            group = strongdm.Group(
                name=group_data["name"],
                description=group_data["description"],
                tags=group_data["tags"]
            )

            response = client.groups.create(group, timeout=30)
            created_groups.append(response.group)

            print(f"  Created group: {response.group.name}")
            print(f"    ID: {response.group.id}")
            print(f"    Description: {response.group.description}")
            print(f"    Tags: {dict(response.group.tags)}")
            print()

        print(f"Successfully created {len(created_groups)} groups.\n")

        # === READ ===
        print("=== READ OPERATIONS ===")

        # List all groups
        print("Listing all groups:")
        all_groups = client.groups.list('', timeout=30)

        count = 0
        for group in all_groups:
            count += 1
            print(f"  Group {count}: {group.name} (ID: {group.id})")

        print()

        # List groups with filtering
        print("Listing groups filtered by name (showing our created examples):")
        filtered_groups = client.groups.list('name:"ExampleGroup*"', timeout=30)

        filtered_count = 0
        for group in filtered_groups:
            filtered_count += 1
            print(f"  Filtered Group {filtered_count}: {group.name}")
            print(f"    ID: {group.id}")
            print(f"    Description: {group.description}")
            print(f"    Tags: {dict(group.tags)}")
            print()

        print(f"Total filtered groups: {filtered_count}")
        print()

        # === UPDATE ===
        print("=== UPDATE OPERATION ===")
        if created_groups:
            group_to_update = created_groups[0]
            original_name = group_to_update.name

            print(f"Updating group: {original_name}")
            print(f"  Original name: {group_to_update.name}")
            print(f"  Original description: {group_to_update.description}")

            # Update the group's properties
            group_to_update.name = f"{original_name}_Updated"
            group_to_update.description = f"{group_to_update.description} - Updated via CRUD example"

            # Add/update tags
            updated_tags = dict(group_to_update.tags)
            updated_tags["updated"] = "true"
            updated_tags["update_timestamp"] = "2025-09-22"
            group_to_update.tags = updated_tags

            update_response = client.groups.update(group_to_update, timeout=30)

            print(f"  Updated name: {update_response.group.name}")
            print(f"  Updated description: {update_response.group.description}")
            print(f"  Updated tags: {dict(update_response.group.tags)}")
            print()

            # Update the local reference for cleanup
            created_groups[0] = update_response.group

        print("Update operation completed.\n")

        # === DEMONSTRATE ADDITIONAL READ OPERATIONS ===
        print("=== ADDITIONAL READ EXAMPLES ===")

        # Filter by tags
        print("Filtering groups by tags (purpose=crud-example):")
        tag_filtered_groups = client.groups.list('tags:purpose="crud-example"', timeout=30)

        for group in tag_filtered_groups:
            print(f"  Group: {group.name} - Team: {group.tags.get('team', 'N/A')}")
        print()

        # Get specific group by ID
        if created_groups:
            specific_group_id = created_groups[0].id
            print(f"Getting specific group by ID ({specific_group_id}):")
            specific_group = client.groups.get(specific_group_id, timeout=30)
            print(f"  Retrieved: {specific_group.group.name}")
            print(f"  Description: {specific_group.group.description}")
            print()

    except Exception as e:
        print(f"Error during CRUD operations: {e}")

    finally:
        # === CLEANUP (DELETE) ===
        print("=== CLEANUP (DELETE OPERATIONS) ===")
        print(f"Cleaning up {len(created_groups)} created groups...")

        for group in created_groups:
            try:
                print(f"  Deleting group: {group.name} (ID: {group.id})")
                client.groups.delete(group.id, timeout=30)
                print(f"  Successfully deleted: {group.name}")

                # Verify deletion
                try:
                    client.groups.get(group.id, timeout=30)
                    print(f"  Warning: Group {group.name} still exists after deletion")
                except strongdm.NotFoundError:
                    print(f"  Confirmed: Group {group.name} no longer exists")
                except Exception as verify_error:
                    print(f"  Error verifying deletion of {group.name}: {verify_error}")

            except Exception as delete_error:
                print(f"  Error deleting group {group.name}: {delete_error}")
            print()

        print("=== Groups CRUD Example Completed ===")

if __name__ == "__main__":
    main()