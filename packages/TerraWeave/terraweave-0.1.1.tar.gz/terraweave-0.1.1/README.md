# TerraWeave: A Python Wrapper for Terraform

TerraWeave is a Python library that provides a simple interface for interacting with Terraform. It wraps common Terraform commands such as `init`, `plan`, `apply`, `destroy`, and workspace management, making it easier to integrate Terraform into Python-based workflows.

## Features

- Initialize a Terraform working directory (`terraform init`).
- Generate and show execution plans (`terraform plan`).
- Apply changes to reach the desired state (`terraform apply`).
- Destroy Terraform-managed infrastructure (`terraform destroy`).
- Retrieve Terraform output variables (`terraform output`).
- Manage Terraform workspaces:
  - List workspaces (`terraform workspace list`).
  - Show the current workspace (`terraform workspace show`).
  - Create a new workspace (`terraform workspace new`).
  - Select a workspace (`terraform workspace select`).
  - Delete a workspace (`terraform workspace delete`).

## Installation

#### Pip
``` pip install TerraWeave ```

#### From source
Clone the repository to your local machine:

```bash
git clone https://github.com/brains93/TerraWeave.git
cd TerraWeave
```
Ensure you have Python 3.7+ installed, along with Terraform installed and available in your system's PATH.

Usage
Example: Basic Usage

NOTE: the class uses python logging to print the output to stdout, this can be redirectedto a file using the same logging library 

```
from TerraWeave import TerraformWrapper

# Path to the directory containing Terraform configuration files
working_dir = "/path/to/terraform/config"

# Initialize the TerraformWrapper
tf = TerraformWrapper(working_dir)

# Initialize Terraform
print("Initializing Terraform...")
tf.init()

# Generate a plan
print("Generating Terraform plan...")
tf.plan()

# Apply the changes
print("Applying Terraform changes...")
tf.apply()

# Destroy the infrastructure
print("Destroying Terraform-managed infrastructure...")
tf.destroy()
```






