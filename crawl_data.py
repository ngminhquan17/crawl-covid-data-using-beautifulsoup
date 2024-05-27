import bs4
import requests
import csv

def GetPageContent(url):
    page = requests.get(url, headers={"Accept-Language": "en-US"})
    return bs4.BeautifulSoup(page.text, "html.parser")

def CrawDataCovid():
    url = 'https://www.worldometers.info/coronavirus/'
    soup = GetPageContent(url)

    data_rows = []

    table = soup.find('table', {'class': 'table table-bordered table-hover main_table_countries'})

    if table:
        # Lấy tiêu đề từ thẻ <th>
        th_tags = table.findAll('th')
        title_row = [th.get_text() for th in th_tags]
        data_rows.append(title_row)

        # Bỏ đi hàng tiêu đề
        for tr in table.find_all('tr')[1:]:
            row = []
            columns = tr.find_all('td')
            for column in columns:
                row.append(column.get_text())
            data_rows.append(row)

        return data_rows
    else:
        print("Không tìm thấy bảng")

def ExportCsv(data_rows):
    with open('covid.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_rows)

data_rows = CrawDataCovid()
if data_rows:
    data_rows = data_rows[0:1] + data_rows[8:]
    ExportCsv(data_rows)
