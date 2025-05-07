import os
from typing import Iterable

from xzonn_mt_tools.config import Config
from xzonn_mt_tools.helper import MTDatabase, MTTranslationItem


def split_texts(config: Config):
  def write_translation_lines(folder: str, file_name: str, lines: Iterable[str]) -> None:
    os.makedirs(f"{config.dir_translation_lines}/{folder}/", exist_ok=True)
    path = f"{config.dir_translation_lines}/{folder}/{file_name}.txt"
    lines_list = list(lines)
    if len(lines_list) == 0:
      if os.path.exists(path):
        os.remove(path)
      return
    with open(path, "w", -1, "utf-8", None, "\n") as writer:
      writer.write("\n".join(lines_list))

  def remove_translation_lines(folder: str, file_name: str) -> None:
    path = f"{config.dir_translation_lines}/{folder}/{file_name}.txt"
    if os.path.exists(path):
      os.remove(path)

  translators_count = len(config.translators)

  with open(config.path_all_text, "r", -1, "utf-8") as reader:
    text = reader.read()

  text = config.replace_control(text)
  text = config.replace_japanese(text)

  text_list = text.split("\n")

  lines = []
  for line in text_list:
    content = config.postfix_pattern.sub("", config.prefix_pattern.sub("", line.strip()))
    if content and content not in lines:
      lines.append(content)

  config.logger.info(f"{len(lines)} 行文本需翻译")

  full_translated: dict[str, dict[str, MTTranslationItem]] = {translator: {} for translator in config.translators}
  partial_translated: dict[str, dict[str, MTTranslationItem]] = {translator: {} for translator in config.translators}
  untranslated: dict[str, list[str]] = {translator: [] for translator in config.translators}

  database = MTDatabase(config.path_mt_database, config.path_override)
  for line in lines:
    translated = 0
    line_translation: dict[str, MTTranslationItem] = {}
    for translator in config.translators:
      chinese = database.translate(translator, line)
      if chinese.get("override", False):
        break
      if chinese.get("chinese"):
        line_translation[translator] = chinese
        translated += 1
    else:
      if translated == translators_count:
        for translator in config.translators:
          full_translated[translator][line] = line_translation[translator]
      else:
        for translator in config.translators:
          if translator not in line_translation:
            untranslated[translator].append(line)
          else:
            partial_translated[translator][line] = line_translation[translator]

  write_translation_lines("japanese", "translated", full_translated[translator].keys())
  for translator, translator_data in config.translators.items():
    auto_japanese = translator_data.get("japanese", False)
    write_translation_lines(translator, "translated", map(lambda x: x["chinese"], full_translated[translator].values()))
    write_translation_lines("japanese", translator, partial_translated[translator].keys())
    write_translation_lines(
      translator, translator, map(lambda x: x["chinese"], partial_translated[translator].values())
    )
    if untranslated[translator]:
      write_translation_lines("japanese", f"{translator}-untranslated", untranslated[translator])
      config.logger.info(f"{len(untranslated[translator])} 行文本待 {translator} 翻译")
    else:
      remove_translation_lines("japanese", f"{translator}-untranslated")
    remove_translation_lines(translator, f"{translator}-untranslated")
    remove_translation_lines(f"{translator}-japanese", f"{translator}-untranslated")
    if not auto_japanese:
      write_translation_lines(
        f"{translator}-japanese", "translated", map(lambda x: x["japanese"], full_translated[translator].values())
      )
      write_translation_lines(
        f"{translator}-japanese", translator, map(lambda x: x["japanese"], partial_translated[translator].values())
      )
