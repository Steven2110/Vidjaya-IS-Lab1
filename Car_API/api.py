from Car_API import db_call as db
import json
import os
import cgi

class IntelligenceSystemCar:
    def ask_question(self):
        cwd = os.getcwd()
        with open(cwd+"/Car_API/question_answer.json") as qaFile:
            q_a = json.load(qaFile)
            qaFile.close()

        print("Tips!!!")
        print(q_a["tips"])

        # Start to ask question
        question_number = 1
        for i in range(9):
            # If user didn't pick "Petrol" or "Diesel" for the fuel type,
            # then don't need to ask for the transmission type.
            # Because all "Electric" car always use "Direct drive" transmission type,
            # and all "Hybird" car always use either "Automatic" or "Automated manual"
            # transmission type.
            if i == 3:
                if "Petrol" in self.user_want["fuel_type"]  or "Diesel" in self.user_want["fuel_type"] or "Any" in self.user_want["fuel_type"]:
                    question = f"q{i+1}"
                else:
                    if "Electric" in self.user_want["fuel_type"] and "Hybrid" in self.user_want["fuel_type"]:
                        self.user_want["transmission_type"] = [
                            "Direct drive", "Automatic", "Automated manual"]
                    elif "Electric" in self.user_want["fuel_type"] and "Hybrid" not in self.user_want["fuel_type"]:
                        self.user_want["transmission_type"] = ["Direct drive"]
                    elif "Electric" not in self.user_want["fuel_type"] and "Hybrid" in self.user_want["fuel_type"]:
                        self.user_want["transmission_type"] = [
                            "Automatic", "Automated manual"]   
                    continue
            else:
                question = f"q{i+1}"

            #Print the question
            print(f"\nQuestion {question_number}")
            print(q_a[question]["q"])

            # Print the answer and ask for input
            # If this is first question which is about min and max price we get 2 input
            if i == 0:
                for index, choice in enumerate(q_a[question]["a"]):
                    answer = int(input(choice))
                    if index == 0 and answer == 0:
                        self.user_want[q_a[question]["key"][index]] = 0
                    elif index == 1 and answer == 1:
                        self.user_want[q_a[question]["key"][index]] = 50000000
                    else:
                        self.user_want[q_a[question]["key"][index]] = answer
            # Else get only 1 input
            else:
                for index, answer in enumerate(q_a[question]["a"]):
                    print(f"{index+1}. {answer}\n")
                answer = input("Please enter your choice: ")
                if i == 6:
                    self.user_want[q_a[question]["key"]
                                   ] = q_a[question]["a"][int(answer)-1]
                else:
                    answers = answer.split(",")
                    for answer in answers:
                        self.user_want[q_a[question]["key"]].append(
                            q_a[question]["a"][int(answer)-1])
            question_number += 1

    def get_best_match(self):
        return db.get_matching_car(self.user_want)

    def get_close_match(self, best_match):
        return db.get_close_car(best_match, self.user_want)

    def __init__(self, user_want) -> None:
        self.user_want = user_want
        self.best_match = []
        self.close_match = []
        # self.ask_question()

# For testing


def test():
    car = IntelligenceSystemCar()
    best_match = car.get_best_match()
    close_match = car.get_close_match(best_match)

    cwd = os.getcwd()
    file1 = open(cwd + "/Car_API/Test_Result_File/test_best_matching_car.txt", "w")
    file2 = open(cwd + "/Car_API/Test_Result_File/test_close_matching_car.txt", "w")

    file1.write(
        f"We found total of {len(best_match)} best matching car for you!\n")
    for index, item in enumerate(best_match):
        file1.write(f"Match no. {index + 1}\n")
        file1.write(str(json.dumps(item, indent=4))+'\n')

    file2.write(
        f"We found total of {len(close_match)} close matching car for you!\n")
    for index, item in enumerate(close_match):
        file2.write(f"Match no. {index + 1}\n")
        file2.write(str(json.dumps(item, indent=4))+'\n')

    file1.close()
    file2.close()

# test()
