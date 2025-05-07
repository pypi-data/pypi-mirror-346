import json
import os

from xzonn_mt_tools.config import Config
from xzonn_mt_tools.helper import MTTranslationItem, TranslationItem, get_text_dict


def update_translations(config: Config):
  with open(config.path_compared_mt, "r", -1, "utf-8") as reader:
    translation_dict: dict[str, list[MTTranslationItem]] = json.load(reader)

  checked: dict[str, dict[str, list[str]]] = {}
  try:
    with open(config.path_checked_mt, "r", -1, "utf8") as reader:
      checked = json.load(reader)
  except Exception:
    pass

  def check_mt(mt: list[tuple[str, int]], ja: str, ch: str) -> bool:
    if all(x == ja for x in mt):
      return False

    if all(set(x) == set(ch) and len(set(ch)) == 1 for x in mt):
      return False

    return True

  def add_sheet(sheet_name: str, ja_list: list[TranslationItem]):
    output_path = f"{config.basic_root}/{config.translation_language}/{sheet_name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result_list = []
    for value in ja_list:
      if value.get("trash", False):
        continue

      key = value["key"]
      speaker = value.get("speaker", "")
      ja = value["original"]
      ch = ja
      mt_comment = ""

      if ja in translation_dict:
        mt_list = list(
          map(lambda x: config.replace_new_text(sheet_name, value, x["chinese"]), translation_dict[ja]),
        )
        if mt_list:
          ch = mt_list[0]
          if check_mt(mt_list, ja, ch):
            mt_list_output = ["**翻译辅助**："]
            for mt in mt_list:
              if mt not in mt_list_output:
                mt_list_output.append(mt)
            mt_comment = "\n\n".join([_.replace("\n", "  \n") for _ in mt_list_output])
      else:
        config.logger.warning(f"没有翻译：{repr(ja)}")

      if sheet_name in checked and key in checked[sheet_name]:
        ch = checked[sheet_name][key][0]

      comment = "\n\n".join(filter(lambda x: x, [speaker, mt_comment.strip()]))

      result_list.append(
        dict(
          zip(
            ("key", "original", "translation", "context"),
            (key, ja, ch, comment),
          )
        )
      )

    if len(result_list) == 0:
      if os.path.exists(output_path):
        os.remove(output_path)
      return False

    with open(output_path, "w", -1, "utf8", None, "\n") as writer:
      json.dump(result_list, writer, ensure_ascii=False, indent=2)

    return True

  ja_list = get_text_dict(f"{config.basic_root}/{config.basic_language}", config.name_filter)
  for sheet_name, sheet_data in ja_list.items():
    add_sheet(sheet_name, sheet_data)
