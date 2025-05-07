import os

from xzonn_mt_tools.config import Config
from xzonn_mt_tools.helper import MTDatabase


def update_mt_database(config: Config):
  database = MTDatabase(config.path_mt_database, config.path_override)
  for file_name in sorted(
    os.listdir(f"{config.dir_translation_lines}/japanese"),
    key=lambda x: (1 if x not in ["translated.txt", "untranslated.txt"] else 0, x),
  ):
    if not file_name.endswith(".txt"):
      continue
    with open(f"{config.dir_translation_lines}/japanese/{file_name}", "r", -1, "utf-8") as reader:
      japanese = reader.read().strip("\n").splitlines()

    for translator, translator_data in config.translators.items():
      chinese_path = f"{config.dir_translation_lines}/{translator}/{file_name}"
      japanese_path = f"{config.dir_translation_lines}/{translator}-japanese/{file_name}"
      if translator_data.get("japanese", False):
        japanese_path = f"{config.dir_translation_lines}/japanese/{file_name}"
      if not os.path.exists(chinese_path) or not os.path.exists(japanese_path):
        continue

      with open(chinese_path, "r", -1, "utf-8") as reader:
        chinese = reader.read().strip("\n").splitlines()
      with open(japanese_path, "r", -1, "utf-8") as reader:
        chinese_japanese = reader.read().strip("\n").splitlines()

      if len(japanese) != len(chinese) or len(japanese) != len(chinese_japanese):
        continue

      for j, c, cj in zip(japanese, chinese, chinese_japanese):
        database.update(translator, j, c, cj)

  database.commit()

  config.logger.info(f"机翻数据库现有条目 {len(database.data) + len(database.override)} 条")
