import requests,json,os
from score import *
from Generater import *

def dataSetup(UID=826487438,character_count=0,TYPE="攻撃力"):
  def get_element_name(element_id):
    elements = {"Fire": "炎", "Water": "水", "Wind": "風", "Electric": "雷","Rock": "岩", "Ice": "氷", "Grass": "草"}
    return elements.get(element_id, "Unknown Element")
  with open("loc.json", "r", encoding="utf-8") as j: content = json.loads(j.read())
  with open("characters.json", "r", encoding="utf-8") as c: chara_data = json.loads(c.read())
  data = requests.get(f"https://enka.network/api/uid/{UID}").json()
  Chara = requests.get("https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/characters.json").json()
  result = artifact_Calculation(character_count=character_count,TYPE=TYPE,base=data)
  chara = data['avatarInfoList'][character_count]
  constellation = chara.get("talentIdList", [])
  avatarId = data["playerInfo"]["showAvatarInfoList"][character_count]["avatarId"]
  characterName = content["ja"][f'{chara_data[f"{avatarId}"]["NameTextMapHash"]}']
  element = Chara[f"{avatarId}"]["Element"]
  element_name = get_element_name(element)
  buf = 1
  fight_prop_keys = ["30", "40", "41", "42", "43", "44", "45", "46"]
  for key in fight_prop_keys:
    if round(chara["fightPropMap"][key] * 100) > 0:
      buf += round(chara["fightPropMap"][key]*100,1) - 1
      break
  gifts = []
  for talent in chara["skillLevelMap"].values():
    gifts.append(talent)
  if "proudSkillExtraLevelMap" in chara:
    for idx, _ in enumerate(chara["proudSkillExtraLevelMap"].values(), start=1):
      gifts[idx] += 3
      if idx >= 2:
        break
  else:
    pass

  weapon = chara["equipList"][5]["flat"]
  parent_dict = chara["equipList"][5]["weapon"]["affixMap"]
  if parent_dict: key, weapon_rate = next(iter(parent_dict.items()))
  else: weapon_rate = 0
  weapon_rate += 1

  output_json = {
    "uid": UID,
    "name": data["playerInfo"]["nickname"],
    "achieve": data["playerInfo"]["finishAchievementNum"],
    "level": data["playerInfo"]["level"],
    "Character": {
      "Name": characterName,
      "Const": len(constellation),
      "Level": data["playerInfo"]["showAvatarInfoList"][character_count]["level"],
      "Love": chara["fetterInfo"]["expLevel"],
      "Status": {
        "HP": round(chara["fightPropMap"]["2000"],1),
        "攻撃力": round(chara["fightPropMap"]["2001"],1),
        "防御力": round(chara["fightPropMap"]["2002"],1),
        "元素熟知": round(chara["fightPropMap"]["28"]),
        "会心率": round(chara["fightPropMap"]["20"] * 100,1),
        "会心ダメージ": round(chara["fightPropMap"]["22"] * 100,1),
        "元素チャージ効率": round(chara["fightPropMap"]["23"] * 100,1),
        f"{element_name}元素ダメージ": round(buf,1)
      },
      "Talent": {
        "通常": gifts[0],
        "スキル": gifts[1],
        "爆発": gifts[2],
      },
      "Base":{
        "HP": round(chara["fightPropMap"]["1"],1),
        "攻撃力": round(chara["fightPropMap"]["4"],1),
        "防御力": round(chara["fightPropMap"]["7"],1)
      },
    },
    "Weapon": {
      "name": content["ja"][f"{weapon['nameTextMapHash']}"],
      "Level": chara["equipList"][5]["weapon"]["level"],
      "totu": weapon_rate,
      "rarelity": weapon["rankLevel"],
      "BaseATK": weapon["weaponStats"][0]["statValue"],
      "Sub": {
        "name": content["ja"][weapon["weaponStats"][1]["appendPropId"]],
        "value": weapon["weaponStats"][1]["statValue"]
      }
    },
    "Score": {
      "State": result["State"],
      "total": round(result["total"],1),
      "flower": round(result["flower"],1),
      "wing": round(result["wing"],1),
      "clock": round(result["clock"],1),
      "cup": round(result["cup"],1),
      "crown": round(result["crown"],1)
    },
    "Artifacts": result["Artifacts"],
    "元素": element_name
  }
  return output_json

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
  result = dataSetup(UID=UID,TYPE="元素熟知")
  print(result)
  update_json_file(file_path, result)
  generation(read_json('data.json'))
