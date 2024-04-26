### Snake Reinforcement Learning 🐍🎮

Welcome to Snake Reinforcement Learning, a Python implementation of the classic Snake game using reinforcement learning techniques. This project aims to train an AI agent to play the game of Snake effectively by learning from its past experiences.

### Features

- Utilizes reinforcement learning (Q-learning) to train the Snake AI.
- Pygame-based graphical interface for visualizing the game.
- Adjustable game parameters such as learning rate, discount factor, and exploration rate.
- Training progress visualization with matplotlib.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Rishit-katiyar/snake-reinforcement-learning.git
   ```

2. Navigate to the project directory:
   ```bash
   cd snake-reinforcement-learning
   ```

3. Install the required dependencies:
   ```bash
   pip install pygame numpy matplotlib
   ```

4. (Optional) Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate
   ```

5. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

To train the Snake AI, run the following command:
```bash
python fast-snake_reinforcement_learning + QL plot.py
```

### Instructions

1. **Game Controls:**
   - Use the arrow keys to control the movement of the Snake.
   - Press `Q` to quit the game.

2. **Training:**
   - During training, the Snake AI learns to navigate the game environment and maximize its score.
   - Training progress is displayed in the console and visualized using matplotlib.

3. **Gameplay:**
   - The Snake AI attempts to eat the food items while avoiding obstacles and its own body.
   - The game ends if the Snake collides with a wall, obstacle, or itself.

### Customize

Feel free to customize the following parameters in the `SnakeGame` class of the `snake_reinforcement_learning.py` file:

- `numEpisodes`: Number of episodes to train the Snake AI.
- Learning parameters: Adjust the learning rate (`lr`), discount factor (`gamma`), and exploration rate (`epsilon`) to optimize the training process.

### Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please open an issue or submit a pull request.

### License

This project is licensed under the GNU GPLv3 License. See the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Inspired by the classic Snake game and reinforcement learning principles.
- Developed with Python, Pygame, numpy, and matplotlib.

### Enjoy playing and happy coding! 🎉🐍
