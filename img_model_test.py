import tensorflow as tf
from tensorflow import keras
import numpy as np
from ipywidgets import FileUpload, Text, Button, Output, VBox, HBox
from IPython.display import display, Image
from io import BytesIO
from PIL import Image as PILImage # Para manipular a imagem
import matplotlib.pyplot as plt

model_mnist = tf.keras.models.load_model('model_cnn(99.0).keras')


uploader = FileUpload(
    accept='image/*',
    multiple=False,
    description='Carregar Imagem'
)

label_input = Text(
    placeholder='Digite a label correta (dígito de 0 a 9)',
    description='Label Correta:',
    disabled=False
)

test_button = Button(
    description='Testar Modelo',
    button_style='success',
    tooltip='Clique para testar o modelo com a imagem e label fornecidas'
)

output_area = Output()


def preprocess_image(image_bytes):
    img = PILImage.open(BytesIO(image_bytes)).convert('L')  # escala de cinza
    img = img.resize((28, 28))  # redimensionar
    img_array = np.array(img) / 255.0  # normalizar
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = np.expand_dims(img_array, axis=0) 
    img_array = preprocess_image(image_bytes)
    plt.imshow(img_array[0, :, :, 0], cmap='gray')
    plt.show()
    return img_array.astype(np.float32)






class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def on_test_button_clicked(b):
    with output_area:
        output_area.clear_output()

        if not uploader.value:
            print("Por favor, carregue uma imagem primeiro.")
            return

        if not label_input.value.isdigit() or int(label_input.value) not in range(10):
          print("Por favor, insira uma label numérica entre 0 e 9.")
          return

        uploaded_filename = list(uploader.value.keys())[0]
        image_content = uploader.value[uploaded_filename]['content']

        try:

            processed_image = preprocess_image(image_content)
            print(processed_image.shape)  # Deve ser (1, 28, 28)
            model_mnist(processed_image)  # Isso deve rodar sem erro se o modelo estiver correto
            display(Image(data=image_content, width=200))

            predictions = model_mnist.predict(processed_image)
            probabilities = tf.nn.softmax(predictions[0]).numpy()
            predicted_class_index = np.argmax(probabilities)
            predicted_probability = np.max(probabilities)
            predicted_class_name = class_names[predicted_class_index]

            true_label = label_input.value.strip().lower()
            predicted_label = predicted_class_name.lower()

            print(f"Previsão do Modelo: {predicted_class_name} (Probabilidade: {predicted_probability:.2f})")
            print(f"Label Correta Informada: {true_label}")

            if predicted_label == true_label:
              print("Resultado: ✅ O modelo reconheceu corretamente!")
            else:
              print(f"Resultado: ❌ O modelo NÃO reconheceu corretamente. Ele previu '{predicted_class_name}' mas a label correta era '{true_label}'.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print("Verifique se o pré-processamento da imagem está correto para o seu modelo (tamanho, canais, normalização).")


test_button.on_click(on_test_button_clicked)

input_widgets = VBox([uploader, label_input, test_button])
display(VBox([input_widgets, output_area]))
