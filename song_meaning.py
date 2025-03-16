import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
open_key = os.getenv("OPENAI_API_KEY")



def get_song_meaning(song: str, model: str):

    system_prompt = "You are an assisstant which explains the meaning of any given song lyrics. "

    user_prompt = "Here are the song lyrics: " + song

    messages = [
        {'role': 'system', 'content':  system_prompt},
        {'role': 'user', 'content':  user_prompt},

    ]

    if model == 'gpt-4o-mini':
        print("OOPS! there is going to be some charge now.")
        print("------------------------")
        openai = OpenAI()

        response = openai.chat.completions.create(
            model=model,
            messages=messages
        )

    else:
        ollama_via_openai = OpenAI(base_url="http://localhost:11434/v1", api_key="some_random_text")

        response = ollama_via_openai.chat.completions.create(
            model=model,
            messages=messages
        )

    return response.choices[0].message.content




model = "gpt-4o-mini"
# model = "llama3.2"

text = '''
Ooh
I, I just woke up from a dream
Where you and I had to say goodbye
And I don't know what it all means
But since I survived, I realized
Wherever you go, that's where I'll follow
Nobody's promised tomorrow
So I'ma love you every night like it's the last night
Like it's the last night
If the world was ending, I'd wanna be next to you
If the party was over and our time on Earth was through
I'd wanna hold you just for a while and die with a smile
If the world was ending, I'd wanna be next to you
Ooh
Oh, lost, lost in the words that we scream
I don't even wanna do this anymore
'Cause you already know what you mean to me
And our love's the only war worth fighting for
Wherever you go, that's where I'll follow
Nobody's promised tomorrow
So I'ma love you every night like it's the last night
Like it's the last night
If the world was ending, I'd wanna be next to you
If the party was over and our time on Earth was through
I'd wanna hold you just for a while and die with a smile
If the world was ending, I'd wanna be next to you
Right next to you
Next to you
Right next to you
Oh-oh, oh
If the world was ending, I'd wanna be next to you
If the party was over and our time on Earth was through
I'd wanna hold you just for a while and die with a smile
If the world was ending, I'd wanna be next to you
If the world was ending, I'd wanna be next to you
Ooh
I'd wanna be next to you
'''

print(get_song_meaning(text, model))



# gpt-4o-mini output
# OOPS! there is going to be some charge now.
# ------------------------
# The lyrics you've shared convey a deep sense of love and urgency in the face of uncertainty about the future. Here’s a breakdown of the themes and meanings:

# 1. **Love and Devotion**: The central theme is a profound commitment to a loved one. The singer expresses that no matter where life takes them, they want to be with this person. The line "Wherever you go, that's where I'll follow" emphasizes their dedication and willingness to support their partner.

# 2. **Impermanence**: The phrase "Nobody's promised tomorrow" reflects the uncertainty of life and the idea that time is fleeting. This idea encourages the singer to appreciate every moment with their loved one as if it could be the last.

# 3. **Living in the Moment**: The repeated motif of treating each night like it’s the last hints at a desire to make the most of each shared moment, adding urgency to their affection. 

# 4. **Imagery of Crisis**: The lyrics bring up scenarios where the world is ending or life on Earth is coming to a close. This imagery serves to highlight the importance of connection and love when faced with existential threats. The singer expresses that they would rather face these dire situations together than be alone.

# 5. **Emotional Vulnerability**: The mention of waking up from a dream where they had to say goodbye reveals vulnerability and fear of loss. This fear enhances the richness of the singer's feelings towards their partner.

# 6. **A Love Worth Fighting For**: The line “our love's the only war worth fighting for” implies that despite challenges or conflicts, the love shared is valuable and deserving of effort.

# Overall, the song beautifully captures the essence of treasuring love in the face of uncertainty and cherishing every moment with someone special, especially when contemplating life’s unpredictability.


# LLAMA 3.2 output
# These song lyrics seem to convey a deep sense of devotion, passion, and mortality. The artist is proclaiming their unwavering commitment to this person they love.

# The opening lines "I, I just woke up from a dream / Where you and I had to say goodbye" suggest that the relationship has come to an end at least in the dreaming world. This could be seen as a metaphor for death or separation, which adds depth to the overall sentiment of the song.

# The repetition of "(Wherever you go, that's where I'll follow / Nobody's promised tomorrow)" drives home the idea that despite the uncertainty and unpredictability of life (symbolized by "nobody's promised tomorrow"), this person is willing to always be with their loved one. This declaration shows an intense yearning for connection.

# The lines "(If the world was ending, I'd wanna be next to you)" emphasize how even in the face of catastrophic loss or collapse ("the world was ending"), all that remains would be the love shared between the two individuals. The phrase "I'd die with a smile" is also telling, as it indicates an acceptance and appreciation of mortality alongside one's loved one.

# The final section seems to describe an exhausting emotional battle ("Oh, lost, lost in the words that we scream"), yet at the core, their love remains worth fighting for and standing for.

# In essence, this song can be seen as a heartfelt affirmation of enduring love through difficult times and imperfection.