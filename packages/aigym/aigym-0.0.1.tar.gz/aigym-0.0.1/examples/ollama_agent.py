"""Example usage of the Web Gym environment."""

from typing import Generator

import ollama
import tiktoken
from rich import print as rprint
from rich.panel import Panel

import aigym.pprint as pprint
from aigym.agent import Agent
from aigym.env import WikipediaGymEnv


def main():
    enc = tiktoken.get_encoding("cl100k_base")

    def generate_function(prompt: str) -> Generator[str, None, None]:
        for chunk in ollama.generate(
            model="gemma3:27b",
            prompt=prompt,
            stream=True,
            options={
                "temperature": 1.25,
            },
        ):
            yield chunk.response

    agent = Agent(
        generate_function=generate_function,
        token_encoder=enc,
        n_retries_per_action=20,
        url_boundaries=["https://en.wikipedia.org"],
    )

    env = WikipediaGymEnv(n_hops=2, lines_per_chunk=None)
    observation, info = env.reset()
    rprint(f"reset current page to: {observation.url}")

    for step in range(1, 101):
        pprint.print_observation(observation)
        pprint.print_context(observation)
        action = agent.act(observation)
        pprint.print_action(action)
        observation, reward, terminated, truncated, info = env.step(action)
        rprint(
            f"Next observation: {observation.url}, position {observation.current_chunk} / {observation.total_chunks}"
        )
        if terminated or truncated:
            rprint(Panel.fit(f"Episode terminated or truncated at step {step}", border_style="spring_green3"))
            break

    rprint("Task finished!")
    env.close()


if __name__ == "__main__":
    main()
