import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the proxy server
proxies = {
    "http": "http://localhost:9090",
    "https": "http://localhost:9090"
}

try:
    response = requests.get("http://example.com", proxies=proxies)
    logging.info("[+] Proxy Test Successful! Response: ")
    print(response.text[:500])  # Print first 500 characters of the response
except requests.exceptions.RequestException as e:
    logging.error(f"[-] Proxy Test Failed! Error: {e}")
