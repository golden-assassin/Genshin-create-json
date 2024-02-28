const E = "元素ダメージ", P = "パーセンテージ", F = "FIGHT_PROP_", A = "_ADD_HURT";
const prop_to_japanese = {[`${F}HP_PERCENT`]: `HP${P}`,[`${F}ATTACK_PERCENT`]: `攻撃${P}`,[`${F}DEFENSE_PERCENT`]: `防御${P}`,[`${F}ELEMENT_MASTERY`]: "元素熟知",[`${F}HP`]: "HP",[`${F}ATTACK`]: "攻撃力",[`${F}DEFENSE`]: "防御力",[`${F}CRITICAL_HURT`]: "会心ダメージ",[`${F}CRITICAL`]: "会心率",[`${F}CHARGE_EFFICIENCY`]: "元素チャージ効率",[`${F}HEAL_ADD`]: "与える治癒効果",[`${F}PHYSICAL${A}`]: "物理ダメージ",[`${F}FIRE${A}`]: `炎${E}`,[`${F}ELEC${A}`]: `雷${E}`,[`${F}WATER${A}`]: `水${E}`,[`${F}WIND${A}`]: `風${E}`,[`${F}ICE${A}`]: `氷${E}`,[`${F}ROCK${A}`]: `岩${E}`,[`${F}GRASS${A}`]: `草${E}`};

async function request(uid) {
  const host = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store";
  try {
    const userResponse = await fetch(`https://enka.network/api/uid/${uid}`);
    const user = await userResponse.json();
    const locResponse = await fetch(`${host}/loc.json`);
    const loc = await locResponse.json();
    const charactersResponse = await fetch(`${host}/characters.json`);
    const characters = await charactersResponse.json();
    return [user, characters, loc];
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
}

function get_element_name(element_id) {
  const elements = {"Fire": "炎","Water": "水","Wind": "風","Electric": "雷","Rock": "岩","Ice": "氷","Grass": "草"};
  return elements[element_id];
}

async function dataSetup(UID,count=0,TYPE="攻撃力") {
  const response = await request(UID);
  if (!response) return null;
  const [user, character, loc] = response;
  const result = artifact_Calculation(count, TYPE, user, loc);
  const user_character = user.avatarInfoList[count];
  const constellation = user_character.talentIdList || [];
  const avatarId = user.playerInfo.showAvatarInfoList[count].avatarId;
  const element_name = get_element_name(character[avatarId.toString()].Element);
  const fightPropMap = user_character.fightPropMap;

  let buf = 0;
  const fight_prop_keys = ["30", "40", "41", "42", "43", "44", "45", "46"];
  for (const key of fight_prop_keys) {
    const x100 = fightPropMap[key] * 100;
    if (x100 > 0) {
      buf += x100;
      break;
    }
  }

  const talent = [];
  const talents = Object.values(user_character.skillLevelMap);
  for (const tal of talents) talent.push(tal);
  if (talents.length > 3) talent.splice(2, 1);

  if (user_character.proudSkillExtraLevelMap) {
    let idx = 1;
    for (const _ of Object.values(user_character.proudSkillExtraLevelMap)) {
      talent[idx] += 3;
      if (idx >= 2) break;
      idx++;
    }
  }

  const weapon = user_character.equipList[5].flat;
  const parent_dict = user_character.equipList[5].weapon.affixMap;
  let weapon_rate = parent_dict ? parent_dict[Object.keys(parent_dict)[0]] + 1 : 1;

  const UI_Name = character[avatarId.toString()].SideIconName.replace("UI_AvatarIcon_Side_", "");
  const UI_Gacha = "UI_Gacha_AvatarImg_" + UI_Name;

  const output_json = {
    uid: UID,
    name: user.playerInfo.nickname,
    level: user.playerInfo.level,
    Character: {
      Name: loc.ja[character[avatarId.toString()].NameTextMapHash.toString()],
      Const: constellation.length,
      Level: user.playerInfo.showAvatarInfoList[count].level,
      Love: user_character.fetterInfo.expLevel,
      Status: {
        HP: Math.round(fightPropMap["2000"]),
        攻撃力: Math.round(fightPropMap["2001"]),
        防御力: Math.round(fightPropMap["2002"]),
        元素熟知: Math.round(fightPropMap["28"]),
        会心率: parseFloat((fightPropMap["20"] * 100).toFixed(1)),
        会心ダメージ: parseFloat((fightPropMap["22"] * 100).toFixed(1)),
        元素チャージ効率: parseFloat((fightPropMap["23"] * 100).toFixed(1)),
        [`${element_name}元素ダメージ`]: parseFloat(buf.toFixed(1))
      },
      Talent: {
        通常: talent[0],
        スキル: talent[1],
        爆発: talent[2]
      },
      Base: {
        HP: parseInt(fightPropMap["1"]),
        攻撃力: parseInt(fightPropMap["4"]),
        防御力: parseInt(fightPropMap["7"])
      }
    },
    Weapon: {
      name: loc.ja[weapon.nameTextMapHash.toString()],
      Level: user_character.equipList[5].weapon.level,
      totu: weapon_rate,
      rarelity: weapon.rankLevel,
      BaseATK: weapon.weaponStats[0].statValue,
      Sub: {
        name: loc.ja[weapon.weaponStats[1].appendPropId],
        value: weapon.weaponStats[1].statValue
      }
    },
    Score: {
      State: result.State,
      total: parseFloat(result.total.toFixed(1)),
      flower: parseFloat(result.flower.toFixed(1)),
      wing: parseFloat(result.wing.toFixed(1)),
      clock: parseFloat(result.clock.toFixed(1)),
      cup: parseFloat(result.cup.toFixed(1)),
      crown: parseFloat(result.crown.toFixed(1))
    },
    Artifacts: result.Artifacts,
    元素: element_name,
    UI: {
      UI_weapon: weapon.icon,
      avatarId: avatarId,
      UI_Name: UI_Name,
      UI_Gacha: UI_Gacha
    }
  };
  return output_json;
}
function artifact_Calculation(count,TYPE,user=null,loc=null) {
  if (user && user.avatarInfoList && user.avatarInfoList.length > 0) {
    const first_avatar_info = user.avatarInfoList[count];
    if (first_avatar_info.equipList) {
      const Info = first_avatar_info.equipList;
      if (Info.length > 0) {
        let flower = 0, wing = 0, clock = 0, cup = 0, crown = 0;
        let score = 0, Total = 0;
        const result_json = {};
        const mainlist = [], receipt = [];
        for (let p = 0; p < 5; p++) {
          const sublist = [];
          for (let i = 0; i < 4; i++) {
            if (p < Info.length && Info[p].flat && Info[p].flat.reliquarySubstats && i < Info[p].flat.reliquarySubstats.length) {
              const artifact = Info[p].flat.reliquarySubstats[i];
              const statValue = parseFloat(artifact.statValue);
              const converted_value = Math.round(statValue * 10) / 10;
              const value = Number.isInteger(converted_value) ? parseInt(converted_value) : converted_value;
              const part = artifact.appendPropId;
              if (part === `${F}CRITICAL_HURT`) score += value;
              if (part === `${F}CRITICAL`) score += value * 2;
              if (TYPE === "HP" && part === `${F}HP_PERCENT`) score += value;
              if (TYPE === "攻撃力" && part === `${F}ATTACK_PERCENT`) score += value;
              if (TYPE === "防御力" && part === `${F}DEFENSE_PERCENT`) score += value;
              if (TYPE === "元素チャージ効率" && part === `${F}CHARGE_EFFICIENCY`) score += value;
              if (TYPE === "元素熟知" && part === `${F}ELEMENT_MASTERY`) score += value * 0.25;
              if (p === 0) flower += score;
              if (p === 1) wing += score;
              if (p === 2) clock += score;
              if (p === 3) cup += score;
              if (p === 4) crown += score;
              score = 0;
              const sub_ja_name = prop_to_japanese[part] || "";
              sublist.push({
                option: sub_ja_name,
                value: value,
              });
            } else continue;
          }
          receipt.push(sublist);
          const reliquary = Info[p].flat.reliquaryMainstat;
          const main_ja_name = prop_to_japanese[reliquary.mainPropId] || "";
          mainlist.push({ option: main_ja_name, value: reliquary.statValue });
          const artifactID = Info[p].flat.setNameTextMapHash;
          const parts = ["flower", "wing", "clock", "cup", "crown"]
          const current_json = {
            [parts[p]]: {
              icon: Info[p].flat.icon,
              type: loc.ja[String(artifactID)],
              Level: Info[p].reliquary.level - 1,
              rarelity: Info[p].flat.rankLevel,
              main: mainlist[p],
              sub: receipt[p]
            }
          };
          Object.assign(result_json, current_json);
        }
        const result_json_str = JSON.stringify(result_json, null, 2);
        const result_json_object = JSON.parse(result_json_str);
        Total += (flower + wing + clock + cup + crown);
        const result = {
          State: TYPE,
          total: Total,
          flower: flower,
          wing: wing,
          clock: clock,
          cup: cup,
          crown: crown,
          Artifacts: result_json_object
        };
        return result;
      }
    }
  }
}

function create(uid=null,count=0,TYPE="攻撃力") {
  if (uid===null) return null;
  return dataSetup(uid,count,TYPE).then((data) => {
    console.log('data:',data);
    return data;
  }).catch((error) => {
    console.log('error:',error)
    return error;
  });
}
// create(uid=826487438,count=1,TYPE="HP");
