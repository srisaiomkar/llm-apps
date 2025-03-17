import ollama
import json
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Link(BaseModel):
    title: str
    url: str

class Links(BaseModel):
    links: list[Link]
    

def make_ollama_call(messages, model = "llama3.2"):
    response = ollama.chat(model, messages)
    return response["message"]["content"]

def make_openai_call(messages, model= "gpt-4o-mini"):
    openai = OpenAI()
    response = openai.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content


class Website:
    def __init__(self, url):
        try:
            self.url = url
            self.links = []
            self.text = ""
            response = requests.get(url)
            soup = BeautifulSoup(response.content,'html.parser')

            self.title = soup.title.string if soup.title else "Title not found"

            if soup.body:
                for element in soup.body(["script", "style", "img", "input"]):
                    element.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
            links = [link.get('href') for link in soup.find_all('a')]
            self.links = [link for link in links if link]
        except Exception as e:
            print(e)
            pass


    def get_content(self):
        return f"Webpage with the title {self.title} has the following content:\n {self.text}\n\n"

    def get_relevant_links(self):
        system_prompt = '''
You are provided with a list of links of a website. 
Your job is to find a few links which are most relevant to include in the brochure of the company. 
Do not include any non http links.
Your response should be in json like the following example:
{
    "links": [
        {"title": "about us page", "url": "https://full.url/about"}
        {"title": "career page", "url": "https://careers.full.url.com/"}
    ]
}
'''
        user_prompt = f"Here are the links of the website {self.url} - \n " \
        "Find the most relevant links for the brochure and dont forget to include the complete url. Also respond in json" + "\n".join(self.links)

        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        print("----------")
        print(self.links)
        print("----------")
        print(user_prompt)
        print("----------")
        response = ollama.chat("llama3.2", messages, format=Links.model_json_schema())
        content = response["message"]["content"]


        # openai = OpenAI()
        # response = openai.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=messages,
        #     response_format={"type": "json_object"}
        # )
        # content = response.choices[0].message.content

        return json.loads(content)
    
    def generate_brochure(self):
        system_prompt = '''
Given information about a company, generate a brochure for it. 
The brochure should attract people, talent, and investors across the world and should highlight all the great things about the company. 
Do not include any images. Make sure the response is in proper markdown syntax and is formatted properly.
'''
        user_prompt = f"Generate a brochure for this company. {self.title} using the information below\n Landing page information : {self.text}\n"

        relevant_links = self.get_relevant_links()
        print(relevant_links)
        for link in relevant_links["links"]:
            page = Website(link["url"])
            title = link["title"]
            user_prompt+= f"\n\n {title} page content: {page.text}\n"

        user_prompt = user_prompt[:20000]

        print("----------")
        print(user_prompt)
        print("----------")

        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        print("----------")
        print(messages)

        # openai = OpenAI()
        # response = openai.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=messages,
        #     # response_format={"type": "json_object"}
        # )
        # content = response.choices[0].message.content

        response = ollama.chat("llama3.2", messages)
        content = response["message"]["content"]

        print("-----------------")

        return content
        

# print(Website("https://ollama.com/").__dict__)

website = Website("https://stackoverflow.co/")
print("----------------------------")
print(website.generate_brochure())




# Stack Overflow is a Q&A forum for programmers, developers, and tech enthusiasts. The company was founded in 2008 by Joel Spolsky and Jeff Atwood as a way to connect developers with each other and provide a platform for them to ask and answer questions.

# **Key Features:**

# 1. **Q&A Forum**: A platform where users can ask and answer questions related to programming, software development, and technology.
# 2. **Community-driven**: The site is driven by the community of developers who contribute to its growth and development.
# 3. **Popular topics**: Stack Overflow covers a wide range of topics, including programming languages, frameworks, libraries, databases, and more.
# 4. **APIs and tools**: Stack Overflow provides APIs and tools for developers to integrate into their own applications.
# 5. **Career development**: The site offers resources and tools for career development, such as job boards, resume building, and interview preparation.

# **Company News:**

# 1. **Expansion of Jobs**: Stack Overflow has expanded its international reach through partnerships with Indeed.
# 2. **Partnerships with Google Cloud and OpenAI**: The company has partnered with Google Cloud to bring generative AI to millions of developers.
# 3. **Launch of OverflowAPI**: Stack Overflow's API, which allows developers to build applications that interact with the site.

# **Awards and Recognition:**

# 1. **Best AI API Award at API World 2024**: Stack Overflow's API won an award for being one of the best in its category.
# 2. **Recognition as a Leader in Gartner's Magic Quadrant**: The company has been recognized as a leader in Gartner's Magic Quadrant for Developer Platforms.

# **Statistics:**

# 1. **Millions of users per month**: Stack Overflow attracts millions of visitors each month.
# 2. **Over 50 billion questions answered**: The site has helped developers answer over 50 billion times.
# 3. **77% of developers favor AI tools, but only 48% trust their accuracy**: A recent survey found that while many developers are interested in AI tools, they are skeptical about their accuracy.

# **Leadership:**

# 1. **Jeff Atwood**: Co-founder and CEO of Stack Overflow.
# 2. **Joel Spolsky**: Co-founder and former CEO of Stack Overflow.
# 3. **Ryan Polk**: Chief Product Officer at Stack Overflow.

# **Resources:**

# 1. **Annual Developer Survey**: A report summarizing survey results from the world's largest developer community.
# 2. **Stack Overflow Podcast**: A podcast discussing software development, coding, and technology.
# 3. **Customer Academy**: Resources for developers to improve their skills and knowledge.