# VisionRLCS
## An environment suitable for facilitation the development, training, and testing of a Vision based Reinforcement Learning Control System

### Problem Statement

Implement a reinforcement environment consisting of a vision based, differential wheeled robot and points of interest to either navigate towards or avoid. The objective of the robot is to maximise the number of positive targets, and to minimize the number of negative targets visited.

### Motivation

Humans rely heavily on vision to observe, identify, and devise appropriate courses of action to deal with various objects of interest. It is of key interest to emulate this behaviour in autonomous robots whose targets or points of interest are not confined to a fixed region, and are required to be seeked out and navigated to. While such a task pushes the limits of conventional control systems, it can be achieved through the use of a reinforcement learning based approach, which would be better equipped to combat the increasing scales of complexity. This project implements a modular environment suitable for the training and testing of such an agent, and proposes a simple temporal difference based tabular reinforcement learning approach to solve the aforementioned environment. This kind of environment uses a high level of generalization of any specific tasks to be accomplished by the robot, and hence this in conjunction with transfer learning can be used to generate a basic foundational policy which can be specialized to more specific tasks through further training.

---

### To Use

<kbd>src/main.py</kbd> contains code for the training loop of the RL agent. Any algorithms to be trained must be implemented here. See the contents of the file for the general structure of the implementation. The environment is to be interfaced with through the OpenAI Gym API. Trained weights are saved as <kbd>src/weights.npy</kbd>  
<kbd>src/test.py</kbd> displays a trial run of the trained agents, using the saved weights. In case an alternate solution is implemented, this must also be modified to correctly infer the action from the policy.
All other files in <kbd>src/</kbd> contain the implementation of the environment.

A more thorough treatment of this project is available in <kbd>report/</kbd>

---

Project by *Viraj Shah*
