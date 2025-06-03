# AI Shorts Factory

## プロジェクト概要
生成AIを活用して、YouTube Shorts を自動生成・投稿するパイプラインです。  
GitHub Actions と各種 API（OpenAI, ElevenLabs, YouTube Data API など）を組み合わせ、**1 日 1 本の動画を全自動で公開**することを目指します。

## ディレクトリ構成
├── src/
│ └── main.py # 生成パイプライン本体
├── requirements.txt # Python 依存ライブラリ
└── .github/
└── workflows/
└── pipeline.yml # GitHub Actions ワークフロー


## セットアップ手順
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `.env` に API キーを設定（詳細は「環境変数」セクション参照）
4. `python src/main.py` でローカル実行テスト
5. GitHub Secrets に同名のキーを登録し、Actions を動かす

## 環境変数
| 変数名 | 説明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI API キー |
| `YT_OAUTH_JSON` | base64 エンコードした OAuth 認証情報 |
| `ELEVENLABS_API_KEY` | ElevenLabs API キー |

## ライセンス
MIT License
