from db_call import get_matching_car
import json
import os


class IntelligenceSystemCar:
    def ask_question(self):
        cwd = os.getcwd()
        with open(cwd+"/carAPI/question_answer.json") as qaFile:
            q_a = json.load(qaFile)
            qaFile.close()
        print("Tips!!!")
        print(q_a["tips"])
        for i in range(8):
            print(f"\nQuestion {i+1}")
            if i == 3:
                if not("Petrol" in self.user_want["fuel_type"]) or not("Diesel" in self.user_want["fuel_type"]):
                    question = f"q{i+2}"
            question = f"q{i+1}"
            print(q_a[question]["q"])
            if i == 0:
                for index, choice in enumerate(q_a[question]["a"]):
                    answer = int(input(choice))
                    if index == 0 and answer == 0:
                        self.user_want[q_a[question]["key"][index]] = 0
                    elif index == 1 and answer == 1:
                        self.user_want[q_a[question]["key"][index]] = 50000000
                    else:
                        self.user_want[q_a[question]["key"][index]] = answer
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
        print(self.user_want)

    def get_best_match(self):
        return get_matching_car(self.user_want)

    def __init__(self) -> None:
        self.user_want = {
            "min_price": 0,
            "max_price": 0,
            "body_type": [],
            "fuel_type": [],
            "transmission_type": [],
            "color": [],
            "brand": [],
            "minimum_year": 2015,
            "vehicle_size": [],
            "profile": []
        }
        self.ask_question()


def test():
    car = IntelligenceSystemCar()
    best_match = car.get_best_match()

    cwd = os.getcwd()
    file = open(cwd + "/carAPI/test.txt", "w")

    for item in best_match:
        file.write(str(json.dumps(item, indent=4))+'\n')

    file.close()


test()
