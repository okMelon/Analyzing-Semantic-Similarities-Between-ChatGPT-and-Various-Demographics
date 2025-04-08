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
LOWBAR = 0

# json loader method
def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)

# json saver method :)
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
    responses = load_json("Data\embeds.json")
    for response in responses:
        if response.get("uid") == uid1:
            r1e = np.array(response.get(q))
        if response.get("uid") == uid2:
            r2e = np.array(response.get(q))
    return calculate_similarity(r1e, r2e) 

# Compares the responses from uid1 and uid2. If stored is true, it will store the responses under uid2.
def compare_all(uid1, uid2, stored):
    q1sim = compare(uid1, uid2, "q1e")
    q2sim = compare(uid1, uid2, "q2e")
    q3sim = compare(uid1, uid2, "q3e")
    q4sim = compare(uid1, uid2, "q4e")
    q5sim = compare(uid1, uid2, "q5e")
    q6sim = compare(uid1, uid2, "q6e")
    q7sim = compare(uid1, uid2, "q7e")
    q8sim = compare(uid1, uid2, "q8e")
    qtsim = (q1sim + q2sim + q3sim + q4sim + q5sim + q6sim + q7sim +q8sim)/8
    if stored == True:
        compared = load_json(COMPARED)
        new_compared = {
            "uid": uid2,
            "r1c": q1sim, 
            "r2c": q2sim,
            "r3c": q3sim,
            "r4c": q4sim,
            "r5c": q5sim,
            "r6c": q6sim,
            "r7c": q7sim,
            "r8c": q8sim,
            "rtc": qtsim
        }
        compared.append(new_compared)
        save_json(compared, COMPARED)
    else:
        print(f"\nQuestion one has a similarity of {q1sim:.3f}")
        print(f"\nQuestion two has a similarity of {q2sim:.3f}")
        print(f"\nQuestion three has a similarity of {q3sim:.3f}")
        print(f"\nQuestion four has a similarity of {q4sim:.3f}")
        print(f"\nQuestion five has a similarity of {q5sim:.3f}")
        print(f"\nQuestion six has a similarity of {q6sim:.3f}")
        print(f"\nQuestion seven has a similarity of {q7sim:.3f}")
        print(f"\nQuestion eight has a similarity of {q8sim:.3f}")
        print(f"\nOverall similarity is given a score of {qtsim:.4f}")

def compare_every(uid1, uid2):
    print(f"Comparing {uid1} and {uid2}, on q1 embeddings")
    q1sim = compare(uid1, uid2, "q1e")
    q2sim = compare(uid1, uid2, "q2e")
    q3sim = compare(uid1, uid2, "q3e")
    q4sim = compare(uid1, uid2, "q4e")
    q5sim = compare(uid1, uid2, "q5e")
    q6sim = compare(uid1, uid2, "q6e")
    q7sim = compare(uid1, uid2, "q7e")
    q8sim = compare(uid1, uid2, "q8e")
    qtsim = (q1sim + q2sim + q3sim + q4sim + q5sim + q6sim + q7sim +q8sim)/8
    return q1sim, q2sim, q3sim, q4sim, q5sim, q6sim, q7sim, q8sim, qtsim

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
    responses.append(new_user)
    save_json(responses, RESPONSES)
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
    embeds.append(new_embedding)
    save_json(embeds, EMBEDS)
    # Since we are adding a user, we will also calculate their similarity to ChatGPT
    compare_all(1, uid, True)
    

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

# For custom questions, we need to be able to ask ChatGPT the new questions.
# Adding token count as an input later on would be good. That way I could change the amount of sentences the user wants generated.
def ask_gpt(question):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        max_tokens=100
    )

    return completion.choices[0].message.content

# For asking ChatGPT questions not listed in the survey and comparing the response to the question poser's response
# When adding token count as an input to ask_gpt() method, also add it as an input here.
def bonus_questions(question, human_response):
    chatgpt_response = str(ask_gpt(question))
    chatgpt_embedding = get_embedding(chatgpt_response)
    human_embedding = get_embedding(human_response)
    similarity = calculate_similarity(chatgpt_embedding, human_embedding)

    custom = load_json(CUSTOMQS)
    new_custom = {
        "Question": question,
        "Human Response": human_response,
        "ChatGPT Response": chatgpt_response,
        "Similarity": similarity
    }
    custom.append(new_custom)
    save_json(custom, CUSTOMQS)
    return chatgpt_response, similarity



def create_graph_data():
    responses = load_json(RESPONSES)
    demos = [[[],[],[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]]
    # Three dimensions
    # First dimension is either 0 - age, 1 - gender, 2 - ethnicity, 3 - education, 4 - income
    for r in responses:
        # Age 0: 18-24, 1: 25-34, 2: 35-44, 3: 45-54, 4: 55-64, 5: 65+, 6: unlisted
        try:
            int_age = int(r["age"])
            if 18 <= int_age <= 24:
                demos[0][0].append(r["uid"])
            elif 25 <= int_age <= 34:
                demos[0][1].append(r["uid"])
            elif 35 <= int_age <= 44:
                demos[0][2].append(r["uid"])
            elif 45 <= int_age <= 54:
                demos[0][3].append(r["uid"])
            elif 55 <= int_age <= 64:
                demos[0][4].append(r["uid"])
            elif int_age >= 65:
                demos[0][5].append(r["uid"])
            else:
                demos[0][6].append(r["uid"])
                print(f"\nCorrect value type. Not in range of responses: {r['uid']}, age: {r['age']}")
            print(f"Age as int is: {int_age}")
        except (ValueError, TypeError):
            demos[0][6].append(r["uid"])
            print(f"\nUnlisted: {r['uid']}, age: {r['age']}")
        
        
        # Gender 0: Male, 1: Female, 2: Non-binary, 3: Prefer not to say/Other, 4: unlisted
        try:
            if r["gender"] == "Male":
                demos[1][0].append(r["uid"])
            elif r["gender"] == "Female":
                demos[1][1].append(r["uid"])
            elif r["gender"] == "Non-binary":
                demos[1][2].append(r["uid"])
            elif r["gender"] == "Prefer not to say/Other":
                demos[1][3].append(r["uid"])
            else:
                demos[1][4].append(r["uid"])
                print(f"\nCorrect value type. Not in range of responses: {r['uid']}, gender: {r['gender']}")
        except (ValueError, TypeError):
            demos[1][4].append(r["uid"])
            print(f"\nUnlisted: {r['uid']}, gender: {r['gender']}")
                
        # Ethnicity 0: White/Caucasian, 1: Asian - Eastern, 2: Asian - Indian, 3: Hispanic, 4: Black, 5: Native American, 6: Prefer not to answer, 7: unlisted
        try:
            if r["ethnicity"] == "White/Caucasian":
                demos[2][0].append(r["uid"])
            elif r["ethnicity"] == "Asian - Eastern":
                demos[2][1].append(r["uid"])
            elif r["ethnicity"] == "Asian - Indian":
                demos[2][2].append(r["uid"])
            elif r["ethnicity"] == "Hispanic":
                demos[2][3].append(r["uid"])
            elif r["ethnicity"] == "Black":
                demos[2][4].append(r["uid"])
            elif r["ethnicity"] == "Native American":
                demos[2][5].append(r["uid"])
            elif r["ethnicity"] == "Prefer not to answer":
                demos[2][6].append(r["uid"])
            else:
                demos[2][7].append(r["uid"])
                print(f"\nCorrect value type. Not in range of responses: {r['uid']}, ethnicity: {r['ethnicity']}")
        except (ValueError, TypeError):
            demos[2][7].append(r["uid"])
            print(f"\nUnlisted: {r['uid']}, ethnicity: {r['ethnicity']}")
        # Education 0: Highschool Diploma, 1: Bachelor's Degree, 2: Master's Degree, 3: Prefer not to answer, 4: Lower than highschool level education, 5: unlisted
        try:
            if r["education"] == "Highschool Diploma":
                demos[3][0].append(r["uid"])
            elif r["education"] == "Bachelor's Degree":
                demos[3][1].append(r["uid"])
            elif r["education"] == "Master's Degree":
                demos[3][2].append(r["uid"])
            elif r["education"] == "Prefer not to answer":
                demos[3][3].append(r["uid"])
            elif r["education"] == "Lower than highschool level education":
                demos[3][4].append(r["uid"])
            else:
                demos[3][5].append(r["uid"])
                print(f"\nCorrect value type. Not in range of responses: {r['uid']}, income: {r['education']}")
        except (ValueError, TypeError):
            demos[3][5].append(r["uid"])
            print(f"\nUnlisted: {r['uid']}, education: {r['education']}")
        # Income 0: $0 - $4,999, 1: $5,000 - $7,499, 2: $7,500 - $9,999, 3: $10,000 - $12,499, 4: $12,500 - $14,999, 5: $15,000 - $19,999
        # 6: $20,000 - $24,999, 7: $25,000 - $29,999, 8: $30,000 - $34,999, 9: $35,000 - $39,999, 10: $40,000 - $49,999, 11: $50,000 - $59,999 
        # 12: $60,000 - $74,999, 13: $75,000 - $99,999, 14: $100,000 - $149,999, 15: $150,000+, 16: Prefer not to answer, 17: unlisted
        try:
            if r["income"] == "$0 - $4,999":
                demos[4][0].append(r["uid"])
            elif r["income"] == "$5,000 - $7,499":
                demos[4][1].append(r["uid"])
            elif r["income"] == "$7,500 - $9,999":
                demos[4][2].append(r["uid"])
            elif r["income"] == "$10,000 - $12,499":
                demos[4][3].append(r["uid"])
            elif r["income"] == "$12,500 - $14,999":
                demos[4][4].append(r["uid"])
            elif r["income"] == "$15,000 - $19,999":
                demos[4][5].append(r["uid"])
            elif r["income"] == "$20,000 - $24,999":
                demos[4][6].append(r["uid"])
            elif r["income"] == "$25,000 - $29,999":
                demos[4][7].append(r["uid"])
            elif r["income"] == "$30,000 - $34,999":
                demos[4][8].append(r["uid"])
            elif r["income"] == "$35,000 - $39,999":
                demos[4][9].append(r["uid"])
            elif r["income"] == "$40,000 - $49,999":
                demos[4][10].append(r["uid"])
            elif r["income"] == "$50,000 - $59,999":
                demos[4][11].append(r["uid"])
            elif r["income"] == "$60,000 - $74,999":
                demos[4][12].append(r["uid"])
            elif r["income"] == "$75,000 - $99,999":
                demos[4][13].append(r["uid"])
            elif r["income"] == "$100,000 - $149,999":
                demos[4][14].append(r["uid"])
            elif r["income"] == "$150,000+":
                demos[4][15].append(r["uid"])
            elif r["income"] == "Prefer not to answer":
                demos[4][16].append(r["uid"])
            else:
                demos[4][17].append(r["uid"])
                print(f"\nCorrect value type. Not in range of responses: {r['uid']}, income: {r['income']}")
        except (ValueError, TypeError):
            demos[4][17].append(r["uid"])
            print(f"\nUnlisted: {r['uid']}, income: {r['income']}")
    return demos

# Take the average rc (response compared) value of demos uid grouping
# uids will be a passed in value like demos[4][16]
# rc will be response compared choice. Input like "rtc" or "r1c"
def average_dem(uids, rc):
    compared = load_json(COMPARED)
    rcs = []
    if uids == "":
        return 0
    for r in compared:
        if r["uid"] in uids:
            if r[rc] > LOWBAR:
                rcs.append(r[rc])
    try:
        avg = sum(rcs)/len(rcs)
    except (ZeroDivisionError):
        return 0
    return avg

def main():
    while True:
        print("\nChatGPT Analysis")
        print("\n1. Manual new response")
        print("\n2. Create a new question and check similarity")
        print("\n3. Compare two responses")
        print("\n4. Generat graph data")
        print("\n5. Exit")
        
        choice = input("Choose an option: ").strip()
        if choice == "1":
            manual_ask()
        elif choice == "2":
            chatgpt_response, similarity = bonus_questions(input("What question do you have?"), input("What is your response to the question?"))
            print(f"ChatGPT response: {chatgpt_response}\nSimilarity: {similarity}")
        elif choice == "3":
            compare_all(int(input("Provide the first uid: ")), int(input("Provide the second uid: ")), False)
        elif choice == "4":
            demos = create_graph_data()
            print (demos)
        elif choice == "5":
            break
        else:
            print("\nInvalid choice. Try again.")

if __name__ == "__main__":
    main()