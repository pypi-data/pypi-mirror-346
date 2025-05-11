# ScriptSmith

ScriptSmith is an open-source Python tool designed to automate the creation and management of tasks using Amazon Q and Supabase. It leverages natural language prompts to generate scripts that can be scheduled and managed directly from your command line. With an easy-to-use CLI, you can interact with Amazon Q, create tasks, and view logs of script executions.

## Features

- **Task Creation**: Create and manage tasks with natural language descriptions.
- **Task Scheduling**: Schedule tasks using cron syntax for automation.
- **Amazon Q Integration**: Use Amazon Q to generate scripts based on task descriptions.
- **Log Management**: Store logs of task executions and generated scripts in Supabase.
- **Interactive Setup**: Easily configure Supabase database and Amazon Q Builder ID.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Setup ScriptSmith](#setup-scriptsmith)
  - [Create a Task](#create-a-task)
  - [List Tasks](#list-tasks)
  - [Run a Task](#run-a-task)
- [Configuration](#configuration)
- [Development](#development)
- [License](#license)

## Installation

### Install via `pip`

To install **ScriptSmith** via `pip`, run the following command:

```bash
pip install scriptsmith
```

### Prerequisites

Before using **ScriptSmith**, ensure that you have the following prerequisites:

- **macOS Users**: If you're on macOS, **ScriptSmith** will automatically attempt to install **Amazon Q CLI** via Homebrew. Ensure Homebrew is installed:

  ```bash
  brew install amazon-q
  ```

- **Windows Users**: On Windows, you will be prompted to manually download and install the Amazon Q Developer tool if it's not already installed. Follow the on-screen instructions for installation.

---

## Usage

After installation, you can use **ScriptSmith** directly from the command line.

### Setup ScriptSmith

To configure **ScriptSmith**, run the setup command, which will prompt you to enter your Supabase credentials and Amazon Q Builder ID:

```bash
scriptsmith setup
```

You will need to provide the following information during setup:
- **Supabase URL**: The URL of your Supabase project.
- **Supabase Key**: The key to authenticate with Supabase.
- **Amazon Q Builder ID**: Your Amazon Q Builder ID for script generation.

### Create a Task

To create a new task, use the `create-task` command with a natural language description. You can optionally add a cron schedule:

```bash
scriptsmith create-task "Description of the task" --schedule "0 0 * * *"
```

The `--schedule` option is optional, and you can specify a cron schedule to automate the task. If no schedule is provided, the task is created without one.

### List Tasks

To list all tasks in your Supabase database, run:

```bash
scriptsmith list-tasks
```

This will display all tasks along with their ID, description, and any scheduled time.

### Run a Task

To run a task by its ID, use the `run-task` command:

```bash
scriptsmith run-task <task_id>
```

This will send the task description to Amazon Q, where it will generate a script based on the task description. The generated script will be logged, and the result will be shown in your terminal.

---

## Configuration

### Environment Variables

For **ScriptSmith** to work, you need to configure the following environment variables in a `.env` file:

```env
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_key>
AMAZON_Q_BUILDER_ID=<your_amazon_q_builder_id>
```

### Configuring ScriptSmith

You can always reconfigure **ScriptSmith** by running:

```bash
scriptsmith setup
```

This will prompt you to enter your credentials again and reconfigure your environment.

---

## Development

If you want to contribute to **ScriptSmith** or modify the code, follow these steps:

### Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/scriptsmith.git
cd scriptsmith
```

### Install Development Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Tests

To ensure everything works as expected, you can run the tests using `pytest`:

```bash
pytest
```

### Build the Package

If you're ready to release a new version, build the package using:

```bash
python setup.py sdist bdist_wheel
```

### Upload to PyPI

To upload the package to PyPI, use `twine`:

```bash
twine upload dist/*
```

Make sure you have the correct credentials for PyPI before uploading.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

We welcome contributions! If you'd like to contribute, open an issue or submit a pull request. Before submitting a pull request, please ensure you've followed the development guidelines and run the tests.

---
