import argparse
from .server import mcp

def main():
    """GCP IAM Extension: Interact with IAM resources like service accounts and roles."""
    parser = argparse.ArgumentParser(
        description="Tools for querying and managing Google Cloud IAM resources."
    )
    parser.parse_args()
    mcp.run()

if __name__ == "__main__":
    main()
