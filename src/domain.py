from urllib.parse import urlparse

# from general url to domain name. Urls can have lots of noise
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split(".")
        final_result = results[-2] + "." + results[-1]
        return final_result
    except:
        return ""
    

def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ""