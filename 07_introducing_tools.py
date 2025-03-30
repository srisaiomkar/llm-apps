import gradio as gr
import openai
import json

def get_order_status(order_id):
    order_id_status_map = {
        "100" : "delivered",
        "200" : "ready for pickup",
        "300" : "cancelled",
        "400" : "on the way"
    }
    if order_id in order_id_status_map:
        return order_id_status_map[order_id]
    else:
        return "order id invalid"


order_status_function = {
    "name" : "get_order_status",
    "description" : "gets the order status of the given order id",
    "parameters": {
        "type" : "object",
        "properties" : {
            "order_id" :{
                "type" : "string",
                "description" : "the order id for which you want the status"
            }
        },
        "required": ["order_id"],
        "additionalProperties" : False,
    }
}

tools = [{"type" : "function", "function": order_status_function}]

def chat(input, history):
    system_message = "You are a helpful assistant. If you do not know the answer, say so. Do not make up your own answers"
    messages = [{"role" : "system", "content": system_message}] + history + [{"role" : "user", "content": input}]

    print(messages)

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    if response.choices[0].finish_reason == "tool_calls":
        # sample response.choices[0].tool_calls  object of type: ChatCompletionMessageToolCall
        # [{
        #     "id": "call_12345xyz",
        #     "type": "function",
        #     "function": {
        #         "name": "get_weather",
        #         "arguments": "{\"location\":\"Paris, France\"}"
        #     }
        # }]

        tool_call = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)

        fn_name = tool_call.function.name
        if fn_name == "get_order_status":
            order_id = arguments["order_id"]
            fn_response = get_order_status(order_id)

        messages.append(response.choices[0].message)
        messages.append({"role": "tool", 
            "content" : json.dumps({"order_id" : order_id, "status" : fn_response}),
            "tool_call_id" : tool_call.id})

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

    return response.choices[0].message.content

gr.ChatInterface(fn=chat, type="messages").launch()


# response.choices[0]: Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_lEnA5f1gwbRUbx9nruIILkyR', function=Function(arguments='{"order_id":"100"}', name='get_order_status'), type='function')]))





# order status

# Could you please provide me with the order ID for which you would like to check the status?

# 100

# The status of order ID 100 is "delivered." If you have any more questions or need further assistance, feel free to ask!

# 120

# The order ID 120 is invalid. Please double-check the order ID and try again. If you need further assistance, let me know!
