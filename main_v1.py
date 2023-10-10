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
imagem_referencia = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2RGB)

# Converte a imagem de referência para escala de cinza
imagem_referencia_cinza = cv2.cvtColor(imagem_referencia, cv2.COLOR_RGB2GRAY)

# Detecta as faces na imagem de referência
faces_referencia = detector_faces(imagem_referencia_cinza)

# Obtém os pontos faciais da primeira face encontrada na imagem de referência
pontos_referencia = modelo_pontos_faciais(imagem_referencia_cinza, faces_referencia[0])

# Inicializa a câmera
cap = cv2.VideoCapture(0)

while True:
    # Captura o quadro da câmera
    ret, frame = cap.read()

    # Converte o quadro para escala de cinza
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta as faces no quadro
    faces_detectadas = detector_faces(frame_cinza)

    for face in faces_detectadas:
        # Obtém os pontos faciais do quadro
        pontos_faciais = modelo_pontos_faciais(frame_cinza, face)

        # Converte o quadro para RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Calcula os descritores faciais da imagem de referência e do quadro
        descritor_referencia = modelo_reconhecimento.compute_face_descriptor(imagem_referencia, pontos_referencia)
        descritor_frame = modelo_reconhecimento.compute_face_descriptor(frame_rgb, pontos_faciais)

        # Calcula a distância euclidiana entre os descritores faciais
        distancia = np.linalg.norm(np.array(descritor_referencia) - np.array(descritor_frame))

        # Define um limite de similaridade
        limite_similaridade = 0.5

        if distancia < limite_similaridade:
            # Se a distância for menor que o limite de similaridade, a pessoa é reconhecida
            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
            cv2.putText(frame, "Pessoa reconhecida", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2)
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
