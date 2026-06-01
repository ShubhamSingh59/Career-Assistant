import json

from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class ResumeAnalyzer:
    def __init__(self):
        # Set the apis keys and other configurations
        self.HF_TOKEN = os.getenv("HF_TOKEN")

        self.template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an expert Career Coach and Senior Technical Recruiter. "
                        "Your goal is to analyze a candidate's resume and provide constructive feedback. "
                        "You must ALSO predict the top 3 job titles this candidate is most qualified for. "
                        "CRITICAL: You must output ONLY a valid JSON object. Do not add markdown formatting, "
                        "conversational text, or ```json tags. Just the raw JSON object."
                    ),
                ),
                (
                    "human",
                    (
                        "Analyze the following resume and return a JSON object with this EXACT structure:\n"
                        "{{\n"
                        '  "overall_impression": "A 2-sentence summary of the candidate.",\n'
                        '  "core_strengths": ["Strength 1", "Strength 2", "Strength 3"],\n'
                        '  "areas_for_improvement": ["Improvement 1", "Improvement 2"],\n'
                        '  "ats_readability": "Feedback on layout and structure.",\n'
                        '  "actionable_steps": ["Step 1", "Step 2", "Step 3"],\n'
                        '  "predicted_job_titles": ["Title 1", "Title 2", "Title 3"]\n'
                        "}}\n\n"
                        "Resume Text:\n{resume_text}"
                    ),
                ),
            ]
        )

        self.llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Llama-3.1-8B-Instruct",
            huggingfacehub_api_token=self.HF_TOKEN,
            temperature=0.2,
            max_new_tokens=1000,
        )

        self.model = ChatHuggingFace(llm=self.llm)

        self.parser = StrOutputParser()

        self.chain = self.template | self.model | self.parser

    def analyze_resume(self, resume_text):
        response = self.chain.invoke({"resume_text": resume_text})
        clean_text = response.strip()

        try:
            return json.loads(clean_text.strip())
        except Exception as e:
            return {
                "error": f"Failed to parse JSON: {str(e)}",
                "raw_response": clean_text,
            }
