# 1° Ingreso de módulos
import streamlit as st #pip install streamlit
import pygame
import threading
import time

# 2° Ingreso de valores
title_page_web='¿UNREAL?' #Título del Dashboard
title_portada='🚗Viajes|🤠Aventuras|🚲Ciclismo|🎥Peliculas|🎵Musicas|' #Título del Dashboard
mensajes = [
        "¡Pensaste que me había olvidado de ti! 🤔 ...",
        "Tu intuición pueda que te haya hecho pensar así ☝️, pero a veces las personas se equivocan. Mírame, tengo un don para programar 👨‍💻 y aun así tengo errores en la codificación, a veces me frustro y es ahí es donde sale a flote mi optimismo 🤓, el creer que todo me irá bien hace que piense en grande y me adelante a los hechos 😌. Pero el sentir algo por alguien es un algoritmo que no puedo comprender 😱, de seguro mi código no compila bien 🤔 y hace que la ejecución no salga como lo esperaba. Pero, sea lo que sea el dilema de mi vida o el problema que se suscite 😔, estoy seguro que lo solucionaré 💪; la desesperación ya no afecta en lo absoluto, por más que digas que soy un mocoso o un niño, entiende que a veces el nerviosismo y lo atrevido salen a flote con la persona indicada 😏.",
        "Creí haber perdido el camino hace tiempo, pero llego la señorita bella, inteligente, empática, misteriosa, graciosa …<continuará>… a mi vida 😳, que hizo que cobre la conciencia y me dé cuenta de las cosas que estuve haciendo mal ✌️. Cuanta razón tuvo Maquiavelo al decir “El fin justifica los medios” ✅, es una frase para justificar el accionar de las personas; ahora comprendo su significado, y me pregunto ¿Qué pasa después de que alguien consigue su objetivo? Al fin y al cabo, los seres humanos estamos hechos de codicia, y tratamos de llegar a la meta al costo de todo y de todos 😓; a este mundo le falta “empatía” cualidad que distingue a las personas 🌎.",
        "Haciendo una retrospectiva en el tiempo ⏳, me di cuenta que quería conocerte desde el momento en que te vi 👀, estoy seguro que la ley de la atracción no se equivocó al decir que “Atraemos lo que pensamos” 👍, la razón del porque nos atrajimos es debido a que en un pequeño instante de tiempo estuvimos en la cabeza uno del otro 👤; ahora las decisiones que vayamos a tomar marcarán un hito para nuestro destino 🕘🕙🕛. El cual también lo justifica la teoría del caos, al afirmar que basta con el pequeño aleteo de una mariposa para causar un tifón en el mundo.",
        "En este corto tiempo, me estudiaste bien, no negaré que sentía inseguridades con respecto a lo que quería 😐. Por atemorizante que sea, el sufrimiento nos hace más fuertes 💪, durante ese proceso debemos ser resilientes 👊, y estar convencidos de lo que no te mata te hace más fuerte ❤️‍🩹. Ambos pasamos por la misma decepción una y otra vez, ambos desistimos de amar nuevamente, pero hoy en día no logro encontrar la señal que cupido mal interpretó 😅, por más que busque y busque la respuesta no la encuentro 🤫. Ahora estoy convencido de que tú resultaste ser la excepción a todo lo que dije que nunca haría 😳, y tener la certeza de que eres la casualidad más bonita que ha llegado a mi vida 😏. Por ello, dame la oportunidad que yo me encargo de que valga la pena 🙌. Entrégame el tiempo que te sobre, y lo gastaré en llevarte de aventuras y de adrenalina 👉👈.",
        ]

#********************************************************************************************************
# 3° Nombres de la página web.
st.set_page_config(page_title = title_page_web, #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = '🖤', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

st.title(title_portada)
st.subheader("_🍷 Con cariño para_: :red[GRACIELA INES HUIZA BAUTISTA] ")#, divider='rainbow')
st.subheader("_⚡ De_:              :blue[S.D.C.A] ")#, divider='rainbow')
st.markdown("---") # Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

# Arreglo de 1x2 para las imágenes

col1, col2, col3 = st.columns([1,5,1]) #Centrar el botón
with col2:
    st.image("Imagen.jpg", use_column_width=True, width=None)

st.markdown("---") # Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown
#4° Insertar música: Sin que esta se pare...
audio1=open("Music.mp3","rb")
st.write("<REPRODUCEME 🎧🎵> [Runaway - Ed Sheeran]")
st.audio(audio1)

# # # # # Función para cargar y reproducir música en un hilo separado
# # # # def play_music(file_path, music_state):
# # # #     pygame.mixer.init()
# # # #     pygame.mixer.music.load(file_path)
# # # #     while music_state["playing"]:
# # # #         pygame.mixer.music.play()
# # # #         time.sleep(pygame.mixer.music.get_length())
# # # #     pygame.mixer.music.stop()

# # # # # Ruta al archivo de música
# # # # music_file_path = "music.mp3"

# # # # # Crear un diccionario para almacenar el estado de la música
# # # # music_state = {"playing": False}

# # # # # Almacenar el estado de la música en la sesión de Streamlit
# # # # if "music_state" not in st.session_state:
# # # #     st.session_state.music_state = music_state

# # # # # Iniciar la música al cargar la aplicación
# # # # if not st.session_state.music_state["playing"]:
# # # #     st.session_state.music_state["playing"] = True
# # # #     music_thread = threading.Thread(target=play_music, args=(music_file_path, st.session_state.music_state), daemon=True)
# # # #     music_thread.start()


# Menú lateral con las pestañas
st.warning(mensajes[0])
del(mensajes[0])

with st.container():
    # Índice del mensaje actual
    indice_mensaje = st.session_state.get('indice_mensaje', -1)
    
    # Botón Next
    if st.button("Next=>"):
        # Incrementar el índice para mostrar el siguiente mensaje
        indice_mensaje = (indice_mensaje + 1) % len(mensajes)
        st.session_state.indice_mensaje = indice_mensaje

    # Mostrar todos los mensajes anteriores en arreglos de 2 x 2
    for i in range(0, indice_mensaje + 1, 2):  # Incrementar de 2 en 2
        # Crear una fila para mostrar los mensajes en una matriz de 2 x 2
        col1, col2 = st.columns(2)
        with col1:
            if i < indice_mensaje + 1:
                st.warning(mensajes[i])
        with col2:
            if i + 1 < indice_mensaje + 1:
                st.warning(mensajes[i + 1])
    
    # st.write("[Live Video >](https://www.youtube.com/watch?v=VAiHHUMUp-4)")