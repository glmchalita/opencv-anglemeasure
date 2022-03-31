
# Python e OpenCV

## Objetivo / descrição do Projeto

Processamento de imagens usando Python e OpenCV. Calcular o ângulo, através do vídeo da webcam, formado pela reta entre as duas maiores circunferências da imagem *circulos.png* e apresentar o resultado.


## Como usar

Para testar o projeto primeiro precisa clona-lo em seu diretório:

> cd /user/pasta<br>
> git clone https://github.com/glmchalita/opencv-nac1.git<br>
> cd opencv-nac1<br>
> dir

e instalar as bibliotecas do *requirements.txt*:
>  pip install -r /diretório/pasta/requirements.txt

Após isso basta imprimir a imagem *circulos.png* e executar o arquivo *webcam.py*.

Irá ser necessário realizar ajustes no alcance do HSV:

    # Mask Circunferência Esquerda
    
    left_lower = np.array([34, 32, 93])
    left_upper = np.array([95, 184, 217])
    left_mask = cv2.inRange(img, left_lower, left_upper)
    
    # Mask Circunferência Direita
    
    right_lower = np.array([105, 139, 30])
    right_upper = np.array([179, 255, 255])
    right_mask = cv2.inRange(img, right_lower, right_upper)
Como auxílio poderá usar a Trackbar, que está comentada no código, e procurar o melhor alcance para o seu vídeo.

## Demonstração em vídeo

Pequena demonstração do projeto em funcionamento.

[Vídeo](https://youtu.be/HQXQnYQGhAw)


### Referências

* [Como usar duas máscaras .inRange()](https://stackoverflow.com/questions/48109650/how-to-detect-two-different-colors-using-cv2-inrange-in-python-opencv)

* [Como calcular área de uma circunferência usando .HoughCircles()](https://stackoverflow.com/questions/62151611/how-can-i-calculate-the-area-of-a-circle-which-i-detected-with-cv2-houghcircles)

* [OpenCV Trackbars](https://youtu.be/SJCu1d4xakQ)
