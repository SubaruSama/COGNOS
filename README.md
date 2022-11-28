# cognoscere-minacia (COGNOS)

Implementação do projeto final 2. cognoscere do latim, conhecer, e minacia, do latim, ameaça. Ferramenta que tem como objetivo medir o nível de interesse de threat actors em fóruns da deep/dark web que estejam a procura de exploits.

Este projeto utilizou o [Doccano Spacy](https://github.com/FieteO/doccano_spacy) para poder gerar os arquivos necessários para que o [Spacy](https://github.com/explosion/spaCy) pudesse treinar os modelos de NER.

O arquivo [Projeto Final 2](https://github.com/SubaruSama/COGNOS/blob/main/Projeto%20Final%202.ipynb) é o notebook que usei no Google Colab para que fosse possível treinar. Tentei no desktop e notebook porém não deu certo. A ideia é que seja fácil e rápido de treinar, não precisando criar ambientes e contas em terceiros.

O arquivo [generate_train_file.py](https://github.com/SubaruSama/COGNOS/blob/main/generate_train_file.py) modfiquei para o meu uso, então se for dar `git clone` precisa ajustar.
