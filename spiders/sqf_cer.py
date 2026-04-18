import scrapy, json
from scrapy.cmdline import execute
from scrapy.exceptions import CloseSpider
import db_config as db

class SqfCerSpider(scrapy.Spider):
    name = "sqf_cer"
    allowed_domains = ["sqfi.compliancemetrix.com"]

    url = "https://sqfi.compliancemetrix.com/rql/queue/"

    cookies = {
        "__requestverificationtoken961": "Q719EcWSrF2qmo27TPGtmS2MLtfiZiCvaiBYgzbRQsLM4qrb3JPbYOc2Vt/4CK/3/uHYDZTdnKw+CuW8E+OZ7g==",
        "tz": "India Standard Time",
        "tzo": "330",
        "dst": "false",
        "CMXAUTH": "c3RyLTljNzE1ZDBkYTBjZTRkZTg5ZjU0MDVkNTg1MDJjZmUyO0VvWUp4MGhGVUVteUwwb1VTbjVSWjJzVm4zSUNGZDFLNnZram9iQ2NPZVBXM29qNVBpc242aWtvSE8raU1PQm54THlZNmpvaXhUT0NkNFpyMFovWk5RPT07c3FmaS5jb21wbGlhbmNlbWV0cml4LmNvbTttSHRWbXlLUUdONWdPUkJTdHFPaG1uNnV3aXVlckRkSVVSQUdIVWVCTlErbFdQbmg5NmlXRHRTR2dpTkZSVHZr",
    }

    headers = {
        "__requestverificationtoken": "b0eb1d94459447efaaa6b0b5f0cb84a2",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/json",
        "origin": "https://sqfi.compliancemetrix.com",
        "referer": "https://sqfi.compliancemetrix.com/",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    payload = {
        "AppName": "Core_Organization",
        "ViewName": "Active_Not_Pending_No_DFW_Lookup_Q_G_Core_Registration_0",
        "Filters": [],
        "FilterName": "",
        "PageIndex": 0,
        "PageSize": 200,
        "UseDefaultFilter": False,
        "Mode": "Grid",
        "ViewArguments": None,
        "SetId": None,
        "AccessToken": "eBbBZBRE9zOCmaOZXp9Hle3adjKLh/nkWkOx4sibq0+jkdgMqsPesyIg+vwCmhVjPGcJsr6zTJT9eHc1by4tBfZxXYbJdN5GThj0bDYZ03smYB+lHMyyMQRTloYxkEeNp33IuFQPVJvQAsXI2s4epA==",
        "Context": {
            "StoreId": "shd-aed213c65c7945658a4a012ff48e3c77",
            "AppName": "Core_Registration",
            "StorePath": "/store/Core_Registration",
        },
    }

    def start_requests(self):

        yield scrapy.Request(
            url=self.url,
            method="POST",
            headers=self.headers,
            cookies=self.cookies,
            body=json.dumps(self.payload),
            meta={'page': 0},
            callback=self.parse,
        )
    def parse(self, response):
        page = response.meta['page']
        print(f"Processing page: {page}")

        if response.status != 200:
            raise CloseSpider("Non-200 response")

        res = json.loads(response.text)
        items = res.get("DataPage", {}).get("Items", [])
        headers = res.get("DataPage", {}).get("Properties", [])

        if not headers or not items:
            raise CloseSpider("No more Data found - stopping spider")

        for i, row in enumerate(items):
            if len(row) != len(headers):
                print(f"Row {i} length mismatch: {len(row)} vs {len(headers)}")

        records = [dict(zip(headers, row)) for row in items]

        placeholders = ", ".join(["%s"] * len(headers))
        columns = ", ".join(headers)

        sql = f"""
                INSERT INTO {db.organization_name} ({columns})
                VALUES ({placeholders})
                """

        db.cursor.executemany(sql, items)
        db.conn.commit()
        self.logger.info(f"[Page No: {page}] Data inserted successfully.")

        next_payload = self.payload.copy()
        next_payload["PageIndex"] = page + 1

        yield scrapy.Request(
            url=self.url,
            method="POST",
            headers=self.headers,
            cookies=self.cookies,
            body=json.dumps(next_payload),
            meta={'page': page + 1},
            callback=self.parse
        )

if __name__ == '__main__':
    execute("scrapy crawl sqf_cer".split())

