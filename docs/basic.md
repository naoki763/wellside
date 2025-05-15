# 基本設計書

## 1. 概要

本設計書は、要件定義を基にシステムのアーキテクチャと主要コンポーネント設計、使用技術をまとめたものです。

* **システム名称**：ビジネス向けコミュニケーションツール
* **主要機能**：投稿（Xライク）、1対1チャット、グループチャット、AI分析・要約
* **対象プラットフォーム**：Web（SPA）、モバイル（将来対応予定）

## 2. アーキテクチャ概要

```plaintext
┌──────────────┐      ┌────────┐      ┌──────────┐
│  Client (Vue) │ ⇄ WebSocket/REST ⇄ │  FastAPI  │ ⇄ │  PostgreSQL │
│  - Vue.js     │      │Backend API│      │ DB         │
│  - TypeScript │      └────────┘      └──────────┘
└──────────────┘           │
                            │
                            ▼
                         ┌────────┐      ┌────────┐
                         │ Redis  │      │ AI/ML  │
                         │(Cache, │      │サービス│
                         │ Pub/Sub)│      │(OpenAI)│
                         └────────┘      └────────┘
                             │               
                             ▼
                      ┌────────────┐       
                      │  AWS S3 /  │       
                      │  CloudFront│       
                      └────────────┘       
```

## 3. 使用技術

| 分類           | 技術                                       | 用途                   |
| ------------ | ---------------------------------------- | -------------------- |
| 言語／フレームワーク   | Python, FastAPI                          | Web API              |
| ORM          | SQLAlchemy                               | DBアクセス               |
| 言語／フレームワーク   | TypeScript, Vue.js                       | フロントエンド（SPA）         |
| DB           | PostgreSQL                               | リレーショナルデータベース        |
| 認証／認可        | OAuth2 / JWT                             | トークンベース認証・認可         |
| キャッシュ／PubSub | Redis                                    | セッションキャッシュ・Pub/Sub通知 |
| メッセージング      | WebSocket / Socket.IO                    | リアルタイムチャット           |
| AI分析・要約      | OpenAI API                               | 投稿分析、要約レポート生成        |
| インフラ         | AWS (ECS, RDS, S3, ALB, CloudWatch)      | 本番環境                 |
| IaC          | Terraform                                | インフラ構成管理             |
| ローカル開発       | DevContainer, LocalStack, Docker Compose | AWSモック、開発環境構築        |
| パッケージ管理      | uv (py包管理), mise                         | Python環境管理           |
| タスク管理        | go-task                                  | 開発タスク自動化             |
| Lint／フォーマット  | ruff, Black, ESLint, Prettier            | コード品質・フォーマット         |
| 型チェック        | mypy, TypeScript                         | 静的型検査                |
| テスト          | pytest, pytest-asyncio, Vitest, Cypress  | ユニット・E2Eテスト          |
| CI/CD        | GitHub Actions / AWS CodePipeline        | 自動ビルド／デプロイ           |
| ロギング／トレーシング  | structlog / OpenTelemetry                | 構造化ログ・分散トレーシング       |
| メトリクス        | Prometheus / Grafana                     | システム監視               |
| ドキュメンテーション   | Swagger (FastAPI自動生成)                    | API仕様書               |
| Secret管理     | AWS Secrets Manager / Parameter Store    | 機密情報管理               |

## 4. コンポーネント設計

### 4.1 フロントエンド（Vue.js）

* **構成**：Vue 3 + Composition API + Vue Router + Pinia
* **主要機能**：

  * 投稿タイムライン表示
  * チャット画面（1対1／グループ）
  * 分析結果ダッシュボード
* **API連携**：Axios（JWT認証ヘッダー付き）
* **リアルタイム**：WebSocket（Socket.IO client）

### 4.2 バックエンド（FastAPI）

* **構成**：uvicorn + FastAPI
* **ルーティング**：APIRouterで機能別モジュール化
* **DBアクセス**：SQLAlchemy + Alembic（マイグレーション）
* **認証**：OAuth2 Password Flow + JWT
* **リアルタイム**：WebSocket endpoint
* **AI連携**：非同期タスクでOpenAI API呼び出し (Celery + Redis)

### 4.3 データベース（PostgreSQL）

* **テーブル例**：

  * users (id, username, email, hashed\_password, created\_at)
  * posts (id, user\_id, content, media\_urls, created\_at)
  * follows (id, follower\_id, followee\_id, created\_at)
  * messages (id, sender\_id, receiver\_id, content, created\_at)
  * group\_chats (id, name, created\_by, created\_at)
  * group\_members (id, group\_id, user\_id, joined\_at)
  * chat\_logs (id, room\_id, sender\_id, content, timestamp)
  * summaries (id, target\_type, target\_id, summary\_text, created\_at)

### 4.4 インフラ／CI/CD

* **インフラ構成**：

  * AWS ECS Fargate クラスター
  * RDS for PostgreSQL
  * S3 バケット + CloudFront
  * ALB（HTTPS）
  * CloudWatch Logs / Metrics
* **CI/CD**：GitHub Actionsで

  * Lint → Test → Build Docker → Terraform Plan/Apply → Deploy

## 5. 非機能要件対応

| 要件      | 対応技術・手法                    |
| ------- | -------------------------- |
| パフォーマンス | Redisキャッシュ、DBインデックス設計      |
| 可用性     | ECS Auto Scaling、マルチAZ RDS |
| セキュリティ  | HTTPS/TLS、WAF導入、IAM最小権限    |
| 拡張性     | マイクロサービス分割、コンテナ化           |
| 保守性     | IaC、コードLint/型チェック、自動テスト    |

---

*以上*
