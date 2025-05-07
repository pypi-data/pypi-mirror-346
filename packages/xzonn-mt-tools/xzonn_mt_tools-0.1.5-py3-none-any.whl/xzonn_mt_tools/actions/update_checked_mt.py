import json
import os

from xzonn_mt_tools.config import Config
from xzonn_mt_tools.helper import MTTranslationItem, TranslationItem, get_text_dict


def update_checked_mt(config: Config):
  with open(config.path_compared_mt, "r", -1, "utf-8") as reader:
    translation_dict: dict[str, list[MTTranslationItem]] = json.load(reader)

  checked: dict[str, dict[str, list[str]]] = {}
  try:
    with open(config.path_checked_mt, "r", -1, "utf8") as reader:
      checked = json.load(reader)
  except Exception:
    pass

  def get_sheet(sheet_name: str, ja_list: list[TranslationItem]):
    ja_dict = {item["key"]: item for item in ja_list}

    file_path = f"{config.basic_root}/{config.translation_language}/{sheet_name}.json"
    if not os.path.exists(file_path):
      return
    if sheet_name not in checked:
      checked[sheet_name] = {}

    with open(file_path, "r", -1, "utf-8") as reader:
      translation_list: list[TranslationItem] = json.load(reader)

    for item_dict in translation_list:
      key = item_dict["key"]

      if key not in ja_dict:
        continue
      ja = ja_dict[key]["original"]
      ch = item_dict["translation"]
      if ja not in translation_dict:
        if ja == ch:
          if key in checked[sheet_name]:
            del checked[sheet_name][key]
        else:
          checked[sheet_name][key] = [ch, ""]
        continue

      mt_list = list(
        map(lambda x: config.replace_new_text(sheet_name, ja_dict[key], x["chinese"]), translation_dict[ja]),
      )
      old_mt = list(
        x.replace("  \n", "\n") for x in item_dict.get("context", "").split("**翻译辅助**：\n\n", 1)[-1].rsplit("\n\n")
      )

      if mt_list[0] == ch or (len(old_mt) and old_mt[0] and old_mt[0] == ch):
        if key in checked[sheet_name]:
          del checked[sheet_name][key]
      else:
        checked[sheet_name][key] = [ch, mt_list[0]]

  ja_list = get_text_dict(f"{config.basic_root}/{config.basic_language}", config.name_filter)
  for sheet_name, sheet_data in ja_list.items():
    get_sheet(sheet_name, sheet_data)

  sorted_mt = {
    k: {k2: checked[k][k2] for k2 in sorted(checked[k].keys())} for k in sorted(checked.keys()) if len(checked[k])
  }
  with open(config.path_checked_mt, "w", -1, "utf8", None, "\n") as writer:
    json.dump(sorted_mt, writer, ensure_ascii=False, indent=2)
