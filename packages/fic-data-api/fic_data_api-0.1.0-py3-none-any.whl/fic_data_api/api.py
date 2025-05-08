"""
 * @Author：cyg
 * @Package：api
 * @Project：Default (Template) Project
 * @name：api
 * @Date：2025/5/8 09:52
 * @Filename：api
"""

import requests


class FicDataApi:
	def __init__(self, token):
		self.api_url = "http://127.0.0.1:5001"
		self.token = token
	
	def get_data(self, post_id):
		if not self.token:
			raise ValueError("Token has not been set")
		
		url = f"{self.api_url}/posts/{post_id}"
		headers = {"Authorization": f"Bearer {self.token}"}
		response = requests.get(url, headers=headers)
		
		if response.status_code == 200:
			return response.json()
		else:
			print(f"Failed : {response.status_code}")
			return None
