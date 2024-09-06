from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def get_llm_response(prompt, max_tokens=1):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        # model="llama3-70b-8192",
        model="llama-3.1-70b-versatile",
        temperature=0.0,
        max_tokens=max_tokens,
        # model="llama3-8b-8192",
        # model="mixtral-8x7b-32768",
    )
    return chat_completion.choices[0].message.content



def get_dataset():
    with open('dataset/dataset.txt', 'r') as file:
        text = file.read()

    return text


#  prompt = f"""Generate a report for {crop_type} crop with the following conditions: \n"
# Temperature: {temperature}
# Humidity: {humidity}
# Wind Speed: {wind_speed}
# Percipitation: {percipitation}
# Sunchine: {sunchine}
# Growth Stage: {growth_stage}
# Irregation Method: {irregation_method}

# The output should be a json object with the following fields:
# - irregation_frequency: how often the crop should be irregated in days (int)
# - irregation_amount: how much water should be used for irregation in every square meter (mm) (float)

# Rules:
# - Output a thourough explanation (300 words) of how the values were calculated below the json object.
# - Use the following prefix for the json object string: "JSON: "
# - Output the json object in one line.
# - The json object should be the last line of the output.


# def clean_response(response):
#     explanation = response.split('JSON: ')[0].strip()
#     json_str = response.split('JSON: ')[1]
#     json_str = response.replace('\n', '').strip()

#     return explanation, json_str
