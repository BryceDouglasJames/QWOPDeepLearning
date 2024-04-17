import time
import sys

sys.path.append('/absolute/path/to/qwop_agent')
from environment import QWOPEnvironment

def main():
    # Initialize the QWOP game environment
    environment = QWOPEnvironment()
    
    try:
        _ = environment.get_player_state()
        _ = environment.get_distance_state()
        environment.press_key("Q", 1)
        environment.press_key("P", 1)
        environment.press_key("W", 1)
        environment.press_key("Q", 1)
        time.sleep(2)
        print(environment.is_game_over())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to close the browser...")
        environment.close()
    

if __name__ == "__main__":
    main()