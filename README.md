# bilkent-summer-work TUR
Bilkent Summer stajı için öğrencilere iş veren şirketleri Excel formatına çevireceğim.
4306 şirketin bilgisi var. Hangi departmanlardan öğrenci istedikleri ve Cyberpark'ta 
olup olmadıkları bilgisi de var.

# bilkent-summer-work ENG
I will create an Excel file of the companies that give summer work for bilkent students. 
There are information of 4306 companies. Qualified departments are also added. The 
companies which are in Cyberpark are marked.

# Some Important Notes
* As recommended the code of this project will only create two csv files on .txt format which are stored on 'data' folder. 
* Other libraries could also be used, but I've chosen to use scrapy on this project, please don't recommend me to use other libs (like urllib.requests, selenium or others). Scrapy is the coolest way to scrape these kinds of data :)
* I didn't want to create a scrapy project so we will use a primitive way of using spiders.
* Try not to crush Bilkent's servers. Adding waiting time for our spiders will hopefully solve this issue.
* The information is fetched from: http://mfstaj.cs.bilkent.edu.tr

# How To Use?
```python
first_process()   # would start the first spider
second_process()  # would start the second spider
```

# Future
- [] adding pandas and xlsxwriter implementation for turning csv to excel.  
