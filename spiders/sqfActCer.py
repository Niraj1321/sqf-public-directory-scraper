import scrapy, json
from scrapy.cmdline import execute
import db_config as db
from scrapy.exceptions import CloseSpider

class SqfactcerSpider(scrapy.Spider):
    name = "sqfActCer"
    allowed_domains = ["sqfi.compliancemetrix.com"]

    url = 'https://sqfi.compliancemetrix.com/rql/queue/'

    cookies = {
        'group': 'public_directory',
        'group-storeid': '',
        '__requestverificationtoken611': 'JFfnXGHLkwgDeO0TtYpfeCQFvOt6nIQljmjUXfEAwlSXWz1+BISC92Z86MJGu0HzG76UgCoHGoCIYkKPy7mIAg==',
        'tz': 'India Standard Time',
        'tzo': '330',
        'dst': 'false',
        'RqlCookieNoticeDismissed': '1',
        '_ga': 'GA1.1.1940673670.1774253372',
        '_ga_QD7TDPJK65': 'GS2.1.s1774336898$o5$g0$t1774336898$j60$l0$h0',
        'AWSALB': 'lCxkGZ8PC81hBJrsHZfFU+8pxpcW7p/UIOSUEzim/KBilXKGgP8z0ZiR6SUaCMEL0WqucmbDYPxMdvB0kMJuCE3qL6Be6VlU6POgtNbTaAFa19ymu5t97FiVKpUQ',
        'AWSALBCORS': 'lCxkGZ8PC81hBJrsHZfFU+8pxpcW7p/UIOSUEzim/KBilXKGgP8z0ZiR6SUaCMEL0WqucmbDYPxMdvB0kMJuCE3qL6Be6VlU6POgtNbTaAFa19ymu5t97FiVKpUQ',
    }

    headers = {
        '__requestverificationtoken': '71fc29d90b3b4e6eb7a3287e6898bb44',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,gu;q=0.8,hi;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://sqfi.compliancemetrix.com',
        'priority': 'u=1, i',
        'referer': 'https://sqfi.compliancemetrix.com/rql/g/Public_Directory',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'group=public_directory; group-storeid=; __requestverificationtoken611=JFfnXGHLkwgDeO0TtYpfeCQFvOt6nIQljmjUXfEAwlSXWz1+BISC92Z86MJGu0HzG76UgCoHGoCIYkKPy7mIAg==; tz=India Standard Time; tzo=330; dst=false; RqlCookieNoticeDismissed=1; _ga=GA1.1.1940673670.1774253372; _ga_QD7TDPJK65=GS2.1.s1774336898$o5$g0$t1774336898$j60$l0$h0; AWSALB=lCxkGZ8PC81hBJrsHZfFU+8pxpcW7p/UIOSUEzim/KBilXKGgP8z0ZiR6SUaCMEL0WqucmbDYPxMdvB0kMJuCE3qL6Be6VlU6POgtNbTaAFa19ymu5t97FiVKpUQ; AWSALBCORS=lCxkGZ8PC81hBJrsHZfFU+8pxpcW7p/UIOSUEzim/KBilXKGgP8z0ZiR6SUaCMEL0WqucmbDYPxMdvB0kMJuCE3qL6Be6VlU6POgtNbTaAFa19ymu5t97FiVKpUQ',
    }

    json_data = {
        'AppName': 'Core_Certification_Directory_Analyze',
        'ViewName': 'Filtered_Report_Q',
        'Filters': [],
        'FilterName': '',
        'PageIndex': 0,
        'PageSize': 200,
        'UseDefaultFilter': False,
        'Mode': 'Grid',
        'IsEmbed': True,
        'UseEmbedQueueTest': False,
        'NestedQueuesMasterAppName': 'Core_Certification_Directory_Analyze',
        'NestedQueuesMasterViewName': 'Filtered_Report_Q',
        'ViewArguments': None,
        'Context': {
            'AppName': 'Core_Certification_Directory',
            'StoreId': 'str-1fd8be65951a40db9d295ca6f73f032b',
            'ChainContextId': 'str-1fd8be65951a40db9d295ca6f73f032b',
        },
    }

    def start_requests(self) :
        yield scrapy.Request(
            url=self.url,
            method="POST",
            headers=self.headers,
            cookies=self.cookies,
            body=json.dumps(self.json_data),
            meta={'page': 0},
            callback=self.parse
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
        INSERT INTO {db.certificate_table} ({columns})
        VALUES ({placeholders})
        """

        db.cursor.executemany(sql, items)
        db.conn.commit()
        self.logger.info(f"[Page No: {page}] Data inserted successfully.")

        next_payload = self.json_data.copy()
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

if __name__ == "__main__":
    execute("scrapy crawl sqfActCer".split())