import re

from docutranslate.utils.markdown_utils import MaskDict

mask_dict=MaskDict()
def uris2placeholder(markdown:str, mask_dict:MaskDict):
    def uri2placeholder(match: re.Match):
        id = mask_dict.create_id()
        mask_dict.set(id, match.group(2))
        return f"{match.group(1)}(<ph-{id}>)"

    uri_pattern = r'(!?\[.*?\])\((.*?)\)'
    markdown = re.sub(uri_pattern, uri2placeholder, markdown)
    return markdown

if __name__ == '__main__':
    markdown_text="""
    ![一个图片](https://baidu.com)
    [一个链接](https://baidu.com)
    """
    print(uris2placeholder(markdown_text,mask_dict))