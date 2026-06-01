from dotenv import load_dotenv
import os

import requests

load_dotenv()

class JobFinder:
    def __init__(self):
        self.APP_ID = os.getenv("APP_ID")
        self.APP_KEY = os.getenv("APP_KEY")
        self.ROOT_URL = os.getenv("ROOT_URL")
        self.country = "in" 

    def find_jobs(self, job_title, location, results_per_page=10):
        
        if not self.APP_ID or not self.APP_KEY or not self.ROOT_URL:
            raise ValueError("API credentials or ROOT_URL are not set in environment variables.")
        
        search_url = f"{self.ROOT_URL}/jobs/{self.country}/search/1"
        
        params = {
            "app_id": self.APP_ID,
            "app_key": self.APP_KEY,
            "results_per_page": results_per_page,
            "what": job_title,
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            raw_jobs = data.get("results", [])
            
            cleaned_jobs = []
            for job in raw_jobs:
                cleaned_jobs.append({
                    "job_title": job.get("title"),
                    "company": job.get("company", {}).get("display_name", "Unknown"),
                    "location": job.get("location", {}).get("display_name", "Unknown"),
                    "link": job.get("redirect_url"),
                    "money": job.get("salary_is_predicted"),
                    "description": job.get("description", "Unavailable")
                })
                
            return cleaned_jobs
        
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}