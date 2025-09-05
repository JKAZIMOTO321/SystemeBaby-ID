# import keyboard

# print("Appuyez sur une touche (Ctrl+C pour quitter):")

# def on_key(event):
#     print(f"Touche appuyée : {event.name}")

# keyboard.on_press(on_key)

# keyboard.wait()  # Attend indéfiniment

import matplotlib.pyplot as plt
import numpy as np


theta = np.linspace(0, 2*np.pi, 1000)
r = np.linspace(0, 4, 1000)
x = r*np.cos(theta)+0.5*np.sin(4*theta)
y = r*np.sin(theta)+0.5*np.cos(4*theta)
# plt.figure(figsize=(8, 8))
plt.title("Graphique en coordonnées polaires")
plt.scatter(x, y, c=theta, cmap='cool', s=3)
plt.axis('equal')
plt.show()
# x = np.linspace(0, 10, 100)
# y = np.sin(x)

# plt.plot(x, y)
# plt.title("Graphique de la fonction sinus")
# plt.xlabel("x")
# plt.ylabel("sin(x)")
# plt.grid()
# plt.show()
