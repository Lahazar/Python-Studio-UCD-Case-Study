import pyhtml
import page1B.page_1b

pyhtml.MyRequestHandler.pages["/"] = page1B.page_1b
pyhtml.host_site()