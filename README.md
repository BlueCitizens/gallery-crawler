# gallery-crawler
这个仓库是我第一次进行Python爬虫的实践，目标是某网站的webp图片。由于该网站大多为静态内容，没有使用框架，所以爬取的难度较低。为规避版权问题隐去了网站地址。

## 设计思路
- 打开第一页，获取标题和pagination信息
- 以标题新建根路径
- 按页数拼接url遍历所有页，解析html标签
- 抓取webp的静态资源地址，并持久化到csv文件
- 遍历图片地址下载所有图片到/webp
- 将webp转换为jpg输出到根路径，并保留源文件在/webp里