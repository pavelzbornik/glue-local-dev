# AWS Glue Local Development Environment

This project provides a local development environment for AWS Glue using VS Code Dev Containers.

## Prerequisites

- Docker Desktop
- Visual Studio Code
- VS Code Remote - Containers extension
- AWS CLI

## Ubuntu Setup Guide

### 1. Install Docker and Configure User Permissions

Follow the guide at [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

```bash
# Create docker group if it doesn't exist
sudo groupadd docker

# Add current user to docker group
sudo usermod -aG docker $USER

# NOTE: Log out and log back in for group changes to take effect
# After logging back in, verify Docker works without sudo:
docker run hello-world
```


### 2. Install Visual Studio Code

For more info see [Visual Studio Code on Linux](https://code.visualstudio.com/docs/setup/linux)

VS Code is officially distributed as a Snap package in the Snap Store.

[Get it from the Snap Store](https://snapcraft.io/code)

You can install it by running:

```bash
sudo snap install --classic code # or code-insiders
```

Once installed, the Snap daemon takes care of automatically updating VS Code in the background. You get an in-product update notification whenever a new update is available.


### 3. Install VS Code Extensions
1. Open VS Code
2. Press `Ctrl+Shift+X` to open Extensions
3. Search and install:
   - Remote - Containers
   - Python
   - Jupyter

### 4. Configure AWS Credentials

To install for this [Installing or updating to the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

```bash
# Configure AWS credentials
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region
# - Default output format
```

### 5. System Requirements
Ensure your system meets these minimum requirements:
- 8GB RAM (16GB recommended)
- 20GB free disk space
- 4 CPU cores (8 recommended)

To check system resources:
```bash
# Check RAM
free -h

# Check disk space
df -h

# Check CPU cores
nproc
```

After completing these steps, proceed to the "Getting Started" section.

## Getting Started

1. Clone this repository
2. Open the repository in VS Code
3. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command
4. Wait for the container to build and start (this may take a few minutes)

## Features

- **AWS Glue version 4.0** environment
- Apache Spark **3.3.0-amzn-1**
- JupyterLab interface
- Python development tools
- Pre-configured VS Code settings

## Available Ports

- Spark UI: `4040`
- Spark History Server: `18080`
- Livy: `8998`
- JupyterLab: `8889`

## Usage

### Using VS Code

- Use the integrated terminal to run Glue jobs
- Debug Python scripts with VS Code's debugging tools
- Access AWS services using your local credentials

## AWS Configuration

1. Configure AWS credentials in your local `~/.aws/credentials`
2. The container will automatically mount these credentials

## Sample Code

Check `test.ipynb` for an example of:
- Setting up a Spark session
- Creating a DynamicFrame
- Basic data transformation

## Testing

### Running Tests
The project includes pytest examples for testing PySpark code. To run the tests:

```bash
pytest
```

### Example Test Cases
The `tests/test_spark_transformations.py` file demonstrates:
- Setting up PySpark test fixtures
- Testing DataFrame transformations
- Testing DataFrame filters and aggregations
- Best practices for unit testing with PySpark

Example test:
```python
def test_filter_by_department(spark, sample_data):
    filtered_df = sample_data.filter(sample_data.department == "Engineering")
    assert filtered_df.count() == 2
```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistency. A pre-commit hook is a script that runs automatically before a git commit is completed. It's part of Git's hooks system and helps maintain code quality by running checks before code changes are committed.

### Configuration Files

The pre-commit configuration consists of two main files:

1. `.pre-commit-config.yaml`: Defines the hooks and their sources
2. `pyproject.toml`: Contains Python-specific tool configurations

#### .pre-commit-config.yaml Explanation
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0  # Version of pre-commit-hooks to use
    hooks:
      - id: trailing-whitespace  # Removes trailing whitespace
      - id: end-of-file-fixer   # Ensures files end with newline
      # ...other hooks...

  - repo: https://github.com/psf/black
    rev: 23.9.1  # Version of Black to use
    hooks:
      - id: black  # Python code formatter
```

#### pyproject.toml Explanation
```toml
[tool.isort]
profile = "black"  # Makes isort compatible with Black
skip_glob = ["migrations/*"]  # Directories to skip

[tool.codespell]
skip = ["*.json","*.yaml"]  # Files to skip
builtin = "clear,rare,informal,usage,code,names"  # Dictionary types to use
ignore-words-list = "dne,iam,IAM,jupyter,master,thead"  # Words to ignore
```

### Hook Descriptions

### Code Quality Hooks
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **black**: Python code formatter
- **isort**: Sorts Python imports
- **pydocstyle**: Checks Python docstring formatting

### Security Hooks
- **detect-private-key**: Prevents committing private keys
- **check-added-large-files**: Prevents large files from being committed

### YAML Hooks
- **check-yaml**: Validates YAML syntax
- **yamllint**: Lints YAML files
- **yamlfmt**: Formats YAML files

### Other Hooks
- **codespell**: Checks for common misspellings

### Installation

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install the pre-commit hooks:
```bash
pre-commit install
```

### Running Hooks

- Hooks run automatically on `git commit`
- Run manually on all files:
```bash
pre-commit run --all-files
```

- Run a specific hook:
```bash
pre-commit run <hook-id>
```

## Troubleshooting

- If JupyterLab doesn't start, check the logs in `/tmp/postStart.out`
- Ensure Docker has sufficient resources allocated
- Verify AWS credentials are properly configured

## Python Versions

This environment includes two Python versions:

### Python 3.10.2

Available packages:

```python
Package                   Version
------------------------- --------------
aiobotocore               2.4.1
aiohappyeyeballs          2.4.3
aiohttp                   3.8.3
aioitertools              0.11.0
aiosignal                 1.3.1
anyio                     4.6.0
argon2-cffi               23.1.0
argon2-cffi-bindings      21.2.0
arrow                     1.3.0
asttokens                 2.4.1
async-lru                 2.0.4
async-timeout             4.0.2
asynctest                 0.13.0
attrs                     22.2.0
autovizwidget             0.21.0
avro-python3              1.10.2
babel                     2.16.0
beautifulsoup4            4.12.3
bleach                    6.1.0
boto                      2.49.0
boto3                     1.24.70
botocore                  1.27.59
certifi                   2021.5.30
cffi                      1.17.1
chardet                   3.0.4
charset-normalizer        2.1.1
click                     8.1.3
comm                      0.2.2
cryptography              43.0.1
cycler                    0.10.0
Cython                    0.29.32
debugpy                   1.8.6
decorator                 5.1.1
defusedxml                0.7.1
docutils                  0.17.1
enum34                    1.1.10
exceptiongroup            1.2.2
executing                 2.1.0
fastjsonschema            2.20.0
fqdn                      1.5.1
frozenlist                1.3.3
fsspec                    2021.8.1
gssapi                    1.9.0
h11                       0.14.0
hdijupyterutils           0.21.0
httpcore                  1.0.6
httpx                     0.27.2
idna                      2.10
importlib-metadata        5.0.0
iniconfig                 2.0.0
ipykernel                 6.29.5
ipython                   8.28.0
ipywidgets                8.1.5
isoduration               20.11.0
jedi                      0.19.1
Jinja2                    3.1.4
jmespath                  0.10.0
joblib                    1.0.1
json5                     0.9.25
jsonpointer               3.0.0
jsonschema                4.23.0
jsonschema-specifications 2023.12.1
jupyter                   1.1.1
jupyter_client            8.6.3
jupyter-console           6.6.3
jupyter_core              5.7.2
jupyter-events            0.10.0
jupyter-lsp               2.2.5
jupyter_server            2.14.2
jupyter_server_terminals  0.5.3
jupyterlab                4.2.5
jupyterlab_pygments       0.3.0
jupyterlab_server         2.27.3
jupyterlab_widgets        3.0.13
kaleido                   0.2.1
kiwisolver                1.4.4
krb5                      0.7.0
MarkupSafe                3.0.0
matplotlib                3.4.3
matplotlib-inline         0.1.7
mistune                   3.0.2
mpmath                    1.2.1
multidict                 6.0.4
nbclient                  0.10.0
nbconvert                 7.16.4
nbformat                  5.10.4
nest-asyncio              1.6.0
nltk                      3.7
notebook                  7.2.2
notebook_shim             0.2.4
numpy                     1.23.5
overrides                 7.7.0
packaging                 23.0
pandas                    1.5.1
pandocfilters             1.5.1
parso                     0.8.4
patsy                     0.5.1
pexpect                   4.9.0
Pillow                    9.4.0
pip                       23.0.1
platformdirs              4.3.6
plotly                    5.16.0
pluggy                    1.5.0
pmdarima                  2.0.1
prometheus_client         0.21.0
prompt_toolkit            3.0.48
psutil                    6.0.0
ptvsd                     4.3.2
ptyprocess                0.7.0
pure_eval                 0.2.3
pyarrow                   10.0.0
pycparser                 2.22
pydevd                    2.5.0
Pygments                  2.18.0
pyhocon                   0.3.58
PyMySQL                   1.0.2
pyparsing                 2.4.7
pyspnego                  0.11.1
pytest                    8.3.3
python-dateutil           2.8.2
python-json-logger        2.0.7
pytz                      2021.1
PyYAML                    6.0.1
pyzmq                     26.2.0
referencing               0.35.1
regex                     2022.10.31
requests                  2.23.0
requests-kerberos         0.15.0
rfc3339-validator         0.1.4
rfc3986-validator         0.1.1
rpds-py                   0.20.0
s3fs                      2022.11.0
s3transfer                0.6.0
scikit-learn              1.1.3
scipy                     1.9.3
seaborn                   0.12.2
Send2Trash                1.8.3
setuptools                49.1.3
six                       1.16.0
sniffio                   1.3.1
soupsieve                 2.6
sparkmagic                0.21.0
stack-data                0.6.3
statsmodels               0.13.5
subprocess32              3.5.4
sympy                     1.8
tbats                     1.1.0
tenacity                  9.0.0
terminado                 0.18.1
threadpoolctl             3.1.0
tinycss2                  1.3.0
tomli                     2.0.2
tornado                   6.4.1
tqdm                      4.64.1
traitlets                 5.14.3
types-python-dateutil     2.9.0.20241003
typing_extensions         4.12.2
uri-template              1.3.0
urllib3                   1.25.11
wcwidth                   0.2.13
webcolors                 24.8.0
webencodings              0.5.1
websocket-client          1.8.0
wheel                     0.37.0
widgetsnbextension        4.0.13
wrapt                     1.14.1
yarl                      1.8.2
zipp                      3.10.0
```

### Python 3.7.16
Available packages:

```python
Package            Version
------------------ -----------
backcall           0.2.0
debugpy            1.7.0
decorator          5.1.1
entrypoints        0.4
exceptiongroup     1.2.2
importlib-metadata 6.7.0
iniconfig          2.0.0
ipykernel          6.16.2
ipython            7.34.0
jedi               0.19.2
jupyter-client     7.4.9
jupyter-core       4.12.0
matplotlib-inline  0.1.6
nest-asyncio       1.6.0
numpy              1.21.6
packaging          24.0
pandas             1.3.5
parso              0.8.4
pexpect            4.9.0
pickleshare        0.7.5
pip                20.2.2
pluggy             1.2.0
prompt-toolkit     3.0.48
psutil             6.1.1
ptyprocess         0.7.0
pygments           2.17.2
pytest             7.4.4
python-dateutil    2.9.0.post0
pytz               2024.2
pyzmq              26.2.0
setuptools         49.1.3
six                1.17.0
tomli              2.0.1
tornado            6.2
traitlets          5.9.0
typing-extensions  4.7.1
wcwidth            0.2.13
zipp               3.15.0
```

## Related Repositories

Here are some helpful related projects for AWS Glue development:

- [Pytest for AWS Glue](https://github.com/sagadevanmi/Pytest-for-AWS-Glue) - Examples of pytest implementation for AWS Glue jobs
- [glue-libs-devcontainer](https://github.com/pippolino/glue-libs-devcontainer) - Docker development container for AWS Glue
- [glue_libs_sso](https://github.com/jerdoe/glue_libs_sso) - AWS Glue libraries with SSO support
