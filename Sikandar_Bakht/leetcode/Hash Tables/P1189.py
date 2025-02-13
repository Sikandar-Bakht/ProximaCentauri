def maxNumberOfBalloons(text):
    
    counter = {"b":0, "a":0, "l":0, "o":0, "n":0}
    for char in text:
        if char in counter:
            counter[char] += 1
    counter["l"] //= 2
    counter["o"] //= 2
    return min(counter.values())