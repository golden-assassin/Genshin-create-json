import json

def artifact_Calculation(count=0,TYPE="攻撃力",user=None,loc=None):
  F,E,A,P = 'FIGHT_PROP_','元素ダメージ','_ADD_HURT','パーセンテージ'
  prop_to_japanese = {
    f"{F}HP_PERCENT":f"HP{P}",
    f"{F}ATTACK_PERCENT":f"攻撃{P}",
    f"{F}DEFENSE_PERCENT":f"防御{P}",
    f"{F}ELEMENT_MASTERY":"元素熟知",
    f"{F}HP":"HP",
    f"{F}ATTACK":"攻撃力",
    f"{F}DEFENSE":"防御力",
    f"{F}CRITICAL_HURT":"会心ダメージ",
    f"{F}CRITICAL":"会心率",
    f"{F}CHARGE_EFFICIENCY":"元素チャージ効率",
    f"{F}HEAL_ADD":"与える治癒効果",
    f"{F}PHYSICAL{A}":"物理ダメージ",
    f"{F}FIRE{A}":f"炎{E}",
    f"{F}ELEC{A}":f"雷{E}",
    f"{F}WATER{A}":f"水{E}",
    f"{F}WIND{A}":f"風{E}",
    f"{F}ICE{A}":f"氷{E}",
    f"{F}ROCK{A}":f"岩{E}",
    f"{F}GRASS{A}":f"草{E}"
  }
  if "avatarInfoList" in user and len(user["avatarInfoList"]) > 0:
    first_avatar_info = user["avatarInfoList"][count]
    if "equipList" in first_avatar_info:
      Info = first_avatar_info["equipList"]
      if Info and len(Info) > 0:
        flower, wing, clock, cup, crown = 0, 0, 0, 0, 0
        score,Total = 0,0
        result_json = {}
        mainlist,receipt = [],[]
        for p,parts in enumerate(['flower',"wing","clock","cup","crown"]):
          sublist = []
          for i in range(4):
            if p < len(Info) and "flat" in Info[p] and "reliquarySubstats" in Info[p]["flat"] and i < len(Info[p]["flat"]["reliquarySubstats"]):
              artifact = Info[p]["flat"]["reliquarySubstats"][i]
              statValue = float(artifact["statValue"])
              converted_value = round(statValue, 1)
              value = int(converted_value) if converted_value.is_integer() else converted_value
              part = artifact["appendPropId"]
              if part == f"{F}CRITICAL_HURT": score += value
              if part == f"{F}CRITICAL": score += value * 2
              if TYPE == "HP" and part == f"{F}HP_PERCENT": score += value
              if TYPE == "攻撃力" and part == f"{F}ATTACK_PERCENT": score += value
              if TYPE == "防御力" and part == f"{F}DEFENSE_PERCENT": score += value
              if TYPE == "元素チャージ効率" and part == f"{F}CHARGE_EFFICIENCY": score += value
              if TYPE == "元素熟知" and part == f"{F}ELEMENT_MASTERY": score += value * 0.25
              if p == 0: flower += score
              if p == 1: wing += score
              if p == 2: clock += score
              if p == 3: cup += score
              if p == 4: crown += score
              score = 0
              reliquary = Info[p]["flat"]["reliquaryMainstat"]
              sub_ja_name = prop_to_japanese.get(part, "")
              sublist.append({
                "option": sub_ja_name,
                "value": value,
              })
            else:
              continue
          receipt.append(sublist)
          main_ja_name = prop_to_japanese.get(reliquary["mainPropId"], "")
          mainlist.append({"option":main_ja_name,"value":reliquary["statValue"]})
          artifactID = Info[p]['flat']['setNameTextMapHash']
          current_json = {
            parts: {
              "icon": Info[p]["flat"]["icon"],
              "type": loc["ja"][str(artifactID)],
              "Level":  Info[p]["reliquary"]["level"] - 1,
              "rarelity": Info[p]["flat"]["rankLevel"],
              "main": mainlist[p],
              "sub": receipt[p]
            }
          }
          result_json.update(current_json)
        result_json_str = json.dumps(result_json, indent=2)
        result_json_object = json.loads(result_json_str)
        Total += (flower + wing + clock + cup + crown)
  result = {
    "State": TYPE,
    "total": Total,
    "flower": flower,
    "wing": wing,
    "clock": clock,
    "cup": cup,
    "crown": crown,
    "Artifacts": result_json_object
  }
  return result
