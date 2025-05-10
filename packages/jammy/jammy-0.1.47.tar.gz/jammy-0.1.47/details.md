# Setup

```
shell
git clone https://gitlab.com/zqsh419/jam.git --recursive $HOME/jam
export PATH=$HOME/jam/bin:$PATH
```

## install uv

```shell
curl -sSL https://astral.sh/uv/install.sh | sh

# create a virtual environment
uv venv

# activate the virtual environment
source .venv/bin/activate

# Install the package with all optional dependencies
uv pip install -e ".[all]"
```

## publish to pypi manually

```shell
uv build
uv publish --token $PYPI_TOKEN
```