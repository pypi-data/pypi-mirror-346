
# from docling.document_converter import DocumentConverter
# from docling.datamodel.base_models import InputFormat

# converter = DocumentConverter()
# converter.initialize_pipeline(InputFormat.PDF)

# from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
# path = StandardPdfPipeline.download_models_hf()


# import os
# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from huggingface_hub import HfApi
#

try:
    hfapi=HfApi()
    info = hfapi.repo_info(repo_id="ds4sd/docling-models",timeout=1)
    print("Hugging Face Hub 可访问，模型存在!")
except Exception as e:
    print("连接失败:", str(e))

# import httpx,os
#
# httpx.get("https://hf-mirror.com",timeout=1)

