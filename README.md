# Programowanie z użyciem asyncio

## Środowisko

### Instalacja Pythona

Jeśli nie ma już zainstalowanego Pythona, to można użyć narzędzia [uv](https://docs.astral.sh/uv/)

Linux/MacOS
```commandline
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Windows
```commandline
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Utworzyć projekt, a następnie dodać wszystkie zależności.
Warto użyć najnowszej wersji Pythona, dodatkowo w wersji `freethreaded`

```commandline
> uv init my_code --python 3.14+freethreaded
> cd my_code
> uv add httpx beautifulsoup4 starlette pytest pytest-asyncio fastapi uvicorn sqlalchemy aiosqlite pydantic greenlet
```

Oraz sprawdzić:

```commandline
> uv run main.py 
Using CPython 3.14.2+freethreaded
Creating virtual environment at: .venv
Hello from test!
```
