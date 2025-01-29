import os

import fire
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from sanpi_check import Sanpi

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_PATH = os.path.join(THIS_DIR, ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)
else:
    raise FileNotFoundError(f"Environment file not found at {ENV_PATH}")


def proc(query: str):
    llm = ChatOllama(
        model=os.environ["OLLAMA_MODEL"],
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.0,
    )
    s = Sanpi(llm)
    res = s.run(query)
    print(res)


def main():
    fire.Fire(proc)


if __name__ == "__main__":
    main()
