from enum import Enum


class Reactions(str, Enum):
  LIKE = "like"
  HEART = "heart"
  DISLIKE = "dislike"
  ANGRY = "angry"
  SAD = "sad"
  