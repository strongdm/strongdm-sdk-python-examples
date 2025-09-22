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
GroupsRoles CRUD - Complete CRUD operations for GroupsRoles

This example demonstrates:
- Create: Link groups to roles
- Read: List and filter group-role relationships by group or role
- Delete: Remove group-role relationships
- Creates prerequisite groups and roles
- Includes complete resource cleanup
"""
import os
import strongdm

def main():
    print("=== GroupsRoles CRUD Example ===\n")

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
    created_roles = []
    created_group_roles = []

    try:
        # === CREATE PREREQUISITE RESOURCES ===
        print("=== CREATING PREREQUISITE RESOURCES ===")

        # Create test groups
        print("Creating test groups...")
        groups_to_create = [
            {
                "name": "GroupRoleCRUD-Group1",
                "description": "First group for GroupsRoles CRUD demonstration"
            },
            {
                "name": "GroupRoleCRUD-Group2",
                "description": "Second group for GroupsRoles CRUD demonstration"
            },
            {
                "name": "GroupRoleCRUD-Group3",
                "description": "Third group for GroupsRoles CRUD demonstration"
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

        # Create test roles
        print("Creating test roles...")
        roles_to_create = [
            {
                "name": "GroupRoleCRUD-Role1"
            },
            {
                "name": "GroupRoleCRUD-Role2"
            }
        ]

        for role_data in roles_to_create:
            role = strongdm.Role(
                name=role_data["name"]
            )

            response = client.roles.create(role, timeout=30)
            created_roles.append(response.role)

            print(f"  Created role: {response.role.name}")
            print(f"    ID: {response.role.id}")
            print()

        print(f"Successfully created {len(created_groups)} groups and {len(created_roles)} roles.\n")

        # === CREATE GROUP-ROLE RELATIONSHIPS ===
        print("=== CREATE OPERATIONS ===")
        print("Creating group-role relationships...")

        # Create multiple group-role relationships
        relationships_to_create = [
            {"group": created_groups[0], "role": created_roles[0]},  # Group1 -> Role1
            {"group": created_groups[1], "role": created_roles[0]},  # Group2 -> Role1
            {"group": created_groups[1], "role": created_roles[1]},  # Group2 -> Role2
            {"group": created_groups[2], "role": created_roles[1]},  # Group3 -> Role2
        ]

        for relationship in relationships_to_create:
            group_role = strongdm.GroupRole(
                group_id=relationship["group"].id,
                role_id=relationship["role"].id
            )

            response = client.groups_roles.create(group_role, timeout=30)
            created_group_roles.append(response.group_role)

            print(f"  Created relationship:")
            print(f"    ID: {response.group_role.id}")
            print(f"    Group: {response.group_role.group_id}")
            print(f"    Role: {response.group_role.role_id}")
            print()

        print(f"Successfully created {len(created_group_roles)} group-role relationships.\n")

        # === READ OPERATIONS ===
        print("=== READ OPERATIONS ===")

        # List all group-role relationships
        print("Listing all group-role relationships:")
        all_group_roles = client.groups_roles.list('', timeout=30)

        count = 0
        for group_role in all_group_roles:
            count += 1
            print(f"  Relationship {count}:")
            print(f"    ID: {group_role.id}")
            print(f"    Group ID: {group_role.group_id}")
            print(f"    Role ID: {group_role.role_id}")

        print()

        # Filter by specific group ID
        if created_groups:
            test_group_id = created_groups[0].id
            print(f"Filtering relationships by group ID ({test_group_id}):")
            filtered_by_group = client.groups_roles.list(f'groupid:"{test_group_id}"', timeout=30)

            for group_role in filtered_by_group:
                print(f"  Relationship:")
                print(f"    Relationship ID: {group_role.id}")
                print(f"    Group ID: {group_role.group_id}")
                print(f"    Role ID: {group_role.role_id}")
            print()

        # Filter by specific role ID
        if created_roles:
            test_role_id = created_roles[0].id
            print(f"Filtering relationships by role ID ({test_role_id}):")
            filtered_by_role = client.groups_roles.list(f'roleid:"{test_role_id}"', timeout=30)

            for group_role in filtered_by_role:
                print(f"  Relationship:")
                print(f"    Relationship ID: {group_role.id}")
                print(f"    Group ID: {group_role.group_id}")
            print()

        # Get specific relationship by ID
        if created_group_roles:
            specific_id = created_group_roles[0].id
            print(f"Getting specific group-role relationship by ID ({specific_id}):")
            specific_relationship = client.groups_roles.get(specific_id, timeout=30)
            print(f"  Retrieved relationship:")
            print(f"    ID: {specific_relationship.group_role.id}")
            print(f"    Group ID: {specific_relationship.group_role.group_id}")
            print(f"    Role ID: {specific_relationship.group_role.role_id}")
            print()

        # === DEMONSTRATE FILTERING BY NAMES ===
        print("=== ADDITIONAL FILTERING EXAMPLES ===")

        # Filter by group name pattern
        print("Filtering relationships by group name pattern:")
        name_filtered = client.groups_roles.list('groupname:"GroupRoleCRUD-Group*"', timeout=30)

        for group_role in name_filtered:
            print(f"  Found: {group_role.id} -> (Group: {group_role.group_id}, Role: {group_role.role_id})")
        print()

    except Exception as e:
        print(f"Error during CRUD operations: {e}")

    finally:
        # === CLEANUP (DELETE OPERATIONS) ===
        print("=== CLEANUP (DELETE OPERATIONS) ===")

        # Delete group-role relationships
        if created_group_roles:
            print(f"Deleting {len(created_group_roles)} group-role relationships...")
            for group_role in created_group_roles:
                try:
                    print(f"  Deleting relationship: {group_role.group_id} -> {group_role.role_id}")
                    client.groups_roles.delete(group_role.id, timeout=30)
                    print(f"  Successfully deleted relationship ID: {group_role.id}")

                    # Verify deletion
                    try:
                        client.groups_roles.get(group_role.id, timeout=30)
                        print(f"  Warning: Relationship {group_role.id} still exists after deletion")
                    except strongdm.NotFoundError:
                        print(f"  Confirmed: Relationship {group_role.id} no longer exists")
                    except Exception as verify_error:
                        print(f"  Error verifying deletion of relationship {group_role.id}: {verify_error}")

                except Exception as delete_error:
                    print(f"  Error deleting relationship {group_role.id}: {delete_error}")
                print()

        # Delete created roles
        if created_roles:
            print(f"Deleting {len(created_roles)} created roles...")
            for role in created_roles:
                try:
                    print(f"  Deleting role: {role.name} (ID: {role.id})")
                    client.roles.delete(role.id, timeout=30)
                    print(f"  Successfully deleted role: {role.name}")
                except Exception as delete_error:
                    print(f"  Error deleting role {role.name}: {delete_error}")
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

        print("=== GroupsRoles CRUD Example Completed ===")

if __name__ == "__main__":
    main()