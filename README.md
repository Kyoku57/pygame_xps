# Some experimentations with PyGame

## Quick tests

All this section contains very quick experimentations.

| Name of the script            | Description
|--                             |--
| move_rect_with_keyboard.py    | Just a rectangle that moves with keyboard
| crocomath.py                  | A Math Game with a man trying to not be eaten by a crocodile
| tiraprout.py                  | A Math Game with a target and arrow
| jeuxdelavie.py                | A Game of Life with parameters

## CrocoMath

This game was created with https://claude.ai

with the following prompt:
```
Peux tu me faire un petit jeu avec pygame qui affiche un bonhomme poursuivi sur un pont de 25 planches, par un crocodile. Le jeu propose au tour à tour, 25 fois, à un joueur de faire une multiplication de deux nombres entre 0 et 10. * *
* *le crocodile se trouve à 5 planches derrière le joueur * 
* Si le joueur a juste, il avance d'une planche. Le crocodile aussi.
* Si le joueur a répondu en moins de 5 secondes, alors il avance d'une planche supplémentaire mais pas le crocodile
* Si le joueur a mal répondu, il n'avance pas, mais le crocodile avance d'une planche
* Si le joueur a répondu trop lentement au dessus de 15 secondes, le crocodile avance d'une planche supplémentaire.
* Si le joueur arrive à la fin du pont avant le crocodile, le joueur a gagné !
* Sinon ben le crocodile l'a bouffé
```

## Tiraprout

This game was created with https://claude.ai

with the following prompt:

```
Je veux un jeu avec pygame, ou on tire des flèches et il y a une cible avec des nombres. Il faut tirer au moins 2 flèches sur la cible et après avoir tirer les flèches, il y aura une question qui additionne ou multiplie les deux nombres. Et il faut répondre en trentes secondes sinon, il y a un prout qui va surgir. Et si on gagne, il y  aura des confettis. Et si on se trompe, il y aura aussi des prouts

...

dès que la fenetre apparait, elle se referme. QUe doit on modifier dans le code ?

...

le test fonctionne mais le code modifié provoque toujours le même soucis

...

Le test fonctionne et le résultat de ton code modifié est le suivant
pygame 2.6.1 (SDL 2.28.4, Python 3.12.3)
Hello from the pygame community. https://www.pygame.org/contribute.html
Jeu réinitialisé
Jeu initialisé avec succès!
Démarrage du jeu...
Jeu fermé

Il se ferme directement
```


## Video Adventure Game

A game engine to provide a [video adventure game](./src/video_adventure_game/README.md).
