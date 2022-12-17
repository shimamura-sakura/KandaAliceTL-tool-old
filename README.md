# 神田アリスも翻訳する

"神田アリスも推理スル" 文本的修改工具

## 用法

- 提取原文件
  - 使用工具(Ryujinx, yuzu)等提取 exefs, romfs, 复制文件
    - 文件 `exefs/main` 到 `files_old/main` (大小应为 3352505 字节)
    - 文件夹 `romfs/data_yuri/01_script` 到 `files_old/01_script`
- 生成 json 文件: `python main_export.py`，在 `files_new` 中得到一系列 json 文件
- 编辑 json 文件：修改 new 行
- 生成新文件: `python main_create.py`
- 制作 mod: 按照以下方式复制文件
  - `exefs`
    - `main` (`files_out/main`)
  - `romfs`
    - `data_yuri`
      - `01_script`
        - `*.bin` (`files_out/*.bin`)
      - `font`
        - `NotoSansJP-Medium.otf` (建议使用思源黑体，应是 otf 格式)
        - `NotoSansJP-Regular.otf` (建议使用思源黑体，应是 otf 格式)

## 思想

剧本文件使用 JIS 编码，游戏程序查表将 JIS 转换为 UTF-16LE 调用字体显示。为了显示 JIS 编码中不存在的字符（如中文汉字），我们将转换表中一些 JIS 码点对应的 UTF-16LE 编码换成我们想要显示的字符的编码。然后在生成剧本文件时，用那些替换了转换目标的 JIS 码点代替我们想要显示的字符。

设集合 J 是 JIS 编码能够表示的所有字符  
设集合 A 是原剧本中用到的所有字符（谢谢志水，只有不到 2000 个，而 JIS 有 7000 多个）  
设集合 B 是新剧本中用到的所有字符 

可以用于替换的字符 `C = J - A`
替换的目标字符 `D = B - A`

本程序自动完成以上的统计、计算、替换过程，并生成新的可执行文件和剧本文件。
