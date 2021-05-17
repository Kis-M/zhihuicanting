import pdfkit
import requests
from bs4 import BeautifulSoup as BS
from PyPDF2 import PdfFileMerger


class HTML2PDF(object):
    def __init__(self, base_url):
        self.config = pdfkit.configuration(wkhtmltopdf=r"D:\python\wkhtmltox\bin\wkhtmltopdf.exe")
        self.merger = PdfFileMerger()
        self.total_hrefs = self.GetTotalUrl(base_url)
        if len(self.total_hrefs):
            self.Html2PDF(self.total_hrefs)

    def GetTotalUrl(self, base_url="https://docs.python.org/zh-cn/3.9/tutorial/index.html"):
        total_hrefs = []
        response = requests.get(base_url)
        if response.status_code == 200:
            response.encoding = "utf-8"
            soup = BS(response.text, "html.parser")
            linkas = soup.find("div", class_="toctree-wrapper compound").find_all("a", class_="reference internal")
            total_hrefs = ["https://docs.python.org/zh-cn/3.9/tutorial/" + i.get("href").strip() for i in linkas]
            total_hrefs = [i for i in total_hrefs if "#" not in i]

        if len(total_hrefs):
            return total_hrefs
        else:
            return None

    def Html2PDF(self, hrefs, save_name="out"):
        print("HTML文件下载完成，开始转换PDF")
        pdfs = []
        for index, href in enumerate(hrefs):
            print(href)
            name = "pdfs/" + save_name + "{}.pdf".format(index)
            pdfkit.from_url(url=href, output_path=name, configuration=self.config)
            pdfs.append(name)

        for pdf in pdfs:
            self.merger.append(pdf, import_bookmarks=False)  # 合并pdf文件
        self.merger.write("merge.pdf")
        print("PDF转换完成，请到根目录")


if __name__ == '__main__':
    HTML2PDF(base_url="https://docs.python.org/zh-cn/3.9/tutorial/index.html")
