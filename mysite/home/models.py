from django.db import models



#此模型的檔案將上傳到 media資料夾
class Document(models.Model):
    FILES =models.FileField(upload_to = "")  #檔案名稱
    upload_time = models.DateTimeField(auto_now=True)   #上傳時間
    Reviewer = models.CharField(max_length=200)  #檔名稱