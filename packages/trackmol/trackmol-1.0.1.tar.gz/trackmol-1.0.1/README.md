

<img src="logo_trackmol.png" alt="Logo of trackmol" width="600">

The **trackmol** package offers a set of tools for manipulating, analyzing, and visualizing molecular structures. It is divided into several modules to cover different needs: data analysis, clustering, image processing using computer vision techniques, molecular trajectory generation, and various tools to facilitate the research and development workflow in computational chemistry.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Main Modules](#main-modules)
  - [analysis](#analysis)
  - [clustering](#clustering)
  - [computer_vision](#computer_vision)
  - [generation_walks](#generation_walks)
  - [gratin](#gratin)
  - [tools](#tools)
- [Examples](#examples)
- [Contribution](#contribution)
- [License](#license)

## Installation

You can install **trackmol** from the source repository. Make sure you have Python 3.6 or a later version.

```sh
# Clone the repository
git clone https://your-repository.git
```

The package is structured in the directory [src/trackmol](src/trackmol).

## Usage

Refer to the documentation of each module for more details on the available functions and classes.

## Main Modules
### analysis

Enables analysis of random walk trajectories (MSD...).

### clustering

Allows clustering in latent space and links between latent space and the physical properties of the environment in which the random walks take place.

### computer_vision

Using computer vision techniques, experimental trajectories can be determined from experimentally collected videos. 

### generation_walks

Enables random walk generation both statistically and from a position in latent space by denoising diffusion.

### gratin

Module developed by Institut Pasteur and H. Verdier, which uses graph-based neural networks to classify different random walk models and estimate key walk parameters.

## Exemples

Une série d’exemples illustrant l’utilisation des différents modules se trouve dans le répertoire [src/trackmol/examples](src/trackmol/examples).

## Contribution

Les contributions sont les bienvenues ! Veuillez lire le [CONTRIBUTING.rst](CONTRIBUTING.rst) ainsi que le [docs/contributing.rst](docs/contributing.rst) pour les instructions et les bonnes pratiques de contribution.

Avant de soumettre une pull request, assurez-vous que tous les tests passent et que le code respecte les normes du projet.

## Licence

Ce projet est sous licence [LICENSE](LICENSE). Consultez le fichier pour connaître les détails de la licence.

---

Pour toute question ou contribution, merci de soumettre une issue ou de contacter l’équipe de développement.
