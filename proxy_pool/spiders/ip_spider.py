import scrapy

from proxy_pool.items import ProxyPoolItem


class IpSpider(scrapy.Spider):
    name = 'ipspider'

    def start_requests(self):
        urls = [
            'http://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 50)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_dispatch)

    # Dispatch different site to different parser
    def parse_dispatch(self, response):
        item = self.parse_kuaidaili(response)
        yield item

    def parse_kuaidaili(self, response):
        hosts = response.xpath('//td[@data-title="IP"]/text()').extract()
        hosts = list(map(lambda x: "http://" + x, hosts))
        ports = response.xpath('//td[@data-title="PORT"]/text()').extract()
        hosts_ports = list(zip(hosts, ports))
        for host_port in hosts_ports:
            ip = ':'.join(host_port)
            item = ProxyPoolItem()
            item['ip'] = ip
            item['latency'] = 500
            return item
