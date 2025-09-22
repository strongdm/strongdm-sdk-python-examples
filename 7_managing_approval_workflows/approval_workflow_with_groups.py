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
import os
import strongdm
from datetime import datetime, timedelta

# Load the SDM API keys from the environment.
# If these values are not set in your environment,
# please follow the documentation here:
# https://www.strongdm.com/docs/api/api-keys/
api_access_key = os.getenv("SDM_API_ACCESS_KEY")
api_secret_key = os.getenv("SDM_API_SECRET_KEY")
client = strongdm.Client(api_access_key, api_secret_key)

print("Example showing how to create approval workflows using groups as approvers")

# Create approver groups - these groups will be designated as approvers
security_group = strongdm.Group(name="Security Team")
security_group_response = client.groups.create(security_group, timeout=30)
security_group_id = security_group_response.group.id
print(f"Created Security Team group: {security_group_id}")

admin_group = strongdm.Group(name="Administrators")
admin_group_response = client.groups.create(admin_group, timeout=30)
admin_group_id = admin_group_response.group.id
print(f"Created Administrators group: {admin_group_id}")

devops_group = strongdm.Group(name="DevOps Team")
devops_group_response = client.groups.create(devops_group, timeout=30)
devops_group_id = devops_group_response.group.id
print(f"Created DevOps Team group: {devops_group_id}")

# Create some users to add to groups (demonstrating group membership)
security_user = strongdm.User(
    email="security-lead@example.com",
    first_name="Security",
    last_name="Lead"
)
security_user_response = client.accounts.create(security_user, timeout=30)
security_user_id = security_user_response.account.id

admin_user = strongdm.User(
    email="admin-user@example.com",
    first_name="Admin",
    last_name="User"
)
admin_user_response = client.accounts.create(admin_user, timeout=30)
admin_user_id = admin_user_response.account.id

# Add users to their respective groups
security_account_group = strongdm.AccountGroup(
    account_id=security_user_id,
    group_id=security_group_id
)
client.accounts_groups.create(security_account_group, timeout=30)
print("Added security user to Security Team group")

admin_account_group = strongdm.AccountGroup(
    account_id=admin_user_id,
    group_id=admin_group_id
)
client.accounts_groups.create(admin_account_group, timeout=30)
print("Added admin user to Administrators group")

# Create a manual approval workflow with groups as approvers
approval_workflow = strongdm.ApprovalWorkflow(
    name="Group-Based Approval Workflow",
    description="A workflow demonstrating group-based approvers",
    approval_mode="manual"
)

# Step 1: Any member of the Security Team can approve
step1 = strongdm.ApprovalFlowStep(
    quantifier="any",
    approvers=[
        strongdm.ApprovalFlowApprover(group_id=security_group_id)
    ]
)

# Step 2: All specified groups must approve
step2 = strongdm.ApprovalFlowStep(
    quantifier="all",
    skip_after=timedelta(hours=2),
    approvers=[
        strongdm.ApprovalFlowApprover(group_id=admin_group_id),     # Administrators group
        strongdm.ApprovalFlowApprover(group_id=devops_group_id),   # DevOps Team group
        strongdm.ApprovalFlowApprover(reference=strongdm.MANAGER_OF_REQUESTER),  # Plus manager
    ]
)

# Step 3: Mixed approvers - combination of groups and references
step3 = strongdm.ApprovalFlowStep(
    quantifier="any",
    skip_after=timedelta(hours=1),
    approvers=[
        strongdm.ApprovalFlowApprover(group_id=security_group_id),  # Security Team
        strongdm.ApprovalFlowApprover(group_id=admin_group_id),     # Administrators
        strongdm.ApprovalFlowApprover(reference=strongdm.MANAGER_OF_MANAGER_OF_REQUESTER),
    ]
)

approval_workflow.approval_workflow_steps = [step1, step2, step3]

workflow_response = client.approval_workflows.create(approval_workflow, timeout=30)
created_workflow = workflow_response.approval_workflow

print(f"\nSuccessfully created group-based approval workflow.")
print(f"\tID: {created_workflow.id}")
print(f"\tName: {created_workflow.name}")
print(f"\tDescription: {created_workflow.description}")
print(f"\tNumber of Approval Steps: {len(created_workflow.approval_workflow_steps)}")

for i, step in enumerate(created_workflow.approval_workflow_steps, 1):
    print(f"\nStep {i}:")
    print(f"\tQuantifier: {step.quantifier}")
    if step.skip_after:
        print(f"\tSkip After: {step.skip_after}")
    print(f"\tApprovers:")
    for approver in step.approvers:
        if approver.account_id:
            print(f"\t\t- Account ID: {approver.account_id}")
        elif approver.role_id:
            print(f"\t\t- Role ID: {approver.role_id}")
        elif approver.group_id:
            print(f"\t\t- Group ID: {approver.group_id}")
        elif approver.reference:
            print(f"\t\t- Reference: {approver.reference}")

# Demonstrate updating workflow to use different group combinations
updated_workflow = strongdm.ApprovalWorkflow(
    id=created_workflow.id,
    name="Updated Group-Based Approval Workflow",
    description="Updated workflow with different group approver combinations",
    approval_mode="manual"
)

# Single step with multiple group options
updated_step = strongdm.ApprovalFlowStep(
    quantifier="any",
    skip_after=timedelta(hours=24),  # 24 hour timeout
    approvers=[
        strongdm.ApprovalFlowApprover(group_id=security_group_id),
        strongdm.ApprovalFlowApprover(group_id=admin_group_id),
        strongdm.ApprovalFlowApprover(group_id=devops_group_id),
    ]
)

updated_workflow.approval_workflow_steps = [updated_step]

updated_response = client.approval_workflows.update(updated_workflow, timeout=30)
updated_workflow_obj = updated_response.approval_workflow

print(f"\nSuccessfully updated approval workflow:")
print(f"\tNew Name: {updated_workflow_obj.name}")
print(f"\tNew Description: {updated_workflow_obj.description}")
print(f"\tSteps after update: {len(updated_workflow_obj.approval_workflow_steps)}")

step = updated_workflow_obj.approval_workflow_steps[0]
print(f"\tApprovers in updated step (any of these groups can approve):")
for approver in step.approvers:
    if approver.group_id:
        print(f"\t\t- Group ID: {approver.group_id}")

print(f"\nExample demonstrates:")
print(f"  • Creating groups to act as approvers")
print(f"  • Adding users to groups (group membership)")
print(f"  • Using group_id in approval workflow steps")
print(f"  • Combining group approvers with other approver types")
print(f"  • Different quantifiers (any/all) for group-based approval")

# Clean up - delete the approval workflow
client.approval_workflows.delete(updated_workflow_obj.id, timeout=30)
print(f"\nCleaned up approval workflow.")