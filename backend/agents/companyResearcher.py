from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import json

load_dotenv()


class CompanyResearcher:
    def __init__(self):
        self.HF_TOKEN = os.getenv("HF_TOKEN")

        self.template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an expert Corporate Researcher. Your job is to take raw search engine "
                        "results about a company and synthesize them into a clean, professional summary "
                        "for a job applicant. Focus on company culture, recent news, and employee sentiment. "
                        "Write in clear paragraphs. Do NOT use JSON formatting, and do NOT use bullet points."
                    ),
                ),
                (
                    "human",
                    (
                        "Company Name: {company_name}\n\n"
                        "Raw Search Results:\n{search_results}\n\n"
                        "Based on the search results above, write a plain text summary covering: "
                        "a brief overview of what the company does, recent news and projects, "
                        "employee sentiment and culture, and a few interview talking points. "
                        "Write this as continuous, readable paragraphs without any bullet points."
                    ),
                ),
            ]
        )

        self.llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Llama-3.1-8B-Instruct",
            huggingfacehub_api_token=self.HF_TOKEN,
            temperature=0.2,
            max_new_tokens=600,
        )

        self.model = ChatHuggingFace(llm=self.llm)

        self.parser = StrOutputParser()

        self.chain = self.template | self.model | self.parser

    def research_company(self, company_name: str):
        try:
            api_wrapper = DuckDuckGoSearchAPIWrapper(time=None) 
            search_tool = DuckDuckGoSearchRun(api_wrapper=api_wrapper)
            query = f"{company_name} company culture employee reviews recent news"
            
            search_results = search_tool.run(query)
            
            result = self.chain.invoke({
                "company_name": company_name,
                "search_results": search_results
            })
            
            # Just return the raw string, no JSON parsing needed
            return result.strip()

        except Exception as e:
            return {"error": f"Failed to research company: {str(e)}"}
