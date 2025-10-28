# main.py
# pyhtml has the webserver and database connection code
import pyhtml

# Import each page’s content 
import page_1 
import page_2 
import page_3# Level 1A page


# Enables helpful debug messages in the terminal
pyhtml.need_debugging_help = True

# Map each page to a URL path
pyhtml.MyRequestHandler.pages["/"] = page_1  
pyhtml.MyRequestHandler.pages["/page_2.html"]= page_2   
pyhtml.MyRequestHandler.pages["/page_3.html"]= page_3  


# Start the web server — go to http://localhost:8000
pyhtml.host_site()


