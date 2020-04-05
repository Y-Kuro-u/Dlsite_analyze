from Controller.Crawler.crawler import Crawler

class AllDlsiteCrawler(Crawler):
    def run(self):
        url_100 = "https://www.dlsite.com/maniax/ranking/total?category=comic"
        url_200 = "https://www.dlsite.com/maniax/ranking/total?category=comic&page=2"
        url_300 = "https://www.dlsite.com/maniax/ranking/total?category=comic&page=3"
        tags_1_100 = self._run(url_100)
        tags_101_200 = self._run(url_200)
        tags_201_300 = self._run(url_300)

        return [tags_1_100,tags_101_200,tags_201_300]

    def _run(self,url):
        bs = self.get_bs(url)
        search_tags = bs.select(".search_tag")
        tag_list = []
        for search_tag in search_tags:
            tags = []
            for tag in search_tag.stripped_strings:
                tags.append(tag)
            if tags:
                tag_list.append(tags)
        return tag_list

class MonthDlsiteCrawler(Crawler):
    def run(self):
        url_100 = "https://www.dlsite.com/maniax/ranking/month?category=comic"
        url_200 = "https://www.dlsite.com/maniax/ranking/month?category=comic&page=2"
        url_300 = "https://www.dlsite.com/maniax/ranking/month?category=comic&page=3"
        tags_1_100 = self._run(url_100)
        tags_101_200 = self._run(url_200)
        tags_201_300 = self._run(url_300)
        
        return [tags_1_100,tags_101_200,tags_201_300]

    def _run(self,url):
        bs = self.get_bs(url)
        search_tags = bs.select(".search_tag")
        tag_list = []
        for search_tag in search_tags:
            tags = []
            for tag in search_tag.stripped_strings:
                tags.append(tag)
            tag_list.append(tags)
        return tag_list
    
def make_tag_count(tag_list):
    tags = {}
    for search_tag in tag_list:
        for tag in search_tag.stripped_strings:
            if tag not in tags:
                tags[tag] = 1
            else:
                tags[tag] += 1
    tags_sorted = dict(sorted(tags.items(), reverse=True ,key = lambda x: x[1]))
    return tags_sorted

if __name__ == "__main__":
    crawler = MonthDlsiteCrawler()
    crawler.run()