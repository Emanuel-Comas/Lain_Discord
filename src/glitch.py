import random

# Símbolos glitch suaves
soft_symbols = [
    "̷","̸","̶","̴","͏","̀","́","͘","͜",
    "̼","̩","̗","̖","̍","͂","̐"
]

# Símbolos glitch fuertes
hard_symbols = [
    "҉","҇","҈","※","✦","✧"
]

def glitch(text, intensidad=2, legible=True):
    result = ""

    for char in text:
        result += char

        # Probabilidad reducida si es modo legible
        if legible:
            chance = 0.2  # 20% de los caracteres tendrán glitch
        else:
            chance = 1.0  # todos glitch

        if random.random() < chance:
            # pocos símbolos, no tantos
            for _ in range(random.randint(0, intensidad)):
                result += random.choice(soft_symbols)

            # uno fuerte con baja probabilidad
            if random.random() < 0.10:
                result += random.choice(hard_symbols)

    return result
