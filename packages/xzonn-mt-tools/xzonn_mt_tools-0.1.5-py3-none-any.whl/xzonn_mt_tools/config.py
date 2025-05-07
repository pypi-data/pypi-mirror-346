import logging
import re

from xzonn_mt_tools.helper import ControlPattern, MTTranslatorItem, TranslationItem


class Config:
  logger = logging.getLogger()

  basic_language = "ja"
  translation_language = "zh_Hans"

  basic_root = "./texts"
  name_filter = re.compile(".+")

  path_all_text = "workspace/全部文本.txt"
  path_compared_mt = "workspace/机翻对比.json"
  path_checked_mt = "workspace/机翻校对.json"

  dir_translation_lines = "translations"
  path_mt_database = "translations/机翻数据库.pickle"
  path_override = "translations/人翻数据库.json"

  prefix_pattern = re.compile(r"^(?:◆|\s|\\n)*", re.MULTILINE)
  postfix_pattern = re.compile(r"(?:◆|\s|\\n)*$", re.MULTILINE)
  trash_pattern = re.compile(
    r"^[0-9a-zA-Z０-９ａ-ｚＡ-Ｚ#\-/？~№－\?:＋％%\.．ⅠⅡ <>_;，。！：；\n\+]+$|１２３４５６７８９０"
  )
  japanese_pattern = re.compile(r"[\u3040-\u309F\u30A0-\u30FF]+")

  control_pattern_list: list[ControlPattern] = [
    {
      "pattern": re.compile(r"(?:<[^<>]+>|\[[^\[\]]+\]|\$\{[^\{\}]+\})+|\\n"),
      "replace": "◆",
      "translate": [
        re.compile(r"[◆]"),
        re.compile(r"[◆＜＞]"),
        re.compile(r"[◆＜＞“”]"),
        re.compile(r"[◆＜＞“”‘’]"),
        re.compile(r"[◆＜＞“”‘’（）]"),
      ],
      "overdose": "",
    },
  ]

  japanese_replace_dict: dict[str, str] = {}
  chinese_replace_dict: dict[str, str] = {}

  translators: dict[str, MTTranslatorItem] = {
    "baidu": {
      "score": 1.0,
      "japanese": False,
    },
    "youdao": {
      "score": 1.0,
      "japanese": False,
    },
    "sakura": {
      "score": 2.0,
      "japanese": True,
    },
  }

  def __init__(self, logger: logging.Logger):
    self.logger = logger

  def replace_line_break(self, text: str) -> str:
    return text.replace("\n", "\\n")

  def replace_back_line_break(self, text: str) -> str:
    return text.replace("\\n", "\n")

  def replace_control(self, text: str) -> str:
    for pattern in self.control_pattern_list:
      text = pattern["pattern"].sub(pattern["replace"], text)

    return text

  def reinsert_control(self, original: str, translated: str) -> tuple[str, bool]:
    """将原文中的控制符重新插入到译文中

    :param original: 原文
    :param translated: 译文
    :return: 重新插入控制符后的译文
    """

    not_match = False
    for pattern in self.control_pattern_list:
      controls = pattern["pattern"].findall(original)
      original = pattern["pattern"].sub(pattern["replace"], original)
      if len(controls) > 0:
        for p in pattern["translate"]:
          controls_c = p.findall(translated)
          if len(controls_c) == len(controls):
            # 如果控制符数量相同，直接替换
            for _ in controls:
              translated = p.sub(_, translated, 1)
            break
        else:
          # 如果所有模式下控制符数量均不同，以第一个模式替换
          p = pattern["translate"][0]
          controls_c = p.findall(translated)
          for _, __ in zip(controls, controls_c):
            translated = p.sub(_, translated, 1)
          if len(controls_c) < len(controls):
            translated += "".join(controls[len(controls_c) :])
          else:
            for _ in controls_c[len(controls) :]:
              translated = translated.replace(_, pattern["overdose"], 1)
          not_match = True

    translated = self.replace_back_line_break(translated)
    return translated, not_match

  def replace_punc(self, text: str, title_mark: bool = True) -> str:
    """将标点符号替换为中文习惯的符号

    :param text: 文本
    :param title_mark: 是否替换书名号
    :return: 替换后的文本
    """
    text = text.replace("...", "…")
    text = re.sub(r"([^…]|^)…([^…]|$)", r"\1……\2", text)
    text = re.sub(r"([^…]|^)…([^…]|$)", r"\1……\2", text)
    text = re.sub(r"([^—]|^)—([^—]|$)", r"\1——\2", text)
    text = re.sub(r"([^—]|^)—([^—]|$)", r"\1——\2", text)

    replace_dict = {
      ",": "，",
      "?": "？",
      "!": "！",
      # "‘": "“",
      # "’": "”",
      ":": "：",
      "~": "～",
      "&": "＆",
      "・": "·",
      "『": "“",
      "』": "”",
      "「": "“",
      "」": "”",
      "｢": "“",
      "｣": "”",
      "ﾟ": "°",
      "--": "——",
      "- - ": "——",
      "——。": "——",
      "——，": "——",
      "ーー": "——",
      "──": "——",
      "――": "——",
      "……。": "……",
      "……，": "……",
      "——……": "……",
      "～。": "～",
      "～，": "～",
      "ok": "OK",
      "(": "（",
      ")": "）",
      "<": "＜",
      ">": "＞",
      "〈": "＜",
      "〉": "＞",
      "＠": "@",
      "。。": "。",
      "！。": "！",
      "？。": "？",
      "。，": "。",
    }
    for k, v in replace_dict.items():
      text = text.replace(k, v)

    if title_mark:
      text = text.replace("《", "“").replace("》", "”")

    text = re.sub(r"(?<=[？！～＆])[ 　](?=[＆？！～])", "", text)
    text = re.sub(r"(?<!\d)(\d\d)：(\d\d)(?!\d)", r"\1:\2", text)
    text = re.sub(r"\"([^\"]+)\"", r"“\1”", text)
    return text

  def replace_japanese(self, text: str) -> str:
    for k, v in self.japanese_replace_dict.items():
      text = re.sub(k, v, text, flags=re.IGNORECASE)

    return text

  def replace_chinese(self, text: str) -> str:
    for k, v in self.chinese_replace_dict.items():
      text = re.sub(k, v, text, flags=re.IGNORECASE)

    return text

  def replace_new_text(self, sheet_name: str, item: TranslationItem, text: str) -> str:
    ja = item.get("original", "")

    while re.search(r"(“[^”]*)“([^“”]+)”", text):
      text = re.sub(r"(“[^”]*)“([^“”]+)”", r"\1‘\2’", text)
    while re.search(r"((?:^|”)[^“]*)‘([^‘’]+)’", text):
      text = re.sub(r"((?:^|”)[^“]*)‘([^‘’]+)’", r"\1“\2”", text)

    if text.endswith("。"):
      if ja.endswith("”") or ja.endswith("」"):
        text = text + "”"
      elif ja.endswith("’") or ja.endswith("』"):
        text = text + "’"
    elif ja.endswith("。") and text[-1] not in "、，！？：；”’）…—～\n]":
      text = text + "。"

    if (text.endswith("。”") or text.endswith('。"') or text.endswith("。’") or text.endswith("。'")) and not (
      ja.endswith("”")
      or ja.endswith('"')
      or ja.endswith("’")
      or ja.endswith("'")
      or ja.endswith("」")
      or ja.endswith("』")
    ):
      text = text[:-1]
    elif text.endswith("。）") and not (ja.endswith(")") or ja.endswith("）")):
      text = text[:-1]

    text = re.sub(r"\n([、，。！？：；”’）])", r"\1\n", text)

    return text

  def check_simple_translation(
    self,
    original: str,
    translated: str,
    score: float,
  ) -> tuple[str, float]:
    """检查简单的翻译问题

    :param original: 经过处理后的原文
    :param translated: 译文
    :param score: 基础分数
    :param control_pattern_list: 控制符模式列表
    """
    if self.japanese_pattern.search(translated):
      score -= 4.0

    translated, not_match = self.reinsert_control(original, translated)
    if not_match:
      score -= 4.0

    return translated, score

  def check_translation(self, sheet_name: str, line_id: str, ja: str, zh: str) -> str:
    return zh
