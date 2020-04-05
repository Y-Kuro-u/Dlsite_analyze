from Controller.Analyzer.analyzer import DlSiteNetwork
from Controller.Crawler import dlsite_crawler
from matplotlib import rcParams

if __name__ == "__main__":
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

    crawler = dlsite_crawler.AllDlsiteCrawler()
    networks = DlSiteNetwork()
    tags = crawler.run()
    
    dataframe = networks.make_data_frame(tags)[0]
    networks.make_network(dataframe)