from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random

app = FastAPI()

GRID_SIZE = 20

class GameState(BaseModel):
    snake: list
    food: dict
    direction: str
    score: int
    alive: bool

class MoveRequest(BaseModel):
    snake: list
    food: dict
    direction: str
    score: int
    alive: bool

def spawn_food(snake):
    while True:
        food = {"x": random.randint(0, GRID_SIZE - 1), "y": random.randint(0, GRID_SIZE - 1)}
        if food not in snake:
            return food

@app.get("/api/new-game")
def new_game():
    snake = [{"x": 10, "y": 10}, {"x": 9, "y": 10}, {"x": 8, "y": 10}]
    return {
        "snake": snake,
        "food": spawn_food(snake),
        "direction": "RIGHT",
        "score": 0,
        "alive": True
    }

@app.post("/api/move")
def move(req: MoveRequest):
    if not req.alive:
        return req.dict()

    snake = req.snake
    direction = req.direction
    food = req.food
    score = req.score

    head = snake[0]
    moves = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    dx, dy = moves[direction]
    new_head = {"x": head["x"] + dx, "y": head["y"] + dy}

    if not (0 <= new_head["x"] < GRID_SIZE and 0 <= new_head["y"] < GRID_SIZE):
        return {**req.dict(), "alive": False}

    if new_head in snake:
        return {**req.dict(), "alive": False}

    snake = [new_head] + snake

    if new_head == food:
        score += 10
        food = spawn_food(snake)
    else:
        snake = snake[:-1]

    return {"snake": snake, "food": food, "direction": direction, "score": score, "alive": True}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
