# Genshin-create-json

Genshin ArtifacterのGenerater.pyで使用されているdata.jsonを上書きし、新しいデータを導入して画像を生成します。このリポジトリのファイルは全てGenerater.pyと同じ階層に配置してください。
<div>2時間で書いたのでコード汚いです<br>
2023/11/21 16:07</div>

## 使用方法

1. Generater.pyの一部を削除します。以下のコードを削除してください。

   ```python
   # 559行
   Base.show()
   Base.save(f'{cwd}/Tests/Image.png')

   # 583行
   generation(read_json('data.json'))
   ```

2. 関数呼び出し
   ```python
   import json,os
   from main import *
   from Generater import *

   if __name__ == "__main__":
    def update_json_file(file_path, new_data):
      if os.path.exists(file_path):
        try:
          with open(file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
        except json.decoder.JSONDecodeError:
          existing_data = {}
      else:
        existing_data = {}
      existing_data.update(new_data)
      with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=2)

    file_path = 'data.json'
    UID = 826487438
    result = dataSetup(UID=UID)
    update_json_file(file_path, result)
    generation(read_json('data.json'))
   ```


   <img src="image.png">
