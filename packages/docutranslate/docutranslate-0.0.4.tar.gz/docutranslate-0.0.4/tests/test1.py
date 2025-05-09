from docutranslate import FileTranslater


translater = FileTranslater(base_url="https://open.bigmodel.cn/api/paas/v4",
                            key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
                            model_id="glm-4-flashx")
# translater = FileTranslater(base_url="http://127.0.0.1:1234/v1",
#                             key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
#                             model_id="qwen3-30b-a3b-128k")
# translater = FileTranslater(base_url="http://127.0.0.1:1234/v1",
#                             key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
#                             model_id="qwen3-0.6b")
translater.translate_markdown_file(r"C:\Users\jxgm\Desktop\FileTranslate\tests\resource\regex.md",
                                   to_lang="中文",
                                   output_format="html")