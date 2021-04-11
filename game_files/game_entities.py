import random


class Snake:
    def __init__(self, segments, direction):
        self.segments = segments
        self.direction = direction

    def move_snake(self, apple_pos):

        if self.direction == "up":
            new_head = (self.segments[0][0], self.segments[0][1]-1)
            self.segments.insert(0, new_head)
            if apple_pos != self.segments[0]:
                self.segments.pop()

        elif self.direction == "down":
            new_head = (self.segments[0][0], self.segments[0][1]+1)
            self.segments.insert(0, new_head)
            if apple_pos != self.segments[0]:
                self.segments.pop()

        elif self.direction == "left":
            new_head = (self.segments[0][0]-1, self.segments[0][1])
            self.segments.insert(0, new_head)
            if apple_pos != self.segments[0]:
                self.segments.pop()

        elif self.direction == "right":
            new_head = (self.segments[0][0]+1, self.segments[0][1])
            self.segments.insert(0, new_head)
            if apple_pos != self.segments[0]:
                self.segments.pop()

    def check_out_of_bounds(self, squares):

        for segment in self.segments:
            if segment[0] < 0 or segment[0] > squares-1 or segment[1] < 0 or segment[1] > squares-1:
                return True
        for i in range(len(self.segments)):
            if self.segments[i] in self.segments[:i]:
                return True
            if self.segments[i] in self.segments[:i]:
                return True

        return False


class Apple:
    def __init__(self, pos):
        self.pos = pos

    def check_if_eaten(self, snake_pos, score, snake_segments, squares):
        if snake_pos == self.pos:

            while self.pos in snake_segments:
                self.pos = (random.randint(0, squares - 1), random.randint(0, squares - 1))

            score += 1
            return score
        else:
            return score