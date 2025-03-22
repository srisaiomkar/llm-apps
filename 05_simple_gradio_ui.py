import gradio as gr
import openai
import ollama

def stream_gpt(prompt):
    system_message="You are a helpful assistant"
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def stream_llama(prompt):
    system_message="You are a helpful assistant"
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = ollama.chat(
        model='llama3.2',
        messages=messages,
        stream=True,
    )
    result = ""
    for chunk in stream:
        result += chunk['message']['content'] or ""
        yield result

def stream_llm(prompt, model):
    if model == "gpt-4o-mini":
        res = stream_gpt(prompt)
    elif model =="llama3.2":
        res = stream_llama(prompt)
    yield from res


view = gr.Interface(
    fn=stream_llm,
    inputs=[gr.Textbox(label="message"), gr.Dropdown(["gpt-4o-mini","llama3.2"],label="model")],
    outputs=[gr.Textbox(label="output")],
    flagging_mode="never"
)

view.launch()