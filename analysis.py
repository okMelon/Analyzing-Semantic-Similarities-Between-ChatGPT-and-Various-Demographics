# Comparative analysis of given responses from human surveys vs ChatGPT response.
# Version 0.2
# Aidan Buchanan

import os
import json
from openai import OpenAI
import numpy as np
from scipy.spatial.distance import cosine

client = OpenAI()
RESPONSES = "Data\\responses.json"
EMBEDS = "Data\embeds.json"
COMPARED = "Data\compared.json"
CUSTOMQS = "Data\customsqs.json"


def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)

def save_json(user, filename):
    with open(filename, "w") as file:
        json.dump(user, file, indent=4)

# This function will search all responses for this question q to see if they are the same as the response inputted
# If a response matches perfectly, the embedding for it will be fetched
def has_embedding(users_response, question_number):
    responses = load_json(RESPONSES)
    embeds = load_json(EMBEDS)
    low_input = users_response.lower()
    for response in responses:
        if response[question_number].lower() == low_input:
            print("Cheaper route found: ")
            cheaper_uid = response.get("uid")
            for entry in embeds:
                if entry["uid"] == cheaper_uid:
                    return entry[question_number + "e"]
    return get_embedding(users_response)

# Gets the next uid from uid_counter.txt (an external file that saves what count we are at)
def get_next_uid():
    try:
        # Open in append+read mode to create the file if it doesn’t exist
        with open("uid_counter.txt", "a+") as file:
            file.seek(0)  # Move cursor to the beginning of the file
            content = file.read()

            # If the file is empty, start at 0
            uid = int(content) if content else 0
    except ValueError:
        # If content is invalid, reset to 0
        uid = 0
    # Write the incremented UID back to the file
    with open("uid_counter.txt", "w") as file:
        file.write(str(uid + 1))
    return uid + 1


# Main actual comparer. Grabs the two embeddings of the given questions and sends em through calculate simularity
def compare(uid1, uid2, q):
    responses = load_json(EMBEDS)
    for response in responses:
        if response.get("uid") == uid1:
            r1e = np.array(response.get(q))
        if response.get("uid") == uid2:
            r2e = np.array(response.get(q))
    return calculate_similarity(r1e, r2e)

def compare_all(uid1, uid2):
    q1sim = compare(uid1, uid2, "q1e")
    q2sim = compare(uid1, uid2, "q2e")
    q3sim = compare(uid1, uid2, "q3e")
    q4sim = compare(uid1, uid2, "q4e")
    q5sim = compare(uid1, uid2, "q5e")
    q6sim = compare(uid1, uid2, "q6e")
    q7sim = compare(uid1, uid2, "q7e")
    q8sim = compare(uid1, uid2, "q8e")

    print(f"\nQuestion one has a similarity of {q1sim:.3f}")
    print(f"\nQuestion two has a similarity of {q2sim:.3f}")
    print(f"\nQuestion three has a similarity of {q3sim:.3f}")
    print(f"\nQuestion four has a similarity of {q4sim:.3f}")
    print(f"\nQuestion five has a similarity of {q5sim:.3f}")
    print(f"\nQuestion six has a similarity of {q6sim:.3f}")
    print(f"\nQuestion seven has a similarity of {q7sim:.3f}")
    print(f"\nQuestion eight has a similarity of {q8sim:.3f}")
    print(f"\nOverall similarity is given a score of {(q1sim + q2sim + q3sim + q4sim + q5sim + q6sim + q7sim + q8sim)/8:.4f}")


# This is the core function that will take the users input and store it as a json while converting responses to embeddings
# Once embeddings are collected
def add_user(name, age, gender_identity, ethnicity, education, income, q1, q2, q3, q4, q5, q6, q7, q8):
    responses = load_json(RESPONSES)
    embeds = load_json(EMBEDS)

    q1e = has_embedding(q1, "q1")
    q2e = has_embedding(q2, "q2")
    q3e = has_embedding(q3, "q3")
    q4e = has_embedding(q4, "q4")
    q5e = has_embedding(q5, "q5")
    q6e = has_embedding(q6, "q6")
    q7e = has_embedding(q7, "q7")
    q8e = has_embedding(q8, "q8")

    uid = get_next_uid()

    new_user = {
        "uid": uid,
        "name": name,
        "age": age,
        "gender": gender_identity,
        "ethnicity": ethnicity,
        "education": education,
        "income": income,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8
        }
    new_embedding = {
        "uid": uid,
        "q1e": q1e,
        "q2e": q2e,
        "q3e": q3e,
        "q4e": q4e,
        "q5e": q5e,
        "q6e": q6e,
        "q7e": q7e,
        "q8e": q8e
    }
    responses.append(new_user)
    embeds.append(new_embedding)
    save_json(responses, RESPONSES)
    save_json(embeds, EMBEDS)

def manual_ask():
    n = input("What's your name? ").strip()
    a = str(input("What is your age? "))
    g = str(input("What is your gender identity? "))
    eth = str(input("What is your ethnic background? "))
    edu = str(input("What is the highest level of education you have completed? "))
    inc = str(input("How much total gross income did all members of your household earn in this past fiscal year? "))
    
    question1 = input("What does the phrase: \"Actions speak louder than words\" mean? ").strip()
    question2 = input("What makes someone a good leader? ")
    question3 = input("What are some red flags that idicate someone is untrustworthy? ")
    question4 = input("What does it mean to be successful? ")
    question5 = input("What does it mean to be happy? ")
    question6 = input("Imagine you lost something valuable to you. What would you do? ")
    question7 = input("Complete the prompt: The electrician was... ")
    question8 = input("Billy walked into his kitchen and saw a broken glass on the floor. What do you think happened? ")
    add_user(n, a, g, eth, edu, inc, question1, question2, question3, question4, question5, question6, question7, question8)

# Actual embedding grabber
def get_embedding(text):
    # Grabs text embed for the given phrases
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Main similarity function
def calculate_similarity(text1, text2):
    # Finds cosine similarity between two texts
    # Compute cosine similarity
    similarity = 1 - cosine(text1, text2)  # 1 - cosine distance
    return similarity

def main():
    while True:
        print("\nChatGPT Analysis")
        print("\n1. Manual new response")
        print("\n2. Import responses from CSV")
        print("\n3. Compare two responses")
        print("\n4. Exit")
        
        choice = input("Choose an option: ").strip()
        if choice == "1":
            manual_ask()
        elif choice == "2":
            print("\nNot ready yet")
        elif choice == "3":
            compare_all(int(input("Provide the first uid: ")), int(input("Provide the second uid: ")))
        elif choice == "4":
            break
        else:
            print("\nInvalid choice. Try again.")

if __name__ == "__main__":
    main()