from docutranslate import FileTranslater


translater = FileTranslater(base_url="https://open.bigmodel.cn/api/paas/v4",
                            key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
                            # model_id="glm-z1-flash",
                            model_id="glm-4-air",
                            max_concurrent=20
                            # artifact_path=r"C:\Users\jxgm\.cache\docling\models"
                            )
# translater = FileTranslater(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#                             key="sk-a3dd6bdedb5f446cbe678aedfab32038",
#                             model_id="qwen-plus",
#                             max_concurrent=20)
# translater = FileTranslater(base_url="http://127.0.0.1:1234/v1",
#                             key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
#                             model_id="qwen3-1.7b")
# translater=FileTranslater(base_url="https://api.deepseek.com/v1",
#                key="sk-d809e448131d4fbc903a0ed476964294",
#                model_id="deepseek-chat")

translater.translate_file(r"C:\Users\jxgm\Desktop\FileTranslate\tests\resource\test6.md",
                          formula=True,
                          code=True,
                          refine=False,
                          to_lang="中文",
                          output_format="markdown")

# translater.read_file(r"C:\Users\jxgm\Desktop\FileTranslate\tests\resource\test2.pdf",formula=True,code=True,save=True)