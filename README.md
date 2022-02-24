# strongDM Python SDK Examples

This is the examples repository for the [strongDM Python SDK](https://github.com/strongdm/strongdm-sdk-python).

---
> **NOTE:**  
> To increase flexibility when managing thousands of Resources, Role Grants have
been deprecated in favor of Access Rules, which allow you to grant access based
on Resource Tags and Type.
>
> Previously, you would grant a Role access to specific resources by ID via Role
Grants. Now, when using Access Rules, the best practice is to grant Resources access based on Type and Tags.
>
>The following examples demonstrate Dynamic Access Rules with Tags and Resource Types, as well as Static Access Rules for backwards compatibility with Role Grants. If it is _necessary_ to grant access to specific Resources in the same way as RoleGrants did, you can use Resource IDs directly in Access Rules.
---
