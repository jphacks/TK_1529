# 共同開発マイニング
## 組織と組織のつながりを可視化します

### 製品説明
テキストから組織と組織の共同開発の関係を自動抽出し、グラフとして可視化します。
ブラウザを通して、共同開発の情報をインタラクティブに探索することができます。
### 特長
####1. 直感的に "つながり" を可視化する
やることは、任意の組織名(企業、大学、研究室等)を入力して、検索ボタンを押すだけ。その組織の "つながり" を直感的な体裁で可視化する。
####2. "つながり" の中身も掘り起こす
"つながり" の線上の点にマウスポインタをドラッグすれば、組織と組織がどのような "つながり" を持っているか、その詳細を知ることができる。
####3. "つながり" が "つながり" を呼ぶ
"つながり" の可視化によって、新たに表示された組織をダブルクリックすれば、その組織の "つながり"も表示される。さらなる "つながり" を連鎖的に把握することが可能。

### 解決出来ること
"つながり" を可視化することによって、日に日に複雑化していく現代社会をシンプルな像で新たに捉え直すことができる。
### 今後の展望
 "組織" のつながりのみならず、 "人" のつながり、"国" のつながり、といったように様々なつながりを可視化することです。
### 注力したこと（こだわり等）
* シンプルで直感的なインターフェース
* wikipediaのリダイレクト辞書を利用することで、略称でも検索可能 

## 開発技術
### 活用した技術
#### API・データ
* 日本語Wikipedia全記事・カテゴリ情報・リダイレクト情報
* Wikimedia API

#### フレームワーク・ライブラリ・モジュール
* D3.js
* python

#### デバイス
* PC用ブラウザ

### 独自技術
#### ハッカソンで開発した独自機能・技術
* Wikipedia記事からの情報抽出
* https://github.com/jphacks/TK_29/blob/master/ie/extract.py
