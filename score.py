import json

def artifact_Calculation(count=0,TYPE="攻撃力",data=None,loc=None):
  if data is None or loc is None: return
  prop_to_japanese = {
    "FIGHT_PROP_HP_PERCENT": "HPパーセンテージ",
    "FIGHT_PROP_ATTACK_PERCENT": "攻撃パーセンテージ",
    "FIGHT_PROP_DEFENSE_PERCENT": "防御パーセンテージ",
    "FIGHT_PROP_ELEMENT_MASTERY": "元素熟知",
    "FIGHT_PROP_CRITICAL_HURT": "会心ダメージ",
    "FIGHT_PROP_CRITICAL": "会心率",
    "FIGHT_PROP_HP": "HP",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "元素チャージ効率",
    "FIGHT_PROP_ATTACK": "攻撃力",
    "FIGHT_PROP_DEFENSE": "防御力",
    "FIGHT_PROP_HEAL_ADD": "与える治癒効果",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "物理ダメージ",
    "FIGHT_PROP_FIRE_ADD_HURT": "炎元素ダメージ",
    "FIGHT_PROP_ELEC_ADD_HURT": "雷元素ダメージ",
    "FIGHT_PROP_WATER_ADD_HURT": "水元素ダメージ",
    "FIGHT_PROP_WIND_ADD_HURT": "風元素ダメージ",
    "FIGHT_PROP_ICE_ADD_HURT": "氷元素ダメージ",
    "FIGHT_PROP_ROCK_ADD_HURT": "岩元素ダメージ",
    "FIGHT_PROP_GRASS_ADD_HURT": "草元素ダメージ",
  }
  if "avatarInfoList" in data and len(data["avatarInfoList"]) > 0:
    first_avatar_info = data["avatarInfoList"][count]
    if "equipList" in first_avatar_info:
      Info = first_avatar_info["equipList"]
      if Info and len(Info) > 0:
        flower, blade, clock, cup, crown = 0, 0, 0, 0, 0
        score,Total = 0,0
        mainlist,receipt = [],[]
        for j in range(5):
          sublist = []
          for i in range(4):
            artifact = Info[j]["flat"]["reliquarySubstats"][i]
            statValue = float(artifact["statValue"])
            converted_value = round(statValue, 1)
            value = int(converted_value) if converted_value.is_integer() else converted_value
            part = artifact["appendPropId"]
            if part == "FIGHT_PROP_CRITICAL_HURT": score += value
            if part == "FIGHT_PROP_CRITICAL": score += value * 2
            if TYPE == "HP":
              if part == "FIGHT_PROP_HP_PERCENT": score += value
            if TYPE == "攻撃力":
              if part == "FIGHT_PROP_ATTACK_PERCENT":score += value
            if TYPE == "防御力":
              if part == "FIGHT_PROP_DEFENSE_PERCENT":score += value
            if TYPE == "元素熟知":
              if part == "FIGHT_PROP_ELEMENT_MASTERY":score += value * 0.25
            if j == 0: flower += score
            if j == 1: blade += score
            if j == 2: clock += score
            if j == 3: cup += score
            if j == 4: crown += score
            score = 0
            reliquary = Info[j]["flat"]["reliquaryMainstat"]
            sub_ja_name = prop_to_japanese.get(part, "")
            sublist.append({
              "option": sub_ja_name,
              "value": value,
            })
          receipt.append(sublist)
          main_ja_name = prop_to_japanese.get(reliquary["mainPropId"], "")
          mainlist.append({"option":main_ja_name,"value":reliquary["statValue"]})
        Total += (flower + blade + clock + cup + crown)
        name = ["flower","wing","clock","cup","crown"]
        result_json = {}
        for i in range(5):
          current_json = {
            name[i]: {
              "type": loc["ja"][f"{Info[i]['flat']['setNameTextMapHash']}"],
              "Level": 20,
              "rarelity": 5,
              "main": mainlist[i],
              "sub": receipt[i]
            }
          }
          result_json.update(current_json)
        result_json_str = json.dumps(result_json, indent=2)
        result_json_object = json.loads(result_json_str)
  result = {
    "State": TYPE,
    "total": Total,
    "flower": flower,
    "wing": blade,
    "clock": clock,
    "cup": cup,
    "crown": crown,
    "Artifacts": result_json_object
  }
  return result
