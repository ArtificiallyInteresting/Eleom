from dotenv import load_dotenv
import llm

load_dotenv()

def run_game():
    game_llm = llm.llm()
    while(True):
        action = input("Enter your action: ")
        game_llm.process_action(action)

if __name__ == "__main__":
    print("Running game")
    run_game()