# subtitle_splitter_fr

Ce projet Python a pour objectif de diviser des textes en sous-titres de manière intelligente en utilisant un modèle de machine learning basé sur ONNX et la librairie Transformers. Il est particulièrement adapté au français.

## Utilisation

Voici un exemple simple d'utilisation de la classe `Spliter` :

```python
from subtitle-splitter-fr.splitter import Splitter

if __name__ == "__main__":
    splitter = Splitter()
    texte_exemple = "Le château se dressait sur une colline escarpée, dominant la vallée sinueuse où la rivière serpentait lentement, reflétant les rayons du soleil couchant. À l'intérieur, de vastes salles résonnaient du silence des siècles passés, tandis que des tapisseriesComplexes ornaient les murs de pierre froide, racontant des histoires oubliées de chevaliers et de dames. Dehors, le vent murmurait à travers les arbres centenaires, emportant avec lui les échos d'un temps révolu."
    sous_titres = splitter.split(texte_exemple)

    print("\nSous-titres générés :")
    for i, sub in enumerate(sous_titres):
        print(f"{i + 1}: {sub} ({len(sub)} chars)")
```