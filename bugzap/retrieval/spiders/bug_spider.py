from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector as Selector
from retrieval.items import Bug, Comment
from retrieval.spiders.loaders import BugLoader, CommentsLoader


class BugQuerySpider(Spider):
    queries = {
        'bug_table': 'table[class=bz_buglist]',
        'bugs': 'tr[class~=bz_bugitem]',
        'id': 'td[class~=first-child] > a::text',
        'description': 'td[class=bz_short_desc_column] > a::text',
        'product': 'td[class=bz_product_column]::text',
        'component': 'td[class=bz_component_column]::text',
        'status': 'td[class=bz_bug_status_column]::text',
        'assignee': 'td[class=bz_assigned_to_column] > span::text',
        'comments_table': 'table[class=bz_comment_table]',
        'comments': 'div[class~=bz_comment]',
        'commenter': 'span[class=fn]::text',
        'body': 'pre[class~=bz_comment_text]::text'
    }

    url_base = "https://bugzilla.redhat.com/show_bug.cgi?id="
    name = "query.bugzilla"
    allowed_domains = []
    start_urls = []

    def __init__(self, query=None, domain=None, *args, **kwargs):
        """
        Query: The initial Bugzilla query to start the scraping from.
        Domain: The domain for the bugzilla instance to scrape.
        """
        super(BugQuerySpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [domain]
        self.start_urls = [query]

    def parse(self, response):
        """
        :param response:
        """
        self.bugs = self.parse_bugs(response)
        for bug in self.bugs:
            bug['url'] = self.url_base + str(bug['id'])
            yield Request(bug['url'], meta={'item':bug}, callback=self.parse_comments)


    def parse_bugs(self, response):
        """
        :rtype : object
        :param response:
        :return:
        """
        bug_list = []
        sel = Selector(response)
        bugs = sel.css(self.queries['bugs'])
        for b in bugs:
            l = BugLoader(item=Bug(), selector = b, response=response)
            l.add_css('id', self.queries['id'])
            l.add_css('product', self.queries['product'])
            l.add_css('description', self.queries['description'])
            l.add_css('assignee', self.queries['assignee'])
            l.add_css('component', self.queries['component'])
            l.add_css('status', self.queries['status'])
            bug_list.append(l.load_item())
        return bug_list

    def parse_comments(self, response):
        comments_list = []
        sel = Selector(response)
        table = sel.css(self.queries['comments_table'])
        comments = table.css(self.queries['comments'])
        bug = response.request.meta['item']
        for c in comments:
            l = CommentsLoader(item=Comment(), selector = c, response = response)
            l.add_css('commenter', self.queries['commenter'])
            l.add_css('body', self.queries['body'])
            comments_list.append(l.load_item())
        bug['comments'] = comments_list
        yield bug









