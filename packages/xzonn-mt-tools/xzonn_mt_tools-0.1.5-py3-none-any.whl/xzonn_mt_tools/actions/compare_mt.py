import difflib
import json
import random

from xzonn_mt_tools.config import Config
from xzonn_mt_tools.helper import MTDatabase, MTTranslationItem


def compare_mt(config: Config):
  database = MTDatabase(config.path_mt_database, config.path_override)

  def translate(replaced_line: str, original_line: str = "") -> list[MTTranslationItem]:
    line_data: list[MTTranslationItem] = []

    prefix = config.prefix_pattern.search(replaced_line).group(0)
    replaced_line = replaced_line.removeprefix(prefix)
    suffix = config.postfix_pattern.search(replaced_line).group(0)
    replaced_line = replaced_line.removesuffix(suffix)

    for translator, translator_data in config.translators.items():
      translation = database.translate(translator, replaced_line)
      if not translation:
        continue
      c = translation["chinese"]
      if not c:
        continue
      cj = translation["japanese"]
      override = translation.get("override", False)

      if override:
        score = 255.0
        c, score = config.check_simple_translation(original_line, f"{prefix}{c}{suffix}", score)
        line_data.append(
          {
            "translator": "override",
            "chinese": f"{prefix}{c}{suffix}",
            "score": score,
          }
        )
        break

      c = config.replace_punc(c)
      c = config.replace_chinese(c)

      score = 0.0
      if translator_data.get("japanese", False):
        score = translator_data.get("score", 2.0)
      else:
        score = difflib.SequenceMatcher(lambda x: x == " ", replaced_line, cj).ratio()

      c, score = config.check_simple_translation(original_line, f"{prefix}{c}{suffix}", score)

      line_data.append(
        {
          "translator": translator,
          "chinese": c,
          "score": score,
        }
      )

    random.seed(original_line)
    line_data.sort(key=lambda x: (x["score"], random.random()), reverse=True)
    return line_data

  with open(config.path_all_text, "r", -1, "utf-8") as reader:
    lines = reader.read().strip("\n").splitlines()

  translated_lines: dict[str, list[MTTranslationItem]] = {}
  for original_line in lines:
    replaced_line = config.replace_control(original_line)
    replaced_line = config.replace_japanese(replaced_line)

    translations = translate(replaced_line, original_line)
    original_line = config.replace_back_line_break(original_line)
    if len(translations) == 0:
      config.logger.warning(f"未找到翻译：{repr(original_line)}")
      continue
    if all(data["score"] < 0 for data in translations):
      config.logger.warning(f"多项检测不匹配：{repr(original_line)}")
      for data in translations:
        translator = data["translator"]
        config.logger.warning(f"{translator:>14}：{repr(data['chinese'])}")
    translated_lines[original_line] = translations

  with open(config.path_compared_mt, "w", -1, "utf-8", None, "\n") as writer:
    json.dump(translated_lines, writer, ensure_ascii=False, indent=2)
