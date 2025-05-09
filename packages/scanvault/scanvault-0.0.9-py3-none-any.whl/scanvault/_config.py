URL = "https://api.scanvault.in"

def get_api_url():
    # Decode the base64-encoded URL
    
    # Return the decoded URL
    if URL:
        return URL
    else:
        # If URL is not set, return a default or raise an error
        raise ValueError("API URL is not set. Please configure the API URL.")