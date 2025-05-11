import pickle
import os


def save_state(optimizer, filename="state.pkl"):
    if filename == "state.pkl":
        print("Эй, файл то назови как-то, так не очень, но я все равно сохраню это")
    with open(filename, "wb") as fila:
        pickle.dump(optimizer, fila)
    print(f"State saved to {filename}")


def load_state(filename="state.pkl"):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    with open(filename, "rb") as fila:
        return pickle.load(fila)
