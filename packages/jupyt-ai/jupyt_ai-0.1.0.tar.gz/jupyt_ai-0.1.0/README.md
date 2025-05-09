# Jupyt
Jupyt is an intelligent assistant built on top of Jupyter Notebooks. 

## Prerequisites

- Node.js >= 16
- Python >= 3.8
- JupyterLab >= 4.0
- python3-full (for Ubuntu/Debian systems)

## How to run on your system


```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
pip install jupyterlab==4.2.7
pip install -e .
(for ubuntu add --break-system-packages)

Then activate that environment in another terminal
1. In your first terminal:
```bash
# Watch for source changes and rebuild automatically
jlpm watch
```

2. In a second terminal:
```bash
# Run JupyterLab
jupyter lab
```

When you make changes to source files:
1. Save your changes
2. Wait for the rebuild message in the first terminal
3. Refresh your JupyterLab browser window

## Testing

```bash
# Run tests
jlpm test

# Run linting
jlpm lint
```

## Project Structure

FOLDER STRUCTURE:
- src: All the code files for the extension
- style: The css for the codebase
- lib: The build converted into javascript
