from docutranslate import FileTranslater


translater = FileTranslater(base_url="https://open.bigmodel.cn/api/paas/v4",
                            key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
                            # model_id="glm-z1-flash"
                            model_id="glm-4-air"
                            )
# translater = FileTranslater(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#                             key="sk-a3dd6bdedb5f446cbe678aedfab32038",
#                             model_id="qwen-plus")
# translater = FileTranslater(base_url="http://127.0.0.1:1234/v1",
#                             key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
#                             model_id="qwen3-1.7b")
translater.translate_pdf_file(r"C:\Users\jxgm\Desktop\FileTranslate\tests\resource\test2.pdf",
                                   formula=True,
                                    code=True,
                                   to_lang="英文",
                                   output_format="html")