import requests
import urllib.request

URL = "https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbGVQNzl2aFJ5OVFhQUJMSWNxOUdUeHU0VGFtQXxBQ3Jtc0tscFZpQ1BvTnZtNUVqUWtKV1RUaDZZbTZUTjBNRVlBQnBrUFZyelNReUxZM1hIRXB5Y0FRcW10U1hkUFVmU0h3Zkc5dmxwazhuaUt0a01hd1NLSGpQMWthZUlyMG5SRTlCYko5allaMXlHQzdLU3EtVQ&q=https%3A%2F%2Fhaptik-website-images.haptik.ai%2Fspello_models%2Fen.pkl.zip&v=LEA3TDV98zE"

# res= requests.get(URL)
urllib.request.urlretrieve(URL, "nlp-preprocessing\\en.pkl.zip")



# print(res)

