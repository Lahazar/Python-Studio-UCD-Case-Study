# main.py
# pyhtml has the webserver and database connection code
import pyhtml

# Import each page’s content 
import page_1 
import page_2 
import page_3# Level 1A page

import page1B.page_1b
import page2B.page_2b
import page3B.page_3b


# Enables helpful debug messages in the terminal
pyhtml.need_debugging_help = True

# Map each page to a URL path
pyhtml.MyRequestHandler.pages["/"] = page_1  
pyhtml.MyRequestHandler.pages["/page_2.html"]= page_2   
pyhtml.MyRequestHandler.pages["/page_3.html"]= page_3
pyhtml.MyRequestHandler.pages["/page1b.html"] = page1B.page_1b
pyhtml.MyRequestHandler.pages["/page2b.html"] = page2B.page_2b
pyhtml.MyRequestHandler.pages["/page3b.html"] = page3B.page_3b



# Start the web server — go to http://localhost:8000
pyhtml.host_site()


