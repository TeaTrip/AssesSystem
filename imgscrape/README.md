# IAD - Image Scraper

Web crawler based on [Scrapy](http://scrapy.org/) [ImagePipeline](http://doc.scrapy.org/en/latest/topics/media-pipeline.html#using-the-images-pipeline) implementation. Google each label from dataset, downloading all images form page to MongoDB, 'asses' DB, 'images' table.

## Install dependencies
```bash
pip install scrapy validators
```

## Usage
```
python collect.py

```
