import pyhtml
import page1B.page_1b
import page2B.page_2b

pyhtml.MyRequestHandler.pages["/"] = page1B.page_1b
pyhtml.MyRequestHandler.pages["/"] = page2B.page_2b
pyhtml.host_site()