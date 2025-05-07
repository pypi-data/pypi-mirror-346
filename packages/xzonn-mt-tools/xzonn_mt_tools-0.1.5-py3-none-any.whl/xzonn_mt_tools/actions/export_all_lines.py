from xzonn_mt_tools.config import Config
from xzonn_mt_tools.helper import get_text_dict


def export_all_lines(config: Config):
  text_dict = get_text_dict(f"{config.basic_root}/{config.basic_language}", config.name_filter)
  lines = []

  for items in text_dict.values():
    for item in items:
      if item.get("trash", False):
        continue
      lines.append(config.replace_line_break(item.get("translation", item.get("original", ""))))

  with open(config.path_all_text, "w", -1, "utf8", None, "\n") as writer:
    writer.write("\n".join(lines))

  config.logger.info(f"导出了 {len(lines)} 行文本")
