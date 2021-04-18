import redis
import base64
import string
import random
import URLShortener.config as config
import sys

from base64 import b64encode
from hashlib import blake2b

from flask import jsonify
try:
    import md5
except ImportError:
    from hashlib import md5
    
class UrlShortener:
    def __init__(self):
        self.redis = redis.StrictRedis(host=config.REDIS_HOST,
                                       port=config.REDIS_PORT,
                                       db=config.REDIS_DB)                          
        
    def shortcode(self, url):
        """
        Generating a 5 character long as a URL Code
        """
        url_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    
        return url_code	  

    def shorten(self, url):
        """
        Shortens a url by generating a 5 character 
        """

        try:
            keys = self.redis.keys()
            vals = self.redis.mget(keys)
            
            URLFount = ''
            for keyItem,valItem in zip(keys, vals):
                if valItem is not None and url in valItem.decode("utf-8"):
                    URLCode = keyItem
                    return jsonify({'success': True,
                            'message': 'Duplicated url!',
                            'url': url,
                            'code': keyItem.decode("utf-8"),
                            'shorturl': config.URL_PREFIX +'/'+ keyItem.decode("utf-8")})       
   
            safety = 0
                
            while safety < 10: 
                urlCode = self.shortcode(url)

                if not self.redis.exists(urlCode): 

                    self.redis.set(urlCode, url)
                    return jsonify({'success': True,
                            'url': url,
                            'code': urlCode,
                            'shorturl': config.URL_PREFIX +'/'+ urlCode})
                safety += 1 
                   
         
        except Exception as e:
            return jsonify({'success': False,'message': str(e)})  

    def lookup(self, urlCode):
        """
        The same strategy is used for the lookup than for the
        shortening. Here a None reply will imply either an
        error or a wrong code.
        """
        try:
            if self.redis.exists(urlCode): 
                return self.redis.get(urlCode)
            else:    
                return 'Code doesn\'t exist'
        except Exception as e:
             return jsonify({'success': False,'message': str(e)})

    
    

