# Genshin-create-json

Genshin ArtifacterのGenerater.pyで使用されているdata.jsonを上書きし、新しいデータを導入して画像を生成します。このライブラリのファイルは全てGenerater.pyと同じ階層に配置してください。

## 使用方法

1. Generater.pyの一部を削除します。以下のコードを削除してください。

   ```python
   # 559行
   Base.show()
   Base.save(f'{cwd}/Tests/Image.png')

   # 583行
   generation(read_json('data.json'))
   ```
