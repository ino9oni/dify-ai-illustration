
# dify-ai-illustration
ai-illustration on Dify

## TOC

- [dify-ai-illustration](#dify-ai-illustration)
  - [TOC](#toc)
  - [このページ](#このページ)
  - [背景](#背景)
  - [公式のリンク(≒NotebookLMに入れると便利)](#公式のリンクnotebooklmに入れると便利)
  - [前提](#前提)
  - [基礎知識](#基礎知識)
  - [ざっくりアーキテクチャ](#ざっくりアーキテクチャ)
  - [Plugin](#plugin)
    - [課題感](#課題感)
      - [課題の一次回避](#課題の一次回避)
      - [課題の恒久対応](#課題の恒久対応)
    - [Pluginの構造](#pluginの構造)
        - [Stable Diffusion Pluginの作成方法](#stable-diffusion-pluginの作成方法)
  - [LLM \& Agent](#llm--agent)


## このページ

DifyとLocal LLMを利用したAI画像生成のワークフローに関するカスタマイズの記録のためのページ

## 背景

- Difyが提供しているpublicなプラグインのStable Diffusioを用いて、AI画像生成を行っている
- しかし、デフォルトの状態でやりたいことができない、またはやりかたがわからないなどがあったため、備忘のため記録しておく

## 公式のリンク(≒NotebookLMに入れると便利)

- https://docs.dify.ai/ja-jp/introduction
- https://docs.dify.ai/plugin-dev-ja/0211-getting-started-dify-tool
- https://github.com/langgenius/dify/
- https://github.com/langgenius/dify-plugin-daemon

## 前提

- Windows上で実行
- docker版のDifyを利用
- localllmには、ollamaとその上で動くモデルを利用
- local画像生成にはstable diffusionを利用
- GPUはNVIDIA GeForce RTX 4070を利用
- CPUはIntel(R) Core(TM) i7-14700F、2100 Mhz、20 個のコアプロセッサ、28 個のロジカル プロセッサ
- d:\dify に git cloneしてある状態
- (dify plugin cliについても改めて記載)

## 基礎知識

- stable diffusionはautomaticのweb画面でできる内容が、一部fastapiでAPIが公開されている
    > [!WARNING]
    ただしfastapiで利用できる機能はごく一部で、WebUIからできることは部分に限定されている。（apiの引数で渡せるパラメータがUIのそれより少ない）
    > [!WARNING]
    APIのインターフェース定義に定義されていたとしても、機能しないパラメータもある
- Difyのsandboxやplugin_daemonは、実行権限や、実行環境がわけられており、セキュアに実行される仕組みになっている
    > [!WARNING]
    それにより利用できないパッケージや実行権限がないことによりファイルの書き出しやアクセスに制限がある場合がある。sandboxなどで特定のpythonコードによる処理を実行しようとすると許可されないエラー等が出る。
- DifyのpluginはWebUIから操作することでマーケットからダウンロードでき、plugin_daemonという所にインストールされる
    >[!WARNING]
    pluginをインストールした際に、UI部分のコードが固定化されてしまう。pluginの内部処理に相当する、APIのコードはdocker host側からコードのpythonを開いて修正後、コンテナを作成しなおせばすぐに利用できる。しかし。NoCodeのワークフローをデザインする画面のUIに相当するコードは直接daemon配下のコードを修正しても反映されない。pluginのコードのUI部分にはハッシュ値とバージョンがあり、そのバージョンでDBに固定されて呼び出しているらしく？、UIを変えた場合はpluginのインストールし直しが必要になるらしい？そのため公式のpluginを修正してUIごとインストールし直すというのが難しいので、独自のpluginを模倣して作成して、そちらを適宜インストールしなおしてワークフローから使うという形をとる必要がありそう。（現在試行中）

## ざっくりアーキテクチャ

＜後ほど記載＞

## Plugin

本ページで記したかった本題がこれ。
まず、公式のPluginの開発情報がかなり限定的？ではないかなと思います。

### 課題感

公式stable diffusion pluginには以下の課題がある。

- 指定できるパラメータがAPIに公開されているインターフェースより少ない
- 縦横のサイズが固定でしか渡せない（変数化不可）
- Timeoutが短く、Timeout値を延ばさないと途中で画像生成エラーになる

#### 課題の一次回避

- stable diffusionのpluginのソースを直接変更して、コンテナを作り直す
- 方法は以下
1. 以下へ移動（d:\difyはdifyをcloneしたフォルダ、@以下は各人の環境により異なる想定）
    ```powershell
    cd d:\dify\docker\volumes\plugin_daemon\cwd\langgenius\stablediffusion-0.0.2@0981eaefd440dad630d56c52ef494c921e851ffd0bd30d07baff9a4b0862a317
    ```
2. 変更すべきポイントは以下
    > aaaaa
    > bbbbbcd 
3. c
- dockerの.envを修正してTimeout値を修正する
- 方法2
1. 
2. b
3. c

#### 課題の恒久対応


### Pluginの構造

> [!NOTE]
> NotbookLMにより作成  
> 一部本人加工あり

|ファイル/ディレクトリ名|パス (例: telegraph/ プロジェクト内)|説明|
|---|---|---|
|[プラグイン名]/|./telegraph/|プラグインプロジェクトのルートディレクトリ。 すべての関連ファイルがここに配置される|
|GUIDE.md|telegraph/GUIDE.md|プロジェクト作成時に参照される、プラグイン開発に関するガイドファイル|
|requirements.txt|telegraph/requirements.txt|プラグインが依存するPythonライブラリをリストするファイル|
|_assets/|telegraph/_assets/|プラグインのアイコンファイル (icon.png, icon.svgなど) を配置するディレクトリ|
|provider/|telegraph/provider/|プラグインのプロバイダー関連設定やロジックを格納するディレクトリ|
|[プラグイン名].yaml|telegraph/provider/telegraph.yaml|プラグインのプロバイダー設定を定義。特に認証情報(credentials_for_provider) やプラグインの表示情報 (label, description, icon) を設定。|
|[プラグイン名].py|telegraph/provider/telegraph.py|ToolProviderクラスを継承し、ユーザーが提供した認証情報が有効であるかを検証する**_validate_credentialsメソッド**を実装|
|tools/|telegraph/tools/|プラグインのツール（機能）のロジックやパラメータ定義を格納するディレクトリ|
|[プラグイン名].py|telegraph/tools/telegraph.py|Toolクラスを継承し、プラグインのコアロジック（例: 外部API呼び出し）を実装する**_invokeメソッド**を含む|
|[プラグイン名].yaml|telegraph/tools/telegraph.yaml|ツールの入力パラメータ (parameters)、説明 (description - 人間ユーザー向けとLLM向けの両方)、およびツールロジックを実装するPythonファイルへのパス (extra.python.source) を定義|
|.env.example|telegraph/.env.example|環境変数のテンプレートファイルです。ローカル実行に必要な環境変数の例を記述。|
|.env|telegraph/.env|ローカルでの実行・デバッグのために、.env.exampleをコピーしてDifyインスタンスのホストとAPIキーを設定するファイル|
|main.py|telegraph/main.py|ローカルでプラグインサービスを起動するためのメインプログラムファイル|
|manifest.yaml|telegraph/manifest.yaml|プラグイン全体の「身分証明書」で、主要な表示名、全体的な概要、メインアイコン、分類タグなどを設定。Difyのプラグイン管理ページやマーケットプレイスに表示される。|
|README.md|telegraph/README.md|プラグインの詳細な紹介ページとなるファイル。機能詳細、使用例、設定ガイドなどを記述し、マーケットプレイスでユーザーに情報を提供。|
|PRIVACY.md|telegraph/PRIVACY.md|プラグインを公式マーケットプレイスに公開する場合に必要となる、プライバシーポリシーの説明ファイル|


##### Stable Diffusion Pluginの作成方法

公式情報に基づき、一部トライアンドエラーした内容も記載。

1.
```shell

```


## LLM & Agent



