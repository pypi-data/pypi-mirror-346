# Jupyt

A JupyterLab extension that adds AI capabilities to Jupyter notebooks.

## Features

- AI chat interface for asking questions and getting help
- Cell editing with AI assistance
- Theme customization
- Support for multiple AI models

## Prerequisites

* JupyterLab >= 4.0.0
* Node.js >= 18.0
* Python >= 3.8

## Installation

### Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jupyt.git
cd jupyt

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Install the dependencies and build the JupyterLab extension
jlpm install
jlpm run build
```

### User Installation

```bash
# Install the Python package
pip install jupyt
```

## Usage

1. Start JupyterLab:

```bash
jupyter lab
```

2. You should see the Jupyt panel on the right sidebar.

3. Click on the Jupyt icon to open the chat interface.

4. Use the cell toolbar buttons to interact with AI directly on notebook cells.

## Configuration

You can configure your AI model settings through the settings panel accessible from the Jupyt chat interface.

## Development

### Building the Extension

```bash
# Install dependencies
jlpm install

# Build the extension in development mode
jlpm run build

# Build the extension in production mode
jlpm run build:prod
```

### Rebuilding the Extension

If you make changes to the source code, you need to rebuild the extension:

```bash
# Clean the lib/ directory
jlpm run clean

# Build the extension
jlpm run build
```

### Watch Mode

```bash
# Watch for source code changes and rebuild automatically
jlpm run watch
```

## License

This project is licensed under the BSD-3-Clause License.
