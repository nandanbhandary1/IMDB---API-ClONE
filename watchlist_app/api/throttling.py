from rest_framework.throttling import AnonRateThrottle, UserRateThrottle



class ReviewCreteThrottle(UserRateThrottle):
    scope = 'review-create'
        
    
class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
    