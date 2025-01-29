# sanpi-check

`sanpi-check` は、特定のトピックに対する賛成意見と反対意見を生成し、それらを集約してひとつの見解を出力する、LangChainとOllamaを用いた練習用のプロジェクトです。

## 概要

このプロジェクトは、以下のステップで構成されています。

1. **賛成意見の生成**: 与えられたトピックに対して、賛成の立場から意見を生成します。
2. **反対意見の生成**: 同じトピックに対して、反対の立場から意見を生成します。
3. **意見の集約**: 賛成意見と反対意見を統合し、それらを踏まえた上での最終的な見解を出力します。

これらの処理は、LangChainの `RunnableParallel` を用いて並列化されており、効率的に実行されます。また、`ChatOllama` を使用して、ローカルで動作するOllamaの言語モデルを活用しています。

## 使い方

### 前提条件

* Python 3.8以上
* Rye（パッケージと環境の管理に使用）
* Ollamaがインストールされ、適切なモデルが利用可能であること（デフォルトでは `qwen2.5:14b` を想定）

### セットアップ

1. リポジトリをクローンします:

```bash
git clone https://github.com/rmc8/sanpi_check.git
cd sanpi_check
```

2. `.env` ファイルを作成し、必要な環境変数を設定します。

```
OLLAMA_MODEL="qwen2.5:14b"
OLLAMA_BASE_URL="http://localhost:11434"
```

* `OLLAMA_MODEL`: 使用するOllamaのモデル名。
* `OLLAMA_BASE_URL`: OllamaのベースURL (デフォルトは `http://localhost:11434`)。

3. Ryeを使用して依存関係をインストールし、仮想環境を同期します:

```bash
rye sync
```

### 実行

`pyproject.toml` に定義されている `start` スクリプトを使用して、`main.py` を実行します。
コマンドライン引数でクエリを渡すことで、そのトピックに対する賛否意見と集約結果を得ることができます。

```bash
rye run start -- --query "改憲についてどう思いますか？"
````

## ディレクトリ構成

```text
sanpi-check/
├── .python-version      # 使用する Python のバージョン
├── .env                 # 環境変数ファイルをつくって配置してください
├── pyproject.toml       # プロジェクトの設定ファイル（依存関係、スクリプトのショートカットなど）
├── README.md            # この説明ファイル
└── src/
    ├── main.py           # エントリーポイントとなるスクリプト（Fire を使用して CLI 化）
    └── sanpi_check/
        └── \_\_init\_\_.py    # 賛否意見の生成と集約ロジックを含むモジュール
```

## 処理の流れ

`sanpi_check` モジュール内の `Sanpi` クラスが、賛否意見の生成と集約処理を管理します。

1. `Sanpi` クラスの `run` メソッドが、ユーザーからのクエリを受け取ります。
2. `_get_agreement_template` と `_get_disagreement_template` メソッドが、それぞれ賛成意見と反対意見を生成するためのプロンプトテンプレートを取得します。
3. `RunnableParallel` を使用して、賛成意見と反対意見の生成処理を並列実行します。
4. `summarize_prompt` で定義されたプロンプトテンプレートを用いて、賛成意見と反対意見を集約する最終的な見解を生成します。

## 使用技術

* [LangChain](https://www.google.com/url?sa=E&source=gmail&q=https://www.langchain.com/): LLMを利用したアプリケーション開発のためのフレームワーク。
* [Ollama](https://www.google.com/url?sa=E&source=gmail&q=https://ollama.ai/): ローカル環境でLLMを実行するためのツール。
* [Rye](https://www.google.com/url?sa=E&source=gmail&q=https://rye-up.com/): Pythonのパッケージと環境の管理ツール。
* [python-dotenv](https://www.google.com/url?sa=E&source=gmail&q=https://pypi.org/project/python-dotenv/): `.env` ファイルから環境変数を読み込むためのライブラリ。
* [Fire](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/google/python-fire): Pythonオブジェクトからコマンドラインインターフェイス（CLI）を自動生成するライブラリ。

## ライセンス

[MIT License](LICENSE)に従います。
