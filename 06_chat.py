import gradio as gr
import openai

def chat(input, history):
    system_message = "You are a helpful assistant. Your job is to tell customer if an " \
    "item is in stock or not. Here are the items which are in stock - blueberries, strawberries, play station 5, tv, " \
    "blackberries. All other items are out of stock."
    messages = [
        {"role" : "system", "content": system_message}
    ]

    # One way to do multi shot prompting. (Another way is you can include some example directly in the system prompt)
    messages.extend(
    [
        {"role" : "user", "content": "are mangoes in stock"},
        {"role" : "assistant", "content": "no"},
        {"role" : "user", "content": "are blueberries in stock"},
        {"role" : "assistant", "content": "yes"}
    ]
    )

    for user_msg, assistant_msg in history:
        messages.append({"role" : "user", "content": user_msg})
        messages.append({"role" : "assistant", "content": assistant_msg})

    messages.append({"role" : "user", "content": input})
    

    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    response = ""
    for chunk in stream:
        response+= chunk.choices[0].delta.content or ""
        yield response

gr.ChatInterface(fn=chat).launch()


# do you have tv in stock

# yes

# blackberries?

# yes

# what about play station

# yes, the Play Station 5 is in stock.

# and xbox 360?

# no, the Xbox 360 is out of stock.
