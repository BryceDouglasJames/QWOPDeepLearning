import time
import sys

sys.path.append('qwop_agent')
from environment import QWOPEnvironment
from agent import PPOAgent

def main():
    agent = PPOAgent()
    agent.train(total_episodes=100)
    agent.close()

if __name__ == "__main__":
    main()