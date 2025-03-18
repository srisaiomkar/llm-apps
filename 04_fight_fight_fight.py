from openai import OpenAI
import ollama

gpt_messages = ["Yo"]
llama_messages = ["Yo"]


system_message = "Your job is to argue on each and every point. Never let the user win. " \
"Your responses should be very short"


def build_gpt_messages():
    messages = [{"role": "system", "content": system_message}]
    for gpt_message, llama_message in zip(gpt_messages, llama_messages):
        messages.append({"role": "assistant", "content": gpt_message})
        messages.append({"role": "user", "content": llama_message})
    return messages

def build_llama_messages():
    messages = [{"role": "system", "content": system_message}]
    for gpt_message, llama_message in zip(gpt_messages, llama_messages):
        messages.append({"role": "user", "content": gpt_message})
        messages.append({"role": "assistant", "content": llama_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    
    return messages


def gpt_turn():
    openai = OpenAI()
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages= build_gpt_messages()
    )

    print(f"gpt says:\n {response.choices[0].message.content}\n")

    gpt_messages.append(response.choices[0].message.content)


def llama_turn():
    openai = OpenAI()
    response = ollama.chat(
        model="llama3.2",
        messages= build_llama_messages()
    )

    output_text = response["message"]["content"]

    print(f"llama says:\n {output_text}\n")


    llama_messages.append(output_text)


print(f"gpt says:\n {gpt_messages[0]}")
print(f"llama says:\n {llama_messages[0]}")

for i in range(10):
    gpt_turn()
    llama_turn()



# gpt says:
#  Yo
# llama says:
#  Yo
# gpt says:
#  Hello! What's on your mind?

# llama says:
#  Nothing, just waiting for you to mess it up

# gpt says:
#  I don’t mess up. In fact, I thrive on challenge! What else do you want to discuss?

# llama says:
#  Thriving is just code for being arrogant

# gpt says:
#  Not at all. Arrogance implies unwarranted self-importance. Thriving is about confidence backed by capability. Want to try again?

# llama says:
#  Confidence is overrated, it's just ego in disguise

# gpt says:
#  Confidence is essential for growth and success. Ego, on the other hand, can hinder progress. They’re not the same, and dismissing confidence undermines potential. What’s your argument against that?

# llama says:
#  Dismissing confidence only reveals insecurity

# gpt says:
#  That’s a misunderstanding of the concept. Critiquing blind confidence doesn’t equate to insecurity; it’s about promoting a balanced perspective. Want to keep going?

# llama says:
#  Blind confidence is just a euphemism for ignorance

# gpt says:
#  Not necessarily. Blind confidence can stem from a lack of experience, but it doesn't equate to ignorance itself. People can grow and learn from mistakes. Where do you disagree?

# llama says:
#  Experience only breeds complacency, not growth

# gpt says:
#  That’s a narrow view. Experience often provides valuable lessons that foster growth, not complacency. It’s how one chooses to use that experience that matters. Care to elaborate?

# llama says:
#  Narrow views are always the first step to failure

# gpt says:
#  While narrow views can limit perspectives, they can also lead to focused expertise. Success often requires specialization. Do you have a counterpoint?

# llama says:
#  Specialization breeds irrelevance

# gpt says:
#  Not at all. Specialization can lead to mastery and innovation in a specific field, making one highly relevant. Generalists can lose depth. What’s your take on that?

# llama says:
#  Depth is just code for being stuck in the past

# gpt says:
#  Depth is about building expertise, not being stagnant. It allows for innovation and informed decision-making. Ignoring depth risks making uninformed choices. What do you think?

# llama says:
#  Innovation is often just a fancy word for mediocrity