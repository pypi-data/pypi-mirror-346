import json
import os
import pickle
import re
from typing import TypedDict


class ControlPattern(TypedDict):
  pattern: re.Pattern  # 控制符模式
  replace: str  # 替换到原文中以供翻译
  translate: list[re.Pattern]  # 译文中可能存在的模式
  overdose: str  # 译文中多余的控制符


class MTTranslatorItem(TypedDict):
  score: float
  japanese: bool


class MTTranslationItem(TypedDict):
  translator: str
  chinese: str
  japanese: str
  override: bool
  score: float


class TranslationItem(TypedDict):
  key: str
  original: str
  translation: str
  context: str
  speaker: str
  prefix: str
  suffix: str
  trash: bool


class MTDatabase:
  """机翻数据库"""

  def __init__(self, path: str, override_path: str = "") -> None:
    self.path = path
    self.data: dict[str, dict[str, list[str]]] = self._load(path)
    self.override: dict[str, str] = self._load(override_path)

  def _load(self, path: str):
    if not path or not os.path.exists(path):
      return {}
    else:
      try:
        with open(path, "r", -1, "utf8") as reader:
          return json.load(reader)
      except Exception:
        try:
          with open(path, "rb") as reader:
            return pickle.load(reader)
        except Exception:
          return {}

  def translate(self, translator: str, japanese: str) -> MTTranslationItem:
    if japanese in self.override:
      return {
        "chinese": self.override[japanese],
        "japanese": japanese,
        "override": True,
      }
    elif japanese in self.data:
      line = self.data.get(japanese, {}).get(translator, ["", ""])
      return {
        "chinese": line[0],
        "japanese": line[1],
      }
    return {}

  def update(self, translator: str, japanese: str, chinese: str, chinese_japanese: str) -> None:
    if japanese not in self.data:
      self.data[japanese] = {}
    self.data[japanese][translator] = [chinese, chinese_japanese]

  def commit(self):
    with open(self.path, "wb") as writer:
      pickle.dump(self.data, writer)

  def is_translated(self, japanese: str) -> bool:
    return japanese in self.data or japanese in self.override


def half_to_full(text: str) -> str:
  for i in range(10):
    text = text.replace(str(i), chr(ord("０") + i))

  for i in range(26):
    text = text.replace(chr(ord("A") + i), chr(ord("Ａ") + i))
    text = text.replace(chr(ord("a") + i), chr(ord("ａ") + i))

  return text


def full_to_half(text: str) -> str:
  for i in range(10):
    text = text.replace(chr(ord("０") + i), str(i))

  for i in range(26):
    text = text.replace(chr(ord("Ａ") + i), chr(ord("A") + i))
    text = text.replace(chr(ord("ａ") + i), chr(ord("a") + i))

  return text


def get_text_dict(base_root: str, name_filter: re.Pattern = None) -> dict[str, list[TranslationItem]]:
  """获取文本列表

  :param base_root: 基础路径
  :param name_filter: 名称过滤器
  :return: 文本列表
  """
  data = {}
  for root, dirs, files in os.walk(base_root):
    for file_name in files:
      if not file_name.endswith(".json"):
        continue

      sheet_name = os.path.relpath(f"{root}/{file_name}", base_root).replace("\\", "/").removesuffix(".json")
      if name_filter and not name_filter.match(sheet_name):
        continue

      with open(f"{base_root}/{sheet_name}.json", "r", -1, "utf8") as reader:
        messages = json.load(reader)

      data[sheet_name] = messages

  return data
