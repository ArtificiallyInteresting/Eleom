from dotenv import load_dotenv
import llm

load_dotenv()

def run_game():
    game_llm = llm.llm()
    done = False
    while(not done):
        action = input("Enter your action: ")
        done = game_llm.process_action(action)

if __name__ == "__main__":
    run_game()