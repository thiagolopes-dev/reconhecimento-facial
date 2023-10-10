import cv2
import dlib
import numpy as np

# Carrega o detector de faces do dlib
detector_faces = dlib.get_frontal_face_detector()

# Carrega o modelo pré-treinado para reconhecimento facial do dlib
modelo_reconhecimento = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Carrega o modelo de detecção de pontos faciais do dlib
modelo_pontos_faciais = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Carrega a imagem de referência
imagem_referencia = cv2.imread("/Users/thiagolopes/Documents/thiagolopes.JPG")
imagem_referencia_rgb = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2RGB)

# Detecta as faces na imagem de referência
faces_referencia = detector_faces(imagem_referencia_rgb)
if len(faces_referencia) == 0:
    raise Exception("Nenhuma face encontrada na imagem de referência.")

# Obtém os pontos faciais da primeira face encontrada na imagem de referência
pontos_referencia = modelo_pontos_faciais(imagem_referencia_rgb, faces_referencia[0])

# Lista de nomes associados aos descritores faciais das pessoas conhecidas
nomes_conhecidos = ["Thiago", "Maria", "João"]  # Adicione aqui os nomes das pessoas conhecidas

# Inicializa a câmera
cap = cv2.VideoCapture(0)

while True:
    # Captura o quadro da câmera
    ret, frame = cap.read()

    # Converte o quadro para RGB (para cálculo dos descritores faciais)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detecta as faces no quadro
    faces_detectadas = detector_faces(frame_rgb)

    for face in faces_detectadas:
        # Obtém os pontos faciais do quadro
        pontos_faciais = modelo_pontos_faciais(frame_rgb, face)

        # Calcula os descritores faciais da imagem de referência e do quadro
        descritor_referencia = modelo_reconhecimento.compute_face_descriptor(imagem_referencia_rgb, pontos_referencia)
        descritor_frame = modelo_reconhecimento.compute_face_descriptor(frame_rgb, pontos_faciais)

        # Calcula a distância euclidiana entre os descritores faciais
        distancias = np.linalg.norm(np.array(descritor_frame) - np.array(descritor_referencia), axis=0)

        # Calcula o percentual de acertividade
        percentual_acertividade = (1 - np.min(distancias)) * 100

        # Define um limite de similaridade
        limite_similaridade = 0.5

        if np.min(distancias) < limite_similaridade:
            # Encontra o índice do descritor mais próximo na lista de descritores conhecidos
            indice_descritor_mais_proximo = np.argmin(distancias)

            # Obtém o nome da pessoa associado ao descritor mais próximo
            nome_pessoa_reconhecida = nomes_conhecidos[indice_descritor_mais_proximo]

            # Exibe o nome da pessoa reconhecida e o percentual de acertividade
            texto = f"{nome_pessoa_reconhecida} ({percentual_acertividade:.2f}% de acertividade)"

            # Obtém as dimensões do texto para criar o fundo preto
            (largura, altura), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)

            # Desenha o fundo preto atrás do texto
            cv2.rectangle(frame, (face.left(), face.top() - 30), (face.left() + largura, face.top()), (0, 0, 0), -1)

            # Escreve o texto verde sobre o fundo preto
            cv2.putText(frame, texto, (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            # Caso contrário, a pessoa não é reconhecida
            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 2)
            cv2.putText(frame, "Pessoa desconhecida", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2)

    # Exibe o quadro com as marcações
    cv2.imshow("Reconhecimento Facial em Tempo Real", frame)

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
