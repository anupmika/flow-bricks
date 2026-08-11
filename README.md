# flow-bricks

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/anupmika/flow-bricks/main.svg)](https://results.pre-commit.ci/latest/github/anupmika/flow-bricks/main)
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=anupmika_flow-bricks)](https://sonarcloud.io/summary/new_code?id=anupmika_flow-bricks)

Data Engineering Pipeline Manager with Databricks API Integration

## Description

flow-bricks is a Streamlit-based web application designed to simplify the management of Databricks workflows and pipelines. By integrating with the Databricks SDK, it provides data engineers and platform teams with an intuitive interface to monitor, configure, and control their data processing pipelines directly from a web browser.

## Features

- **Workflow Management**: Create, update, and monitor Databricks workflows with ease
- **Pipeline Monitoring**: Track pipeline executions, statuses, and performance metrics
- **Job Scheduling**: Configure and manage job schedules within Databricks
- **Cluster Management**: Monitor and control Databricks clusters
- **Log Access**: View logs and execution details for troubleshooting
- **User-Friendly Interface**: Clean Streamlit UI for non-technical users

## Installation

### Prerequisites

- Python 3.12 or higher
- Databricks workspace access
- Databricks personal access token(PAT) or service principal credentials

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/anupmika/flow-bricks.git
   cd flow-bricks
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -e .
   ```

4. **Configure Databricks credentials:**
   - Set environment variables:

     ```bash
     export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
     export DATABRICKS_TOKEN="your-personal-access-token"
     ```

   - Or use Databricks CLI configuration

## Usage

1. **Run the application:**

   ```bash
   streamlit run src/app.py
   ```

2. **Open your browser** to the URL displayed in the terminal (typically `http://localhost:8501`)

3. **Navigate the interface** to manage your Databricks workflows and pipelines

## Development

### Setup Development Environment

1. **Install development tools:**

   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Run linting and formatting:**

   ```bash
   pre-commit run --all-files
   ```

### Project Structure

```tree
flow-bricks/
├── src/                    # Source code
├── .streamlit/            # Streamlit configuration
├── .github/               # GitHub Actions and templates
├── tests/                 # Test files
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and run tests
4. Commit your changes: `git commit -m 'Add your feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Ensure all pre-commit checks pass

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or contributions, please:

- Open an issue on GitHub
- Check the [Databricks SDK documentation](https://docs.databricks.com/dev-tools/sdk-python.html)
- Review the [Streamlit documentation](https://docs.streamlit.io/)

## Roadmap

- [ ] Advanced pipeline visualization
- [ ] Real-time monitoring dashboards
- [ ] Integration with other data platforms
- [ ] API endpoints for external integrations
- [ ] Multi-workspace support
