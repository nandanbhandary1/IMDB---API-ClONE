from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 3 # In one page how many 
    page_query_param = "P" # name of the string we utilize for page no by default page
    page_size_query_param = 'size' # customize from client side 
    max_page_size = 10 # U can have max of 10 elements in each page even if u pass ?page=1000
    last_page_strings = 'end' # by default last
    
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 2 # A numeric value indicating the limit to use if one is not provided by the client in a query parameter.
    max_limit = 2 # in one page
    limit_query_param = 'limit'
    offset_query_param = 'start'
    

class WatchListCPagination(CursorPagination):
    page_size = 2 # how many val's to load in a page
    