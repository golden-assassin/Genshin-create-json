import requests
from score import *

default_uid = 826487438

def response(uid=default_uid):
  user = requests.get(f"https://enka.network/api/uid/{uid}").json()
  characters = requests.get("https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/characters.json").json()
  loc = requests.get("https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/loc.json").json()
  return user,characters,loc

def dataSetup(UID=826487438,count=0,TYPE="攻撃力"):
  def get_element_name(element_id):
    elements = {"Fire": "炎", "Water": "水", "Wind": "風", "Electric": "雷","Rock": "岩", "Ice": "氷", "Grass": "草"}
    return elements.get(element_id, "Unknown Element")
  response_data = response(uid=UID)
  if response_data:
    d, c, loc = response_data
  result = artifact_Calculation(count=count,TYPE=TYPE,data=d,loc=loc)
  chara = d['avatarInfoList'][count]
  constellation = chara.get("talentIdList", [])
  avatarId = d["playerInfo"]["showAvatarInfoList"][count]["avatarId"]
  element = c[str(avatarId)]["Element"]
  element_name = get_element_name(element)

  buf = 1
  fight_prop_keys = ["30", "40", "41", "42", "43", "44", "45", "46"]
  for key in fight_prop_keys:
    if round(chara["fightPropMap"][key] * 100) > 0:
      buf += round(chara["fightPropMap"][key] * 100,1) - 1
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
  if parent_dict: _, weapon_rate = next(iter(parent_dict.items()))
  else: weapon_rate = 0
  weapon_rate += 1

  UI_Name = c[str(avatarId)]["SideIconName"].replace("UI_AvatarIcon_Side_", "")
  UI_Gacha = "UI_Gacha_AvatarImg_" + UI_Name

  output_json = {
    "uid": UID,
    "name": d["playerInfo"]["nickname"],
    "level": d["playerInfo"]["level"],
    "Character": {
      "UI_": {
        "avatarId": avatarId,
        "UI_Name": UI_Name,
        "UI_Gacha": UI_Gacha
      },
      "Name": loc["ja"][f'{c[str(avatarId)]["NameTextMapHash"]}'],
      "Const": len(constellation),
      "Level": d["playerInfo"]["showAvatarInfoList"][count]["level"],
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
      "UI_weapon": weapon["icon"] ,
      "name": loc["ja"][str(weapon["nameTextMapHash"])],
      "Level": chara["equipList"][5]["weapon"]["level"],
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
