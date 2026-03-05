## Jesus - docs

1. Create a Python venv

```bash
    python -m venv venv
```

2. Activate the venv

```bash
    venv\Scripts\activate
```

3. Install the requirements

```Bash
    pip install -r requirements.txt
```

4. Run App

```bash
    python main.py
```

## Target Architecture

```bash
    Client
    │
    ▼
    Flask Gateway
    │
    ├─ /deploy   → upload function
    └─ /invoke   → run function
            │
            ▼
    Function Registry
            │
            ▼
    Docker Runtime
            │
            ▼
    Function Container
```