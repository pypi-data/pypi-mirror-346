<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg" alt="Apache 2.0 License"></a>
  <a href="https://github.com/cdklabs/cdk-cicd-wrapper/actions/workflows/release.yml"><img src="https://github.com/cdklabs/cdk-data-zone/actions/workflows/release.yml/badge.svg" alt="Release badge"></a>
  <a href="https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cdklabs/cdk-data-zone"><img src="https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue" alt="Open in DEV Containers"></a>
</p>

# CDK Amazon DataZone Construct Library

**CDK Amazon DataZone** is an AWS CDK construct library that simplifies the creation and management of **Amazon DataZone** resources. This library enables developers to automate data governance, data cataloging, and secure data sharing across domains by using familiar infrastructure-as-code practices with AWS CDK.

## Features

* Easily create and manage Amazon DataZone components, such as Domains, Projects, and Environments.
* Seamless integration with the AWS CDK ecosystem, allowing users to manage DataZone resources alongside other AWS resources.
* Support for secure resource configurations like KMS encryption, S3 bucket management, and domain-level blueprinting.

## Installation

To install this library, use the following npm command:

```bash
npm install @cdklabs/cdk-data-zone
```

## Usage Example

Here’s an example of how to use the **@cdklabs/cdk-data-zone** library in your AWS CDK project:

```python
from aws_cdk import App, RemovalPolicy
from aws_cdk.aws_kms import Key
from aws_cdk.aws_s3 import Bucket, BucketEncryption


app = App()
stack = Stack(app, "TestStack")

# Create an S3 Bucket for the Blueprint
bucket = Bucket(stack, "BlueprintBucket",
    enforce_sSL=True,
    removal_policy=RemovalPolicy.DESTROY,
    auto_delete_objects=True,
    encryption=BucketEncryption.S3_MANAGED
)

# Create a DataZone Domain
domain = Domain(stack, "Domain",
    name="integration",
    encryption_key=Key(stack, "Key", enable_key_rotation=True)
)

# Enable a Blueprint for the Domain
blueprint = domain.enable_blueprint(BlueprintEnvironmentIdentifiers.DEFAULT_DATA_LAKE,
    parameters={
        "S3Location": f"s3://{bucket.bucketName}"
    }
)

# Create a Project within the Domain
project = domain.create_project("test-project",
    name="test-project",
    glossaries=Glossaries.from_file("./resources/glossaries.json"),
    forms=Forms.from_file("./resources/form-metadata.json")
)

# Create an Environment Profile for the Project
environment_profile = EnvironmentProfile(stack, "EnvironmentProfile",
    name="dev",
    blueprint=blueprint,
    project=project
)

# Create an Environment using the Environment Profile
Environment(stack, "environment",
    project=project,
    name="DEV",
    environment_profile=environment_profile
)

app.synth()
```

### Key Features Highlighted

* **Domain Creation**: Easily create Amazon DataZone Domains with encryption and other security features.
* **Project Management**: Use Blueprints, Forms, and Glossaries to structure data governance.
* **Environment Profiles**: Manage different environments within your data projects to ensure proper data governance policies.

## Projen for Development

This project leverages **Projen** for managing development workflows. Projen automates common tasks like dependency management, testing, and versioning.

### Getting Started with Development

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/cdklabs/cdk-data-zone.git
   cd cdk-data-zone
   ```
2. **Install Dependencies**:

   ```bash
   npx projen install
   ```
3. **Run Projen** to synthesize files:

   ```bash
   npx projen
   ```
4. **Build the Project**:

   ```bash
   npx projen build
   ```
5. **Run Tests**:

   ```bash
   npx projen test
   ```

## API Reference

Detailed documentation of the available constructs, their properties, and methods is available in the [API.md](API.md) file.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) guide for more details on how to get involved.

## Security policy

Please see the [SECURITY.md](SECURITY.md) for more information.

## License

This project is licensed under the **Apache-2.0** License. See the [LICENSE](LICENSE) file for more information.
