## Development

### Setup

1. Clone the repository

    ```sh
    git clone https://github.com/hyperdrive-eng/workback.git
    cd workback
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install in development mode:

    ```sh
    pip install -e ".[dev]"
    ```

4. Launch the application:

    ```sh
    workback
    ```

5. (Optional) Install dependencies

    ```sh
    pip install <package-name>
    ```

7. Deactivate environment

    ```sh
    deactivate
    ```

### Test

1. Navigate to the project you want to debug

    ```sh
    cd path/to/project
    ```


1. Create and activate a virtual environment:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

1. Install WorkBack in the virtual environment:

    ```sh
    pip install -e /path/to/workback
    ```



1. Deactivate the virtual environment when you're done

    ```sh
    deactivate
    ```

1. Delete the virtual environment if you no longer need it

    ```sh
    rm -rf .venv
    ```


### Publish

1. Create and activate a virtual environment:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

1. Install in development mode:

    ```sh
    pip install -e ".[dev]"
    ```

1. Build package

    ```sh
    python3 -m build
    ```

1. (Optional, but recommended) Check the distribution for common errors

    ```sh
    twine check dist/*
    ```

1. (Optional, but recommended) Publish a test release on
   [TestPyPI](https://test.pypi.org/):

    ```sh
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    ```

    You will be prompted for a TestPyPI API token.

1. (Optional, but recommended) Install test release:

    ```sh
    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ workback
    ```

1. Upload your package to PyPI

    ```sh
    twine upload dist/*
    ```

    You will be prompted for PyPI API token.

### Code Style

The project uses:

- Black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting

Run checks:

```sh
black .
isort .
mypy .
ruff .
```

