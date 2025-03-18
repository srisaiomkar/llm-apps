import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import PyPDF2

class JobPage:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')

        if soup.body:
            for element in soup.body(["script", "style", "img", "input"]):
                element.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        print("--------------------------")
        print(self.text)
        print("--------------------------")


class Resume:
    def __init__(self, resume_path):
        with open(resume_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            self.text = ""
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                self.text += page.extract_text()
            print("--------------------------")
            print(self.text)
            print("--------------------------")


    def score(self, job_page: JobPage):
        system_message= "You are a application tracking system resume scorer. Given a resume and \
the job description, score the resume on a scale of 1 to 10 and respond back with that score and a brief \
explanation of why you gave that score."

        user_prompt=f"Here is the resume content: {self.text}\n"
        user_prompt+=f"Here is the job description content: {job_page.text}\n"

        messages = [
            {"role": "system", "content": system_message },
            {"role": "user", "content": user_prompt},
        ]

        openai = OpenAI()
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        print("--------------------------")
        print(response.choices[0].message.content)
        print("--------------------------")




page = JobPage("https://www.metacareers.com/jobs/**********/") # redacted

resume = Resume("/Users/*****/Downloads/***********.pdf") # redacted

resume.score(page)




