# 日本株テーマトラッカー

外出先からもアクセスできる日本株のテーマ別パフォーマンストラッカーです。

## 機能

- 40以上のテーマ別に日本株のパフォーマンスを追跡
- 8つの期間（1D, 5D, 10D, 1M, 2M, 3M, 6M, 12M）でデータを表示
- 各テーマの構成銘柄と要因分析（テーマ要因 vs 個別要因）
- レスポンシブデザイン（PC・スマホ対応）

## アクセス

デプロイ後、以下のURLでアクセス可能：
```
https://<ユーザー名>.github.io/<リポジトリ名>/
```

## データ更新方法

データを更新する場合：

1. ローカルで依存関係をインストール：
```bash
pip install yfinance pandas numpy
```

2. データ生成スクリプトを実行：
```bash
python3 data_generator.py
```

3. 生成された `themes_jp.json` をコミット＆プッシュ：
```bash
git add themes_jp.json
git commit -m "Update market data"
git push
```

## 自動更新について

GitHub Actionsにより、**毎日 16:30 JST (日本市場クローズ後)** に自動でデータ更新が行われる設定になっています。
設定ファイル: `.github/workflows/daily_update.yml`

⚠️ **注意**: 自動更新が動かない場合は、GitHubリポジトリの `Settings` > `Actions` > `General` > `Workflow permissions` で **"Read and write permissions"** が選択されているか確認してください。

## 技術スタック

- **フロントエンド**: React (CDN), Tailwind CSS
- **データ取得**: yfinance (Python)
- **ホスティング**: GitHub Pages
