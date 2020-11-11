import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
import serial

# Configuração da conexão
conexao = serial.Serial('COM5', 9600)

# PATH DO TESSERACT E CARREGAR A IMAGEM DO CARRO
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img = cv2.imread('images/carro2.jpg')
cv2.imshow('original', img)
cv2.waitKey(0)
# REALIZANDO UM BLUR BILATERAL PARA REDUZIR O RUIDO DA IMAGEM, PARA QUE O ALGORITMO
# DO CANNY EDGES TENHA MAIOR FACILIDADE PARA ENCONTRAR OS CONTORNOS RELEVANTES
bilateral = cv2.bilateralFilter(img, 9, 75, 75)
cv2.imshow('original', bilateral)
cv2.waitKey(0)
# TRANSFORMANDO A IMAGEM COM BLUR PARA CINZA, PARA QUE AS CORES NÃO INTERFIRAM
gray = cv2.cvtColor(bilateral,cv2.COLOR_BGR2GRAY)
cv2.imshow('original', gray)
cv2.waitKey(0)
# UTILIZANDO O ALGORITMO CANNY EDGES, PARA TRAZER OS CONTORNOS DA IMAGEM
# CANNY GERA UMA IMAGEM DE FUNDO PRETO COM TODOS OS CONTORNOS ENCONTRADOS NA IMAGEM
edged = cv2.Canny(gray, 30, 200)
cv2.imshow('original', edged)
cv2.waitKey(0)
contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# LISTA DE CONTORNOS GERADA
print('numero de contornos encontrados: ', len(contours))
largest_rectangle = [0,0]
for cnt in contours:
    # REALIZA UMA APROXIMAÇÃO DOS CONTORNOS DISPONIVEIS,
    # TENTANDO GERAR O MAIS PRÓXIMO DE UM POLIGONO
    approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
    # PROCURANDO UM CONTORNO DE QUATRO LADOS NO POLIGONO GERADO
    # VISANDO QUE AS PLACAS SÃO RETANGULOS, PROCURAMOS UM POLIGONO DE 4 FACES.
    if len(approx)==4:
        area = cv2.contourArea(cnt)
        if area > largest_rectangle[0]:
            # PROCURANDO CONTORNO DE MAIOR AREA.
            largest_rectangle = [cv2.contourArea(cnt), cnt, approx]

# PARAMETROS PARA DESENHAR UM RETANGULO AO REDOR DA PLACA
x,y,w,h = cv2.boundingRect(largest_rectangle[2])
# REALIZAÇÃO DO CROP DA PLACA.
roi=img[y:y+h,x:x+w]
# PLOTANDO O ROI GERADO DA PLACA
plt.imshow(roi, cmap = 'gray')
plt.show()

cv2.destroyAllWindows()
# CAPTURA DOS CARACTERES DA PLACA, DENTRO DE UMA LISTA DE POSSIVEIS CHARACTERES,
# SENDO DE A~Z E 0~9, SEM CHARACTERES ESPECIAIS
text = pytesseract.image_to_string((roi), config='--psm 13 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
text = text[:-2]
print("Placa: ", text)

if('LTN6783' == text):
    conexao.write(b'G')
else:
    conexao.write(b'R')

result = conexao.readline()
result = result.decode("utf-8")
print("Resultado:", result[:(len(result)-2)], "\n")
conexao.write(b'F')
conexao.close()
