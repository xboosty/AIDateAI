# Utiliza la imagen oficial de Python 3.9 para Windows
FROM winamd64/python:3.9.6-windowsservercore-1809

# Instala las bibliotecas que necesitas
RUN pip install --upgrade pip
RUN pip install openai
RUN pip install python-dotenv
RUN pip install numpy
RUN pip install matplotlib
RUN pip install wheel
RUN pip install SpeechRecognition
RUN pip install argparse
RUN pip install flask
RUN pip install requests
RUN pip install tensorflow
RUN pip install keras
RUN pip install pyttsx3
#RUN pip install torch
#RUN pip install git+https://github.com/openai/whisper.git

# Copia tu aplicación Python al contenedor
COPY ./assistant_enterview /app

# Establece el directorio de trabajo
WORKDIR /app

# Comando predeterminado para ejecutar tu aplicación Python
CMD ["python", "kernel.py"]
