import requests
from score import *

default_uid = 826487438
json_path = ["loc.json","characters.json"]

def request(uid=default_uid):
  host = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store"
  user = requests.get(f"https://enka.network/api/uid/{uid}").json()
  try:
    with open(json_path[0], 'r', encoding='utf-8') as lfile: loc = json.load(lfile)
    with open(json_path[1], 'r', encoding='utf-8') as cfile: characters = json.load(cfile)
  except:
    loc = requests.get(f"{host}/loc.json").json()
    characters = requests.get(f"{host}/characters.json").json()
  return user,characters,loc

def get_element_name(element_id):
  elements = {"Fire": "炎", "Water": "水", "Wind": "風", "Electric": "雷","Rock": "岩", "Ice": "氷", "Grass": "草"}
  return elements.get(element_id, "無")

def dataSetup(UID=826487438,count=0,TYPE="攻撃力"):
  response = request(uid=UID)
  if response:
    user, character, loc = response
  result = artifact_Calculation(count=count,TYPE=TYPE,data=user,loc=loc)
  user_character = user['avatarInfoList'][count]
  constellation = user_character.get("talentIdList", [])
  avatarId = user["playerInfo"]["showAvatarInfoList"][count]["avatarId"]
  element_name = get_element_name(character[str(avatarId)]["Element"])

  buf = 1
  fight_prop_keys = ["30", "40", "41", "42", "43", "44", "45", "46"]
  for key in fight_prop_keys:
    if round(user_character["fightPropMap"][key] * 100) > 0:
      buf += round(user_character["fightPropMap"][key] * 100,1) - 1
      break

  talent = []
  talents = user_character["skillLevelMap"].values()
  for tal in talents: talent.append(tal)
  if len(talents) > 3:
    del talent[2]

  if "proudSkillExtraLevelMap" in user_character:
    for idx, _ in enumerate(user_character["proudSkillExtraLevelMap"].values(), start=1):
      talent[idx] += 3
      if idx >= 2:
        break
  else:
    pass

  weapon = user_character["equipList"][5]["flat"]
  parent_dict = user_character["equipList"][5]["weapon"]["affixMap"]
  if parent_dict: _, weapon_rate = next(iter(parent_dict.items()))
  else: weapon_rate = 0
  weapon_rate += 1

  UI_Name = character[str(avatarId)]["SideIconName"].replace("UI_AvatarIcon_Side_", "")
  UI_Gacha = "UI_Gacha_AvatarImg_" + UI_Name

  output_json = {
    "uid": UID,
    "name": user["playerInfo"]["nickname"],
    "level": user["playerInfo"]["level"],
    "Character": {
      "UI": {
        "avatarId": avatarId,
        "UI_Name": UI_Name,
        "UI_Gacha": UI_Gacha
      },
      "Name": loc["ja"][str(character[str(avatarId)]["NameTextMapHash"])],
      "Const": len(constellation),
      "Level": user["playerInfo"]["showAvatarInfoList"][count]["level"],
      "Love": user_character["fetterInfo"]["expLevel"],
      "Status": {
        "HP": round(user_character["fightPropMap"]["2000"],1),
        "攻撃力": round(user_character["fightPropMap"]["2001"],1),
        "防御力": round(user_character["fightPropMap"]["2002"],1),
        "元素熟知": round(user_character["fightPropMap"]["28"]),
        "会心率": round(user_character["fightPropMap"]["20"] * 100,1),
        "会心ダメージ": round(user_character["fightPropMap"]["22"] * 100,1),
        "元素チャージ効率": round(user_character["fightPropMap"]["23"] * 100,1),
        f"{element_name}元素ダメージ": round(buf,1)
      },
      "Talent": {
        "通常": talent[0],
        "スキル": talent[1],
        "爆発": talent[2],
      },
      "Base":{
        "HP": round(user_character["fightPropMap"]["1"],1),
        "攻撃力": round(user_character["fightPropMap"]["4"],1),
        "防御力": round(user_character["fightPropMap"]["7"],1)
      },
    },
    "Weapon": {
      "UI_weapon": weapon["icon"] ,
      "name": loc["ja"][str(weapon["nameTextMapHash"])],
      "Level": user_character["equipList"][5]["weapon"]["level"],
      "totu": weapon_rate,
      "rarelity": weapon["rankLevel"],
      "BaseATK": weapon["weaponStats"][0]["statValue"],
      "Sub": {
        "name": loc["ja"][weapon["weaponStats"][1]["appendPropId"]],
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
