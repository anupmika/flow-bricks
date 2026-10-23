# flow-bricks

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/anupmika/flow-bricks/main.svg)](https://results.pre-commit.ci/latest/github/anupmika/flow-bricks/main)
[![Quality gate status](https://sonarcloud.io/api/project_badges/measure?project=anupmika_flow-bricks&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=anupmika_flow-bricks)

Data Engineering Pipeline Manager with Databricks API Integration

## Description

flow-bricks is a Streamlit application that provides a simple interface for uploading a file to a Databricks Volume, triggering an existing Databricks job, monitoring the job run, and downloading the processed result.

The current implementation uses a fixed job ID, volume path, and output path. Update these values in `src/app.py` to match your Databricks workspace before running the application.

## Features

- **File Upload**: Upload a local file through the Streamlit interface
- **Databricks Authentication**: Connect with a workspace host URL and access token
- **Job Execution**: Trigger an existing Databricks job with input and output paths
- **Run Monitoring**: Poll the job lifecycle state until it completes or times out
- **Result Download**: Download the processed file produced by the Databricks job
- **Streamlit Interface**: Use a browser-based workflow without managing a separate API client

## Installation

### Prerequisites

- Python 3.12 or higher
- Access to a Databricks workspace
- A Databricks personal access token (PAT) or service principal token
- Permission to read from and write to the target Databricks Volume
- An existing Databricks job configured to process the uploaded file

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/anupmika/flow-bricks.git
   cd flow-bricks
   ```

2. **Create and activate a virtual environment:**

   Linux or macOS:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install the project dependencies:**

   ```bash
   pip install -e .
   ```

4. **Configure the application:**

   Update the following values in `src/app.py` for your environment:

   - `job_id`: the Databricks job to run
   - `base_path`: the Databricks Volume path used for input and output files
   - `output_path`: the path where the job writes its result

   The application collects the workspace host and token in the Streamlit form. Never commit credentials to the repository.

## Usage

1. **Run the application:**

   ```bash
   streamlit run src/app.py
   ```

2. **Open your browser** at the URL displayed in the terminal, typically `http://localhost:8501`.

3. **Enter your Databricks credentials** and upload a file.

4. **Submit the form** to upload the file, start the configured job, and monitor its status.

5. **Download the processed file** when the job completes successfully.

## Configuration

| Setting | Location | Purpose |
| --- | --- | --- |
| Databricks host | Streamlit form | Workspace endpoint used by the SDK |
| Access token | Streamlit form | Authenticates requests to Databricks |
| Job ID | `src/app.py` | Identifies the existing job to run |
| Volume path | `src/app.py` | Stores the uploaded input and processed output |
| Polling timeout | `src/app.py` | Limits how long the application waits for the job |

## Development

### Set Up the Development Environment

1. **Install and enable pre-commit:**

   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Run all configured checks:**

   ```bash
   pre-commit run --all-files
   ```

### Project Structure

```tree
flow-bricks/
├── src/                    # Application source code
│   └── app.py              # Streamlit and Databricks workflow
├── .streamlit/             # Streamlit configuration
├── .github/                # GitHub Actions and templates
├── test/                   # Test files (when available)
├── pyproject.toml          # Project metadata and dependencies
└── README.md               # Project documentation
```

## Contributing

We welcome contributions. Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and run the available checks.
4. Commit your changes: `git commit -m 'Add your feature'`
5. Push the branch: `git push origin feature/your-feature`
6. Submit a pull request.

### Development Guidelines

- Follow PEP 8 style guidelines.
- Add tests for new behavior when the test suite is available.
- Update this documentation when configuration or behavior changes.
- Ensure all pre-commit checks pass before submitting a pull request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or contributions:

- Open an issue on GitHub.
- Review the [Databricks SDK for Python documentation](https://docs.databricks.com/dev-tools/sdk-python.html).
- Review the [Streamlit documentation](https://docs.streamlit.io/).

## Roadmap

- [ ] Advanced pipeline visualization
- [ ] Real-time monitoring dashboards
- [ ] Integration with other data platforms
- [ ] API endpoints for external integrations
- [ ] Multi-workspace support
