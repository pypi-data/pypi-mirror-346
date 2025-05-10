from docutranslate.utils.markdown_splitter import split_markdown_text
from docutranslate import FileTranslater

ts=FileTranslater()
ts.read_file(r"C:\Users\jxgm\Desktop\FileTranslate\tests\resource\互联网认证授权机制.md")
ts._mask_uris_in_markdown()
# ts._unmask_uris_in_markdown()

a=split_markdown_text(ts.markdown,max_block_size=5000)
print("\n==================\n".join(a))