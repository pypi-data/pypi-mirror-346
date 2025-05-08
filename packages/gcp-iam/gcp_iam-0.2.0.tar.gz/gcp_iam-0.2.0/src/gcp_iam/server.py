import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS

load_dotenv()

mcp = FastMCP("gcp_iam")

# Setup credentials once for reuse
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)


# -------------------
# Tools
# -------------------
from google.cloud import iam_credentials_v1
from google.cloud import storage
from google.cloud import iam_admin_v1
from google.cloud.iam_admin_v1 import types


# Function to add/remove service account permissions for a resource
@mcp.tool()
def modify_service_account_permissions(resource_name: str, service_account_email: str, role: str, action: str) -> str:
    """Adds or removes a service account's permissions for a resource.

    Args:
        resource_name: The name of the resource (e.g., bucket name).
        service_account_email: The email of the service account.
        role: The role to grant or revoke (e.g., 'roles/storage.objectViewer').
        action: 'add' to grant the role, 'remove' to revoke the role.

    Returns:
        A success message or an error message.
    """
    try:
        client = storage.Client()
        bucket = client.bucket(resource_name)
        policy = bucket.get_iam_policy()

        if action == 'add':
            policy.bindings.append({"role": role, "members": {f"serviceAccount:{service_account_email}"}})
        elif action == 'remove':
            policy.bindings = [binding for binding in policy.bindings if f"serviceAccount:{service_account_email}" not in binding["members"]]
        else:
            return "Invalid action. Use 'add' or 'remove'."

        bucket.set_iam_policy(policy)
        return f"Service account {service_account_email} permissions updated for resource {resource_name}."
    except Exception as e:
        return f"Error: {str(e)}"

# Generalized function to check current IAM policies for a resource
@mcp.tool()
def get_iam_policies(resource_name: str, resource_type: str) -> str:
    """Checks the current IAM policies for a resource.

    Args:
        resource_name: The name of the resource (e.g., bucket name, service account email, or project ID).
        resource_type: The type of the resource (e.g., 'bucket', 'service_account', 'project').

    Returns:
        A string representation of the IAM policies or an error message.
    """
    try:
        if resource_type == 'bucket':
            client = storage.Client()
            bucket = client.bucket(resource_name)
            policy = bucket.get_iam_policy()
            return f"IAM policies for bucket {resource_name}: {policy.bindings}"

        elif resource_type == 'service_account':
            client = iam_admin_v1.IAMClient()
            name = f"projects/-/serviceAccounts/{resource_name}"
            policy = client.get_iam_policy(request={"resource": name})
            return f"IAM policies for service account {resource_name}: {policy.bindings}"

        elif resource_type == 'project':
            from google.cloud import resourcemanager_v3
            client = resourcemanager_v3.ProjectsClient()
            name = f"projects/{resource_name}"
            policy = client.get_iam_policy(request={"resource": name})
            return f"IAM policies for project {resource_name}: {policy.bindings}"

        else:
            return "Error: Unsupported resource type. Supported types are 'bucket', 'service_account', and 'project'."

    except Exception as e:
        return f"Error: {str(e)}"

# Function to grant predefined roles to service accounts
@mcp.tool()
def grant_role_to_service_account(resource_name: str, service_account_email: str, role: str) -> str:
    """Grants a predefined role to a service account for a resource.

    Args:
        resource_name: The name of the resource (e.g., bucket name).
        service_account_email: The email of the service account.
        role: The role to grant (e.g., 'roles/storage.objectViewer').

    Returns:
        A success message or an error message.
    """
    return modify_service_account_permissions(resource_name, service_account_email, role, 'add')

# Function to generate a key for a service account
@mcp.tool()
def generate_service_account_key(service_account_email: str) -> str:
    """Generates a key for a service account.

    Args:
        service_account_email: The email of the service account.

    Returns:
        The path to the generated key file or an error message.
    """
    try:
        client = iam_credentials_v1.IAMCredentialsClient()
        name = f"projects/-/serviceAccounts/{service_account_email}"
        key = client.generate_access_token(name=name, scope=["https://www.googleapis.com/auth/cloud-platform"])
        key_path = f"{service_account_email.replace('@', '_').replace('.', '_')}_key.json"
        with open(key_path, 'w') as key_file:
            key_file.write(key.access_token)
        return f"Key generated and saved to {key_path}."
    except Exception as e:
        return f"Error: {str(e)}"

# Updated function to list all service accounts
@mcp.tool()
def list_service_accounts(project_id: str) -> str:
    """Lists all service accounts in a project.

    Args:
        project_id: The ID of the project.

    Returns:
        A string containing the list of service accounts or an error message.
    """
    try:
        iam_admin_client = iam_admin_v1.IAMClient()
        request = types.ListServiceAccountsRequest()
        request.name = f"projects/{project_id}"

        accounts = iam_admin_client.list_service_accounts(request=request)
        account_emails = [account.email for account in accounts.accounts]
        return f"Service accounts in project {project_id}: {', '.join(account_emails)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to create a service account
@mcp.tool()
def create_service_account(project_id: str, account_id: str, display_name: str) -> str:
    """Creates a new service account in the specified project.

    Args:
        project_id: The ID of the project.
        account_id: The unique ID for the service account.
        display_name: The display name for the service account.

    Returns:
        A success message or an error message.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}"
        service_account = types.ServiceAccount(
            display_name=display_name
        )
        response = client.create_service_account(name=name, account_id=account_id, service_account=service_account)
        return f"Service account {response.email} created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to delete a service account
@mcp.tool()
def delete_service_account(service_account_email: str) -> str:
    """Deletes a service account.

    Args:
        service_account_email: The email of the service account to delete.

    Returns:
        A success message or an error message.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/-/serviceAccounts/{service_account_email}"
        client.delete_service_account(name=name)
        return f"Service account {service_account_email} deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to audit IAM policy changes
@mcp.tool()
def audit_iam_policy_changes(resource_name: str) -> str:
    """Audits IAM policy changes for a resource.

    Args:
        resource_name: The name of the resource (e.g., bucket name).

    Returns:
        A string containing the audit log or an error message.
    """
    try:
        # Placeholder for actual audit logic
        return f"Audit log for {resource_name}: Placeholder for audit details."
    except Exception as e:
        return f"Error: {str(e)}"