Pigrate
=======

Python製のスキーママイグレーションツール


インストール
-----------

#### ソースコードからのインストール

```sh
git clone git@github.com:eiiches/pigrate.git pigrate
cd pigrate
sudo python setup.py install
```

#### パッケージマネージャによるインストール

```sh
sudo pip install pigrate
```

チュートリアル
--------------

### 初期設定

まず、プロジェクトのディレクトリで下記のコマンドを実行します。

```sh
pigrate init
```

これにより、schemaディレクトリとschema/config.pyが作成されます。
自動的にschema/config.pyを編集するためのエディタが起動するので、データベースへの接続情報を編集してください。

起動するエディタは`EDITOR`環境変数によって変更できます。設定されていない場合は、viが使用されます。

#### 設定例 (SQLite3)

```python
from pigrate import config, driver

def configure(env):
    if env == 'local':
        return config({
            'default': driver.sqlite3(db="sqlite3.db"),
        })
```

#### 設定例 (MySQL)

```python
from pigrate import config, driver

def configure(env):
    if env == 'local':
        return config({
            'default': driver.mysql(host='localhost', port=3306,
                                    db='foo',
                                    user='user', passwd='passwd'),
        })
```

上記の設定では、'default'という名前でデータベースを登録していますが、これは自由に変更できます。また、複数のデータベースを登録することもできます。
次の節でマイグレーションスクリプトを作成しますが、その中でここで設定した名前でデータベースを指定することになります。

#### 環境ごとの設定

開発、ステージング、本番など、複数の環境がある場合は、以下のように、`env`変数での条件分岐を追加することで、環境ごとに異なった接続先などを設定できます。

```python
from pigrate import config, driver

def configure(env):
    if env == 'local':
        return config({
            'default': driver.mysql(host="localhost", db="foo",
                                    user="user", passwd="passwd"),
        })
    if env == 'product':
        return config({
            'default': driver.mysql(host="db01.example.com", db="foo",
                                    user="user", passwd="passwd"),
        })
```

また、アプリケーション側で使用している環境設定ファイルがある場合は、ここでそのファイルを読み込むようにすると設定をメンテナンスする手間を軽減できます。


### マイグレーションスクリプトの作成

新しく`user`テーブルを追加してみましょう。下記のコマンドを実行してください。

```sh
pigrate new create-table-user
```

newコマンドの引数には、マイグレーションの内容を表す分かりやすい文字列を指定してください。これは、statusコマンドの表示や、ファイル名の一部として使われます。どのような文字列でも問題ありませんが、命名規則としてはハイフン区切りの小文字ケースを推奨しています。

initコマンドと同じように、自動的にエディタが起動するため、ここでマイグレーションの内容を編集します。`target`変数にはマイグレーションの適用対象となるデータベース名を指定します。また、`up`, `down`にはそれぞれマイグレーションで実行するSQL文、マイグレーションを巻き戻す時に実行するSQL文を指定します。複数の文を実行する場合は、';' (セミコロン)もしくは、`delimiter`変数を設定し、その値で区切って入力してください。

```python
target = 'default'

up = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT NOT NULL
    );
"""

down = """
    DROP TABLE IF EXISTS user;
"""
```

エディタを終了したあと再び内容を変更したい場合は、schema/{timestamp}-create-table-user.pigrate.py を編集してください。{timestamp}は、マイグレーションを作成した時間のUnixミリ秒(UTC)です。


### 現在のマイグレーション実行状態の確認

```sh
pigrate status
```


### マイグレーションの実行

はじめに、現在の状態を確認します。

```sh
pigrate status
# Id            | File                                       | Status
# --------------+--------------------------------------------+--------
# 1396297185976 | 1396297185976-create-table-user.pigrate.py | pending
```

実際にマイグレーションを実行します。statusがpendingになっているものがすべて適用されます。

```sh
pigrate up -i
```

最後に、正しくマイグレーションが適用されているか、再度確認します。

```sh
pigrate status
# Id            | File                                       | Status
# --------------+--------------------------------------------+-------------------------
# 1396297185976 | 1396297185976-create-table-user.pigrate.py | applied to 'default'(ok)
```

初回の実行の時は、マイグレーション状態の管理のための`_pig_status`テーブルを作成して良いか聞かれますので、yと答えてください。


### マイグレーションの巻き戻し

マイグレーションを実行したときと同じように、statusコマンドで状態を確認し、以下のコマンドで最後に実行したマイグレーションを1つ巻き戻します。

```sh
pigrate down -i
```

また、すべてのマイグレーションを巻き戻したあと、さらにもう一度上記のコマンドを実行すると、マイグレーション状態の管理のための`_pig_status`テーブルを削除することができます。


ライセンス
---------

このソフトウェアは、MITライセンスのもとで公開されています。LICENSE.txtを参照してください。

