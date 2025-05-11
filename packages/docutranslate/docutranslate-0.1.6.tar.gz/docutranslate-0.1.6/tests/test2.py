from docutranslate.utils.markdown_splitter import split_markdown_text
from docutranslate import FileTranslater

ts=FileTranslater()
ts.read_file(r".\resource\regex.md")
ts._mask_uris_in_markdown()
# ts._unmask_uris_in_markdown()

a=split_markdown_text(ts.markdown,max_block_size=2000)
print("\n==================\n".join(a))