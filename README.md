# Some experimentations with PyGame

## Quick tests

All this section contains very quick experimentations.

| Name of the script            | Description
|--                             |--
| move_rect_with_keyboard.py    | Just a rectangle that moves with keyboard
| crocomath.py                  | A Math Game with a man trying to not be eaten by a crocodile


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


## Video Adventure Game

A game engine to provide a [video adventure game](./src/video_adventure_game/README.md).
