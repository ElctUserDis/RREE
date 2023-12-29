# 1° Ingreso de módulos
import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.subplots as sp
import openpyxl
import webbrowser

# 2° Ingreso de valores
title_page_web='Recloser' #Título del Dashboard
title_portada='🖥️ Recloser|Respuesta|Comunicación' #Título del Dashboard
name_empresa='Empresa Electrocentro S.A.' #Título de la empresa

ancho_tabla_datos="1000px"
alto_tabla_datos="400px"

n_fig_AMT=6 # Número de figuras para la figura: recloser por alimentador.
n_row_AMT=3 # Número de filas de la figura: recloser por alimentador.
n_column_AMT=2 # Número de columnas de la figura: recloser por alimentador.
Ancho_AMT,height_AMT=8000,8000 # Dimensiones del ancho y la altura de los subplots de la figura: recloser por alimentador.

name_excel='Registros.xlsx' #Ingrese el nombre del excel con extensión.

#Lista de las columnas a mostrar por defecto.
selected_columns = ['AMT',
                    'MARCA',
                    'CONTROLADOR',
                    'SECC.GIS NUEVO',
                    'UBICACIÓN',
                    'OPERADOR INSTALADO',
                    'IP DEL CHIP',
                    'Rpta actual',
                    'Comunicación actual']

selected_columns_comunicacion = ['Fecha',
                    'AMT',
                    'MARCA',
                    'CONTROLADOR',
                    'Código SCADA Actual',
                    'SECC.GIS NUEVO',
                    'OPERADOR INSTALADO',
                    'IP DEL CHIP',
                    'Rpta actual',
                    'Comunicación actual']

lista_recloser=["NOJA","NOJA Power","Schneider","JinkWang","ENTEC","S&C","ABB","SEL"] #Lista de recloser aptos

#********************************************************************************************************
# 3° Nombres de la página web.
st.set_page_config(page_title = title_page_web, #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = '⚡', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

# Columnas
col1, col2 = st.columns([7, 1])  # Usar proporciones para especificar el ancho relativo de cada columna


col1.title(title_portada)
col1.subheader(name_empresa)
col1.subheader("_Elaborado por_: :blue[S.D.C.A] 👷")#, divider='rainbow')

# Columna 2: Imagen
imagen_path = "imagen.jpg"  # Ajusta la ruta de la imagen según sea necesario
col2.image(imagen_path, use_column_width=True)

st.markdown('---') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown
# Menú lateral con las pestañas
selected_tab = st.sidebar.radio("Visualización: ", ["1- Recloser instalados.", "2- Recloser comunicación."])
st.sidebar.markdown("---")# Insertar una línea horizontal

# Contenido de las pestañas

if selected_tab == "1- Recloser instalados.":
    # 4° Abre el libro de Excel "Registros.xlsx"
    direc=name_excel

    workbook = openpyxl.load_workbook(direc)
    sheet_names = []# Lista que almacenará los nombres de las hojas
    for sheet in workbook.sheetnames:# Recorre todas las hojas del libro
        if sheet != "SELECTORES":
            if sheet != "PLANTILLA":
                sheet_names.append(sheet)
    workbook.close()# Cierra el libro
    print(sheet_names) #Lista que almacena el nombre de las hojas del excel

    # Usamos el widget selectbox para seleccionar una hoja
    hoja_excel = st.sidebar.selectbox("Fecha inicio:", sheet_names)

    # 5° Lectura de los datos de la hoja excel seleccionada.
    df = pd.read_excel(direc,sheet_name = hoja_excel)

    # 5° Creación de tablas
    #5.1 Creación de filtros
    st.sidebar.header("Opciones a filtrar:") #5.1.1 sidebar => Crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
    select_all = st.sidebar.checkbox("Seleccionar todos los filtros")# 5.1.2 Casilla de verificación para seleccionar todos los filtros

    
    # Filtro de Departamento
    dpto = st.sidebar.multiselect(
        "Seleccione el Departamento:",
        options=['Seleccionar todo'] + df['DEPARTAMENTO'].unique().tolist(),
        default=[],
    )

    if 'Seleccionar todo' in dpto:
        dpto = df['DEPARTAMENTO'].unique().tolist()

    # Filtro de Unidad de Negocio (se habilita en función de la selección de Departamento)
    unidad_negocio_options = df[df['DEPARTAMENTO'].isin(dpto)]['UNIDAD DE NEGOCIO'].unique()
    unidad_negocio = st.sidebar.multiselect(
        "Seleccione la Unidad de Negocio:",
        options=['Seleccionar todo'] + unidad_negocio_options.tolist(),
        default=[],
    )

    if 'Seleccionar todo' in unidad_negocio:
        unidad_negocio = unidad_negocio_options.tolist()

    # Filtro de Subestación (se habilita en función de la selección de Unidad de Negocio)
    se_options = df[
        (df['DEPARTAMENTO'].isin(dpto)) &
        (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio))
    ]['SUBESTACION'].unique()
    se = st.sidebar.multiselect(
        "Seleccione la Subestación:",
        options=['Seleccionar todo'] + se_options.tolist(),
        default=[],
    )

    if 'Seleccionar todo' in se:
        se = se_options.tolist()

    # Filtro de Operador (se habilita en función de la selección de Subestación)
    operador_options = df[
        (df['DEPARTAMENTO'].isin(dpto)) &
        (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
        (df['SUBESTACION'].isin(se))
    ]['OPERADOR INSTALADO'].unique()
    operador = st.sidebar.multiselect(
        "Seleccione el Operador:",
        options=['Seleccionar todo'] + operador_options.tolist(),
        default=[],
    )

    if 'Seleccionar todo' in operador:
        operador = operador_options.tolist()

    # Filtro de Alimentador (AMT) - Filtrado en base a todas las selecciones anteriores
    amt_options = df[
        (df['DEPARTAMENTO'].isin(dpto)) &
        (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
        (df['SUBESTACION'].isin(se)) &
        (df['OPERADOR INSTALADO'].isin(operador))
    ]['AMT'].unique()
    amt = st.sidebar.multiselect(
        "Seleccione el Alimentador (AMT):",
        options=['Seleccionar todo'] + amt_options.tolist(),
        default=[],
    )

    if 'Seleccionar todo' in amt:
        amt = amt_options.tolist()

    # Verificar si se ha seleccionado algún departamento y desmarcar el checkbox si es el caso
    if len(amt) > 0:
        select_all = False

    # 5.3° Seleccionar todos los filtros
    if select_all:
        dpto = df['DEPARTAMENTO'].unique()
        unidad_negocio_options = df['UNIDAD DE NEGOCIO'].unique()
        unidad_negocio = unidad_negocio_options
        se_options = df['SUBESTACION'].unique()
        se = se_options
        operador_options = df['OPERADOR INSTALADO'].unique()
        operador = operador_options
        amt_options = df['AMT'].unique()
        amt = amt_options

    # 5.4 Filtra el DataFrame en función de las selecciones:
    filtered_df_UN = df[
        (df['DEPARTAMENTO'].isin(dpto)) &
        (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio))
    ]

    filtered_df_SE = df[
        (df['DEPARTAMENTO'].isin(dpto)) &
        (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
        (df['SUBESTACION'].isin(se))
    ]

    filtered_df = df[
        (df['DEPARTAMENTO'].isin(dpto)) &
        (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
        (df['SUBESTACION'].isin(se)) &
        (df['OPERADOR INSTALADO'].isin(operador)) &
        (df['AMT'].isin(amt))
    ]

    # 5.5 Muestra la tabla con los datos filtrados
    st.markdown(f"<p style='font-size: 20px; text-align: center; font-weight: bold;'>TABLA DE DATOS </p>", unsafe_allow_html=True)
    filtered_df_reinicio = filtered_df.reset_index()  # Reiniciar el índice del DataFrame
    del filtered_df_reinicio["index"]

    # Ordenar las filas del dataframe:

    filtered_df_reinicio = filtered_df_reinicio.sort_values(by=filtered_df_reinicio.columns.tolist())

    # Filtro de los campos
    with st.expander("Tabla de datos_ViewData    =====================================================================================================>  (Expandir)"):
        selected_columns_aux=selected_columns #Crear una copia de las columnas a mostrar por defecto

        #Filtrar las columnas seleccionadas por defecto, en la barra de selección.
        selected_columns = st.multiselect(
            "Seleccione el(los) campo(s) a mostrar:",
            options=['Seleccionar todo'] + [col for col in filtered_df_reinicio.columns if col not in selected_columns], #Excluir las columnas que lo pondremos por defecto
            default=[],
            #filtered_df_reinicio.columns[0:3].tolist()+filtered_df_reinicio.columns[9:11].tolist()+filtered_df_reinicio.columns[15:].tolist()
        )

        if 'Seleccionar todo' in selected_columns and len(selected_columns) > 1:
            #Remover la opción seleccionar todo, si en caso marcamos otra columna.
            selected_columns.remove('Seleccionar todo') 
            st.warning("'Seleccionar todo' ha sido desmarcado. Porque seleccionaste otro campo.")

        if 'Seleccionar todo' in selected_columns: 
            #Excluir las columnas que lo pondremos por defecto
            selected_columns = [col for col in filtered_df_reinicio.columns if col not in selected_columns_aux]

        selected_columns = selected_columns + selected_columns_aux

        # Mostrar las columnas por defecto
        filtered_df_reinicio = filtered_df_reinicio[selected_columns]

        # Reorganizar las columnas del DataFrame según el orden de selección
        column_names = filtered_df_reinicio.columns.tolist()# Lista de las columnas de la tabla de datos "filtered_df_reinicio"
        filtered_df_reinicio = filtered_df_reinicio[df.columns.intersection(column_names)]# Ordenar las columnas en base al orden del "df => Excel"

        filtered_df_reinicio = filtered_df_reinicio.reset_index(drop=True)# Reiniciar la enumeración del DataFrame
        filtered_df_reinicio.index = filtered_df_reinicio.index + 1 #Hacer que primera fila no sea "0"

            # TABLA
        st.write(filtered_df_reinicio)
        # # st.write(filtered_df_reinicio.style.background_gradient(cmap="Oranges"))# Imprimir la tabla.
        # Descargar la tabla en formato csv
        csvRES = filtered_df_reinicio.to_csv(index=False).encode('utf-8')  # Corregir aquí
        st.download_button("Download Data", data=csvRES, file_name="Tabla_Datos-DATA.csv", mime="text/csv")

    # 6° Impresión de datos generales:
    st.markdown("---") #separador

        # Calcula el total de elementos en cada columna
    total_rpta = len(filtered_df)
    total_comunicacion = len(filtered_df)

        # Cuenta el número de "Si" y "No" en la columna "Rpta actual"
    si_rpta = filtered_df['Rpta actual'].value_counts().get('Si', 0)
    no_rpta = filtered_df['Rpta actual'].value_counts().get('No', 0)

        # Cuenta los que no tienen comunicación, pero sí tienen respuesta
    si_comunicacion = filtered_df['Comunicación actual'].value_counts().get('Si', 0)
    no_comunicacion = si_rpta-si_comunicacion

    # Impresión de KPIs => Conteo del total de recloser
        # CONTEO DE RECLOSER APTOS
    conteos_marcas = df['MARCA'].value_counts().reset_index()

    conteos_marcas = conteos_marcas[conteos_marcas['MARCA'].isin(lista_recloser)]

    nuevos_nombres = {"MARCA": "Marca", "count": "Total"}
    conteos_marcas.rename(columns=nuevos_nombres, inplace=True)

    conteo_SC = df.loc[df['MARCA'] == 'S&C', 'SECC.GIS NUEVO'].ne("--").sum() #Elementos que no son "--"
    conteo_ABB=df.loc[df['MARCA']=='ABB','CONTROLADOR'].eq("PCD2000R").sum()  #Elementos que son "PCD2000R"
    conteo_SEL=df.loc[df['MARCA']=='SEL','CONTROLADOR'].eq("SEL-351R").sum()

    total_NOJA = conteos_marcas.loc[conteos_marcas['Marca'] == 'NOJA', 'Total'].values[0]
    total_NOJA_Power = conteos_marcas.loc[conteos_marcas['Marca'] == 'NOJA Power', 'Total'].values[0]

    conteos_marcas.loc[conteos_marcas['Marca'] == 'S&C', 'Total']=conteo_SC
    conteos_marcas.loc[conteos_marcas['Marca'] == 'ABB', 'Total']=conteo_ABB
    conteos_marcas.loc[conteos_marcas['Marca'] == 'SEL', 'Total']=conteo_SEL
    conteos_marcas.loc[conteos_marcas['Marca'] == 'NOJA', 'Total']=total_NOJA+total_NOJA_Power

    conteos_marcas.drop(conteos_marcas[conteos_marcas['Marca'] == 'NOJA Power'].index, inplace=True) #Eliminar la fila Noja Power
    conteos_marcas = conteos_marcas.sort_values(by='Total', ascending=False) # Ordenar en base al número de recloser con respuesta.

    total_recloser=conteos_marcas['Total'].sum()
    # URL de Google Maps
    st.markdown('##')
    url_input = "https://www.google.com/maps/d/u/0/viewer?mid=1jDCOXn4Su3ub1LHtoZyHbpffU_0ZwdA&ll=-11.344651744765466%2C-73.25285471281072&z=7"

    col1, col2, col3 = st.columns([3.5,0.4,2.5]) #Centrar el botón
    with col1:
        st.markdown(f"<p style='font-size: 34px; text-align: right; font-weight: bold;'>Recloser instalados: {total_recloser}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='font-size: 34px; text-align: center; font-weight: bold;'> ↝ </p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"[[ Ubicación de recloser en Google Maps ]]({url_input})")


    # 6° Guardar el gráfico de barras en la siguiente variable
    try:
        st.markdown("---") #separador
        #6.1° Creación de dos gráficas en una fila: Por marca y por Unidad de Negocio

        col1,col2=st.columns((2)) #Creación arreglo de gráficas (1x2)
            # 6.1.1° Recloser instalados por marcas.  
        with col1:
            st.subheader("Total de recloser por marca")
            fig = px.bar(conteos_marcas, x="Marca", y="Total",
                        text=['{:,.0f} und.'.format(x) for x in conteos_marcas["Total"]],
                        template="seaborn")
                # Configuración para mostrar el texto encima de las barras y con tamaño 24
            fig.update_traces(textposition='outside', textfont_size=15) # Config. de las etiquetas de las barras.
            fig.update_layout(xaxis=dict(tickangle=-45, tickfont=dict(size=15)),yaxis_range=[0, conteos_marcas['Total'].max()+30]) # Config. texto del eje "X"
            st.plotly_chart(fig, use_container_width=True, height=200)

            # 6.1.2° Agrupar por 'UNIDAD DE NEGOCIO' => "Nro de recloser instalados"----------------->DIAGRAMA DE PASTEL
        with col2:
            st.subheader("Porcentaje de recloser por marca")
            # 1° FORMA
                # GRAFICAR
            fig=px.pie(conteos_marcas,values='Total',hole=0.25)
            fig.update_traces(text=conteos_marcas['Marca'], textposition='outside',textfont_size=15)
            st.plotly_chart(fig,use_container_width=False)

        # 6.2° Creación de tablas
            # 6.2.1: Creación de la tabla de los diagramas
        conteos_marcas.reset_index(drop=True, inplace=True)
        conteos_marcas['Porcentaje (%)']=round(conteos_marcas['Total']/total_recloser*100,2)
        conteos_marcas.index = conteos_marcas.index + 1  # Hacer que la primera fila no sea "0"

        with st.expander("Marca_ViewData"):
            st.write(conteos_marcas)
            # # st.write(conteos_marcas.style.background_gradient(cmap="Greens"))# Imprimir la tabla.
            # Descargar la tabla en formato csv
            csvMarca = conteos_marcas.to_csv(index=False).encode('utf-8')  # Corregir aquí
            st.download_button("Download Data", data=csvMarca, file_name="Marca-DATA.csv", mime="text/csv")

        st.markdown("---") #separador
        #**********************************************************************************************************************************************************
        #6.3° Recloser con respuesta/comunicación
        lista_elementos_rpta=list()
        lista_elementos_com=list()

        # Listas para crear los DataFrames
        columnas_elementos_rpta=["MARCA","Total","Si rpta","No rpta"]
        columnas_elementos_com=["MARCA","Si rpta","Si comunicación","No comunicación"]
        
        #lista_recloser=["NOJA","NOJA Power","Schneider","JinkWang","ENTEC","S&C","ABB","SEL"] #Lista de recloser aptos

        for elemento_com in lista_recloser:
            lista_aux_respuesta,lista_aux_comunicaion=list(),list()
            
            if elemento_com=="S&C":
                # Contar los elementos que digan "Si" en la columna "Rpta actual" en base al filtro ["MARCA","Rpta actual","SECC.GIS NUEVO"].
                si_respuesta = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'Si') & (df['SECC.GIS NUEVO'] != '--'), 'Rpta actual'].count()
                no_respuesta = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'No') & (df['SECC.GIS NUEVO'] != '--'), 'Rpta actual'].count()
                no_com = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'Si') & (df['Comunicación actual'] == 'No') &  (df['SECC.GIS NUEVO'] != '--'), 'Comunicación actual'].count()
            
            elif elemento_com=="ABB":
                si_respuesta = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'Si') & (df['CONTROLADOR'] == 'PCD2000R'), 'Rpta actual'].count()
                no_respuesta = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'No') & (df['CONTROLADOR'] == 'PCD2000R'), 'Rpta actual'].count()
                no_com = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'Si') & (df['Comunicación actual'] == 'No') & (df['CONTROLADOR'] == 'PCD2000R'), 'Comunicación actual'].count()
                   
            elif elemento_com=="SEL":
                si_respuesta = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'Si') & (df['CONTROLADOR'] == 'SEL-351R'), 'Rpta actual'].count()
                no_respuesta = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'No') & (df['CONTROLADOR'] == 'SEL-351R'), 'Rpta actual'].count()
                no_com = df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'Si') & (df['Comunicación actual'] == 'No') & (df['CONTROLADOR'] == 'SEL-351R'), 'Comunicación actual'].count()
            
            else: # Para los demas recloser
                si_respuesta=df.loc[df['MARCA'] == elemento_com, 'Rpta actual'].eq("Si").sum()
                no_respuesta=df.loc[df['MARCA'] == elemento_com, 'Rpta actual'].eq("No").sum()
                no_com=df.loc[(df['MARCA'] == elemento_com) & (df['Rpta actual'] == 'Si') , 'Comunicación actual'].eq("No").sum()
            
            si_com=si_respuesta-no_com
            total=si_respuesta+no_respuesta

            lista_aux_respuesta=[elemento_com,total,si_respuesta,no_respuesta]
            lista_aux_comunicaion=[elemento_com,si_respuesta,si_com,no_com]
            
            lista_elementos_rpta.append(lista_aux_respuesta)
            lista_elementos_com.append(lista_aux_comunicaion)

        df_RPTA = pd.DataFrame(lista_elementos_rpta, columns=columnas_elementos_rpta) # Convertir la lista anilada en un dataframe.
        df_COM = pd.DataFrame(lista_elementos_com, columns=columnas_elementos_com) # Convertir la lista anilada en un dataframe.

        df_RPTA.iloc[0, 1:] = df_RPTA.iloc[0, 1:] + df_RPTA.iloc[1, 1:] # Sumar los valores de la columna "NOJA" y "NOJA Power"
        df_COM.iloc[0, 1:] = df_COM.iloc[0, 1:] + df_COM.iloc[1, 1:] # Sumar los valores de la columna "NOJA" y "NOJA Power"

        df_RPTA = df_RPTA[df_RPTA['MARCA'] != 'NOJA Power'] # Eliminar la fila Noja Power
        df_COM = df_COM[df_COM['MARCA'] != 'NOJA Power'] # Eliminar la fila Noja Power
        
        df_RPTA = df_RPTA.reset_index(drop=True) # Reinicio de índices
        df_COM = df_COM.reset_index(drop=True) # Reinicio de índices

        df_RPTA = df_RPTA.sort_values(by='Total', ascending=False) # Ordenar en base al número de recloser con respuesta.
        df_COM = df_COM.sort_values(by='Si rpta', ascending=False) # Ordenar en base al número de recloser con respuesta.

        df_RPTA.index = df_RPTA.index + 1  # Hacer que la primera fila no sea "0"
        df_COM.index = df_COM.index + 1  # Hacer que la primera fila no sea "0"
        
        # Gráfico de pastel, con el número de recloser con respuesta y comunicación.
        left_column, right_column = st.columns(2)
        si_rpta_total,no_rpta_total=df_RPTA['Si rpta'].sum(),df_RPTA['No rpta'].sum()
        si_com_total,no_com_total=df_COM['Si comunicación'].sum(),df_COM['No comunicación'].sum()

        diccionario_respuesta={
            "Tienen respuesta":si_rpta_total,
            "No tienen respuesta":no_rpta_total
        }
        diccionario_comunicacion={
            "Tienen comunicacion":si_com_total,
            "No tienen comunicacion":no_com_total
        }
        with left_column:
        
            st.markdown(f"<p style='font-size: 22px; text-align: Center'>Respuesta de recloser: {si_rpta_total}/{si_rpta_total+no_rpta_total}</p>", unsafe_allow_html=True)            
            df_respuesta = pd.DataFrame(list(diccionario_respuesta.items()), columns=['Etiqueta', 'Valor'])
            # Crear y mostrar el gráfico de velocidad
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                gauge={'axis': {'range': [0, si_rpta_total+no_rpta_total]},
                    'steps': [{'range': [0,si_rpta_total], 'color': "blue"},
                              {'range': [si_rpta_total,si_rpta_total+no_rpta_total], 'color': "red"}],
                    'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': si_rpta_total}}))
            st.plotly_chart(fig, use_container_width=True)

        with right_column:
            st.markdown(f"<p style='font-size: 22px;  text-align: Center'>Comunicación de recloser: {si_com_total}/{si_rpta_total}</p>", unsafe_allow_html=True)
            df_comunication = pd.DataFrame(list(diccionario_comunicacion.items()), columns=['Etiqueta', 'Valor'])
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                gauge={'axis': {'range': [0, si_rpta_total]},
                    'steps': [{'range': [0,si_com_total], 'color': "green"},
                              {'range': [si_com_total,si_rpta_total], 'color': "brown"}],
                    'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': si_com_total}}))
            fig.update_layout(legend={'traceorder': 'reversed'})
            st.plotly_chart(fig, use_container_width=True)
            
        # Creación de tablas
        with left_column:
            with st.expander("Rpta_ViewData"):
                st.write(df_RPTA)
                # # st.write(conteos_marcas.style.background_gradient(cmap="Greens"))# Imprimir la tabla.
                # Descargar la tabla en formato csv
                csvRPTA = df_RPTA.to_csv(index=False).encode('utf-8')  # Corregir aquí
                st.download_button("Download Data", data=csvRPTA, file_name="RPTA-DATA.csv", mime="text/csv")

        with right_column:
            with st.expander("Com_ViewData"):
                st.write(df_COM)
                # # st.write(conteos_marcas.style.background_gradient(cmap="Greens"))# Imprimir la tabla.
                # Descargar la tabla en formato csv
                csvCOM = df_COM.to_csv(index=False).encode('utf-8')  # Corregir aquí
                st.download_button("Download Data", data=csvCOM, file_name="COM-DATA.csv", mime="text/csv")

        #******************************************************************************************************************************************************************************************************************
        #******************************************************************************************************************************************************************************************************************
        st.markdown("---") #separador
        #6.2° RECLOSER POR UNIDAD DE NEGOCIO
            # Agregar una nueva columna 'Contador de "Si"'
        condicion_SC = (df['MARCA'] == 'S&C') & ((df['SECC.GIS NUEVO'] == '--') | (df['OPERADOR INSTALADO'] == '--'))
        condicion_ABB = (df['MARCA'] == 'ABB') & (df['CONTROLADOR'] != 'PCD2000R')
        condicion_SEL = (df['MARCA'] == 'SEL') & (df['CONTROLADOR'] != 'SEL-351R')
        filtered_df_UN = filtered_df_UN.loc[~(condicion_SC | condicion_ABB | condicion_SEL)]
        
        filtered_df_UN['Recloser con respuesta'] = filtered_df_UN['Rpta actual'].apply(lambda x: x.count('Si'))
        filtered_df_UN['Recloser sin respuesta'] = filtered_df_UN['Rpta actual'].apply(lambda x: x.count('No'))
        filtered_df_UN['Recloser con comunicación'] = filtered_df_UN['Comunicación actual'].apply(lambda x: x.count('Si'))
        filtered_df_UN['Recloser sin comunicación'] = filtered_df_UN['Comunicación actual'].apply(lambda x: x.count('No'))

            # Agrupar y sumar los valores
        grouped_2 = filtered_df_UN.groupby('UNIDAD DE NEGOCIO').agg({
            'UNIDAD DE NEGOCIO': 'first',  # Añadir la primera columna
            'Recloser con respuesta': 'sum',
            'Recloser sin respuesta': 'sum',
            'Recloser con comunicación': 'sum',
            'Recloser sin comunicación': 'sum'
        })

            # Calcular el número de Recloser instalados en cada UNIDAD DE NEGOCIO
        grouped_2['Recloser instalados'] = filtered_df_UN['UNIDAD DE NEGOCIO'].value_counts()
            # Crear el diagrama de pastel
        grouped_2 = grouped_2.sort_values(by='Recloser instalados', ascending=False) # Ordenar en base al número de recloser con respuesta.
        grouped_2 = grouped_2.reset_index(drop=True)# Reiniciar la enumeración del DataFrame
        grouped_2.index = grouped_2.index + 1 #Hacer que primera fila sea "1"

        fig_rpta_UN = px.bar(grouped_2, 
                            x=['Recloser instalados','Recloser con respuesta','Recloser con comunicación'], 
                            y=grouped_2['UNIDAD DE NEGOCIO'],
                            orientation="h", 
                            color_discrete_sequence=["#C2BC18", "#FAA632", '#13B3C1'],
                            opacity=[1], #Opacidad
                            template='plotly_white')  

        st.markdown(f"<p style='font-size: 22px; text-align: Center'>Recloser por Unidad de Negocio</p>", unsafe_allow_html=True)            

        fig_rpta_UN.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title='Unidad de Negocio',
            xaxis_title='Cantidad de recloser',
            title_x=0,
            autosize=True,
            height=1200
        )

        # Configurar el tamaño del gráfico
        fig_rpta_UN.update_layout(height=450)
        fig_rpta_UN.update_xaxes(range=[0, grouped_2['Recloser instalados'].max()+50],
                                tickvals=list(range(0, grouped_2['Recloser instalados'].max()+50, 25)))

        fig_rpta_UN.update_traces(textposition='outside', textfont_size=15) 

        # Superponer las barras en lugar de apilarlas
        fig_rpta_UN.update_layout(barmode='overlay')
        
        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_rpta_UN, use_container_width=True)
        
        with st.expander("UN_ViewData"):
            # Descargar la tabla en formato csv
            csvUN = grouped_2.to_csv(index=False).encode('utf-8')  # Corregir aquí
            st.write(grouped_2)
            st.download_button("Download Data", data=csvUN, file_name="Unidad de Negocio-DATA.csv", mime="text/csv")

# # # #******************************************************************************************************************************************************************************************************************
# # # #******************************************************************************************************************************************************************************************************************
# # #         # 6.2° Agrupar por 'SUBESTACIÓN' => "Nro de respuestas y comunicación de los recloser"----------------->DIAGRAMA DE BARRAS EN HORIZONTAL
# # #         st.markdown("---") #separador
# # #         # Agregar una nueva columna 'Contador de "Si"'
# # #         grouped_1 = pd.DataFrame()

# # #         filtered_df_SE['Recloser con respuesta'] = filtered_df_SE['Rpta actual'].apply(lambda x: x.count('Si'))
# # #         filtered_df_SE['Sin Respuesta actual'] = filtered_df_SE['Rpta actual'].apply(lambda x: x.count('No'))
# # #         filtered_df_SE['Recloser con comunicación'] = filtered_df_SE['Comunicación actual'].apply(lambda x: x.count('Si'))
# # #         filtered_df_SE['Sin Comunicación actual'] = filtered_df_SE['Comunicación actual'].apply(lambda x: x.count('No'))

# # #         # Agrupar y sumar los valores
# # #         grouped_1 = filtered_df_SE.groupby('SUBESTACION').agg({
# # #             'Recloser con respuesta': 'sum',
# # #             'Sin Respuesta actual': 'sum',
# # #             'Recloser con comunicación': 'sum',
# # #             'Sin Comunicación actual': 'sum'
# # #         })
# # #         grouped_1['Recloser instalados'] = filtered_df_SE['SUBESTACION'].value_counts().reindex(grouped_1.index) # Conteo de recloser por SE.

# # #         # 6.1.4° Imprimir tabla
# # #         grouped_1 = grouped_1.sort_values(by='Recloser con respuesta', ascending=False) # Ordenar en base al número de recloser instalados.

# # #         fig_rpta_SE = px.bar(grouped_1, x=['Recloser con respuesta','Sin Respuesta actual'],  y=grouped_1.index,
# # #                                 orientation= "h", #horizontal bar chart
# # #                                 color_discrete_sequence=["blue", "red"],
# # #                                 #color_discrete_sequence=px.colors.qualitative.Set3,  # Colores diferentes
# # #                                 template='plotly_white')  # Ajustar el ancho
        
# # #         fig_com_SE = px.bar(grouped_1, x=['Recloser con comunicación','Sin Comunicación actual'],  y=grouped_1.index,
# # #                             orientation= "h", #horizontal bar chart
# # #                             color_discrete_sequence=["blue", "green"],
# # #                             #color_discrete_sequence=px.colors.qualitative.Set3,  # Colores diferentes
# # #                             template='plotly_white')  # Ajustar el ancho

# # #         fig_rpta_SE.update_layout(
# # #             plot_bgcolor="rgba(0,0,0,0)",
# # #             yaxis_title='Subestaciones',  # Nombre del eje y
# # #             xaxis_title='Cantidad de recloser',  # Nombre del eje x
# # #             title_text="<b>Respuesta de recloser por Subestación</b>",
# # #             title_x=0,  # Alinear a la izquierda
# # #             autosize=True,  # Ajustar automáticamente al ancho disponible
# # #             height=1200  # Aumenta la altura a 600 píxeles (ajusta este valor según tus necesidades)

# # #         )

# # #         fig_com_SE.update_layout(
# # #             plot_bgcolor="rgba(0,0,0,0)",
# # #             yaxis_title='Subestaciones',  # Nombre del eje y
# # #             xaxis_title='Cantidad de recloser',  # Nombre del eje x
# # #             title_text="<b>Comunicación de recloser por Subestación</b>",
# # #             title_x=0,  # Alinear a la izquierda
# # #             autosize=True,  # Ajustar automáticamente al ancho disponible
# # #             height=1200  # Aumenta la altura a 600 píxeles (ajusta este valor según tus necesidades)

# # #         )
# # #         # st.plotly_chart(fig_rpta_SE)# Mostrar el gráfico en Streamlit

# # #         # 6.1.3° Colocar las gráficas con arreglo ( 1 x 2 )

# # #         left_column, right_column = st.columns(2)

# # #         left_column.plotly_chart(fig_rpta_SE, use_container_width = True) #esta va al lado izquierdo
# # #         right_column.plotly_chart(fig_com_SE, use_container_width = True)

# # #             #Tabla:
# # #         with st.expander("Subestaciones_ViewData"):
# # #             summary_df1 = grouped_1.reset_index()  # Reiniciar el índice del DataFrame
# # #             summary_df1.index = summary_df1.index + 1  # Hacer que la primera fila sea "1" en lugar de "0"
# # #             st.write(summary_df1)

# # #             # # st.write(summary_df1.style.background_gradient(cmap="Purples"))  # Imprimir la tabla.
# # #             # Descargar la tabla en formato csv
# # #             csvSE = summary_df1.to_csv(index=False).encode('utf-8')  # Corregir aquí
# # #             st.download_button("Download Data", data=csvSE, file_name="Subestaciones-DATA.csv", mime="text/csv")
        
        # **************************************
        st.markdown("---") #separador
        # Estilo del "Streamlit"
        hide_st_style = """
                <style>
    
                footer {visibility: hidden;}

                </style>
                """

        st.markdown(hide_st_style, unsafe_allow_html= True)

    except Exception as e:
        st.markdown("...(Espera)")

elif selected_tab == "2- Recloser comunicación.":
    try:
        # st.header("¡UPS!, Esta pestaña se encuentra en actualizacion.")

        # 4° Abre el libro de Excel "Registros.xlsx"
        direc=name_excel
        workbook = openpyxl.load_workbook(direc)

        #4.1° Fecha de inicio
        sheet_names = []# Lista que almacenará los nombres de las hojas
        for sheet in workbook.sheetnames:# Recorre todas las hojas del libro
            if sheet != "SELECTORES":
                if sheet != "PLANTILLA":
                    sheet_names.append(sheet)
        hoja_excel = st.sidebar.selectbox("Fecha inicio:", sheet_names) # Usamos el widget selectbox para seleccionar una hoja
        for ii,vv in enumerate(sheet_names):
            if vv==hoja_excel:
                item_inicio=ii

        #4.2° Fecha final
        hoja_excel_final = st.sidebar.selectbox("Fecha final:", sheet_names[item_inicio:])# Usamos el widget selectbox para seleccionar una hoja
        for ii,vv in enumerate(sheet_names):
            if vv==hoja_excel_final:
                item_final=ii
        workbook.close()# Cierra el libro
        st.sidebar.markdown("----")

        # 5° Lectura de los datos deL intervalor
        df = pd.read_excel(direc,sheet_name = hoja_excel)
            
        # 5° Creación de tablas
        #5.1 Creación de filtros
        st.sidebar.header("Opciones a filtrar:") #5.1.1 sidebar => Crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
        select_all = st.sidebar.checkbox("Seleccionar todos los filtros")# 5.1.2 Casilla de verificación para seleccionar todos los filtros

        # 5.1.1° Filtro de Departamento
        dpto = st.sidebar.multiselect(
            "Seleccione el Departamento:",
            options=['Seleccionar todo'] + df['DEPARTAMENTO'].unique().tolist(),
            default=[],
        )

        if 'Seleccionar todo' in dpto:
            dpto = df['DEPARTAMENTO'].unique().tolist()

        # 5.1.2° Filtro de Unidad de Negocio (se habilita en función de la selección de Departamento)
        unidad_negocio_options = df[df['DEPARTAMENTO'].isin(dpto)]['UNIDAD DE NEGOCIO'].unique()
        unidad_negocio = st.sidebar.multiselect(
            "Seleccione la Unidad de Negocio:",
            options=['Seleccionar todo'] + unidad_negocio_options.tolist(),
            default=[],
        )

        if 'Seleccionar todo' in unidad_negocio:
            unidad_negocio = unidad_negocio_options.tolist()

        # 5.1.3° Filtro de Subestación (se habilita en función de la selección de Unidad de Negocio)
        se_options = df[
            (df['DEPARTAMENTO'].isin(dpto)) &
            (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio))
        ]['SUBESTACION'].unique()
        se = st.sidebar.multiselect(
            "Seleccione la Subestación:",
            options=['Seleccionar todo'] + se_options.tolist(),
            default=[],
        )

        if 'Seleccionar todo' in se:
            se = se_options.tolist()

        # 5.1.4° Filtro de Operador (se habilita en función de la selección de Subestación)
        operador_options = df[
            (df['DEPARTAMENTO'].isin(dpto)) &
            (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
            (df['SUBESTACION'].isin(se))
        ]['OPERADOR INSTALADO'].unique()
        operador = st.sidebar.multiselect(
            "Seleccione el Operador:",
            options=['Seleccionar todo'] + operador_options.tolist(),
            default=[],
        )

        if 'Seleccionar todo' in operador:
            operador = operador_options.tolist()

        # 5.1.6° Verificar si se ha seleccionado algún departamento y desmarcar el checkbox si es el caso
        if len(operador) > 0:
            select_all = False

        # 5.2° Seleccionar todos los filtros
        if select_all:
            dpto = df['DEPARTAMENTO'].unique()
            unidad_negocio_options = df['UNIDAD DE NEGOCIO'].unique()
            unidad_negocio = unidad_negocio_options
            se_options = df['SUBESTACION'].unique()
            se = se_options
            operador_options = df['OPERADOR INSTALADO'].unique()
            operador = operador_options

        # # Filtrar el DataFrame en base a todas las selecciones anteriores
        # filtered_df = df[
        #     (df['DEPARTAMENTO'].isin(dpto)) &
        #     (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
        #     (df['SUBESTACION'].isin(se)) &
        #     (df['OPERADOR INSTALADO'].isin(operador))
        # ]

        # 5.3.1° Filtro de Alimentador (AMT)
        st.sidebar.markdown("----")
        st.sidebar.header("Filtro del Alimentador (AMT):")
        # amt_options = filtered_df['AMT'].unique()

        amt_options = df[
            (df['DEPARTAMENTO'].isin(dpto)) &
            (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
            (df['SUBESTACION'].isin(se)) &
            (df['OPERADOR INSTALADO'].isin(operador))
        ]['AMT'].unique()
        
        amt_input = st.sidebar.text_input("Escriba el alimentador (AMT):", "")
        filtered_amt_options = [option for option in amt_options if amt_input.lower() in option.lower()]
        amt = st.sidebar.selectbox("Seleccione el alimentador (AMT):", options=filtered_amt_options, index=0 if filtered_amt_options else None)

        st.sidebar.markdown("----")
        filtro_opcion = st.sidebar.selectbox("Elección del campo:", ["1- SCADA", "2- GIS"])# Barra desplegable para seleccionar entre "SCADA" y "GIS"
        if filtro_opcion == "1- SCADA":
            # 5.3.2° Filtro por código SCADA

            st.sidebar.header("Seleccione el código SCADA:")
            scada_options = df[df['AMT'] == amt]['Código SCADA Actual'].unique()
            scada_options_non_empty = [option for option in scada_options if option.strip() != '']# Filtra los elementos que contienen "RE"
            seleccion = st.sidebar.radio("", options= scada_options_non_empty, index=0) # Muestrame en el cuadro de los check-list
            field_camp = 'Código SCADA Actual'

        
        elif filtro_opcion == "2- GIS":
            # 5.3.3° Filtro por código SECCIONAMIENTO - Filtrado en base a todas las selecciones anteriores
            st.sidebar.header("Seleccione el código del SECCIONAMIENTO")
            gis_options = df[df['AMT'] == amt]['SECC.GIS NUEVO'].unique()
            gis_options_filtered = [option for option in gis_options if option.strip() != '' and option != '--']
            seleccion = st.sidebar.radio("", options=list(gis_options), index=0)
            field_camp = 'SECC.GIS NUEVO'

        diccionario_fechas={
            "Fecha":[],
            "Nro de respuestas":[],
            "Nro de intermitencias":[],
            "Nro de muestras":[],
            "Rpta actual":[],
            "Comunicación actual":[]
        }
        for hoja_recorrido in sheet_names[item_inicio:item_final+1]:
            # 5° Lectura de los datos de la hoja excel seleccionada.
            df_aux = pd.read_excel(direc,sheet_name = hoja_recorrido)
            
            diccionario_fechas['Fecha'].append(hoja_recorrido)
            diccionario_fechas['Nro de respuestas'].append(df_aux.loc[(df_aux['AMT'] == amt) & (df_aux[field_camp] == seleccion), 'Nro de respuestas'].iloc[0])
                    # df_aux.loc[(df_aux['AMT'] == amt) & (df_aux[field_camp] == seleccion), 'Nro de respuestas'].iloc[0]:
                        # Mascara: (df_aux['AMT'] == amt) & (df_aux[field_camp] == seleccion)
                        # Valor que deseamos sacar: df_aux.loc[... , "field_name" ] => Como un dataframe
                        # Solo obtener el valor: .iloc[0] => Es solo un número.
            
            diccionario_fechas['Nro de intermitencias'].append(df_aux.loc[(df_aux['AMT'] == amt) & (df_aux[field_camp] == seleccion), 'Nro de intermitencias'].iloc[0])
            diccionario_fechas['Nro de muestras'].append(df_aux.loc[(df_aux['AMT'] == amt) & (df_aux[field_camp] == seleccion), 'Nro de muestras'].iloc[0])
            diccionario_fechas['Rpta actual'].append(df_aux.loc[(df_aux['AMT'] == amt) & (df_aux[field_camp] == seleccion), 'Rpta actual'].iloc[0])
            diccionario_fechas['Comunicación actual'].append(df_aux.loc[(df_aux['AMT'] == amt) & (df_aux[field_camp] == seleccion), 'Comunicación actual'].iloc[0])


        # Obtener los datos de la fila seleccionada.
        fila_seleccionada = df[df[field_camp] == seleccion].iloc[0,:13].to_frame().T #Datos de la fila que se selecciona.
            #iloc[0,:13]: Mantenerme las 13 primeras columnas.
            #.to_frame().T: Transponición de filas y columnas.
        fila_seleccionada = pd.concat([fila_seleccionada] * (item_final-item_inicio+1), ignore_index=True)
            #Aumentar las filas de fila_seleccionada y poner los valores de la primera fila en las filas nuevas.
        
        df_final=pd.DataFrame(diccionario_fechas)
        df_final = pd.concat([df_final.iloc[:, :1], fila_seleccionada.iloc[:, 1:], df_final.iloc[:, 1:].reset_index(drop=True)], axis=1)
            #Añadir el dataframe fila_seleccionada a partir de la columna 1 del df_final.

        # Filtro de los campos
        with st.expander("Tabla de datos_ViewData    =====================================================================================================>  (Expandir)"):
            selected_columns_aux=selected_columns_comunicacion #Crear una copia de las columnas a mostrar por defecto

            #Filtrar las columnas seleccionadas por defecto, en la barra de selección.
            selected_columns_comunicacion = st.multiselect(
                "Seleccione el(los) campo(s) a mostrar:",
                options=['Seleccionar todo'] + [col for col in df_final.columns if col not in selected_columns_comunicacion], #Excluir las columnas que lo pondremos por defecto
                default=[],
                #filtered_df_reinicio.columns[0:3].tolist()+filtered_df_reinicio.columns[9:11].tolist()+filtered_df_reinicio.columns[15:].tolist()
            )

            if 'Seleccionar todo' in selected_columns_comunicacion and len(selected_columns_comunicacion) > 1:
                #Remover la opción seleccionar todo, si en caso marcamos otra columna.
                selected_columns_comunicacion.remove('Seleccionar todo') 
                st.warning("'Seleccionar todo' ha sido desmarcado. Porque seleccionaste otro campo.")

            if 'Seleccionar todo' in selected_columns_comunicacion: 
                #Excluir las columnas que lo pondremos por defecto
                selected_columns_comunicacion = [col for col in df_final.columns if col not in selected_columns_aux]

            selected_columns_comunicacion = selected_columns_comunicacion + selected_columns_aux

            # Mostrar las columnas por defecto
            filtered_df_reinicio = df_final[selected_columns_comunicacion]

            # Reorganizar las columnas del DataFrame según el orden de selección
            column_names = filtered_df_reinicio.columns.tolist()# Lista de las columnas de la tabla de datos "filtered_df_reinicio"
            filtered_df_reinicio = filtered_df_reinicio[df_final.columns.intersection(column_names)]# Ordenar las columnas en base al orden del "df => Excel"

            filtered_df_reinicio = filtered_df_reinicio.reset_index(drop=True)# Reiniciar la enumeración del DataFrame
            filtered_df_reinicio.index = filtered_df_reinicio.index + 1 #Hacer que primera fila no sea "0"

                # TABLA
            filtered_df_reinicio = filtered_df_reinicio.set_index(filtered_df_reinicio.columns[0]) #Convertir la primera columna en el índice del dataframe.
            st.write(filtered_df_reinicio)

            # # st.write(filtered_df_reinicio.style.background_gradient(cmap="Oranges"))# Imprimir la tabla.
            # Descargar la tabla en formato csv
            csvRES = filtered_df_reinicio.to_csv(index=False).encode('utf-8')  # Corregir aquí
            st.download_button("Download Data", data=csvRES, file_name="Tabla_Datos-DATA.csv", mime="text/csv")

        
        filtered_df_reinicio.reset_index(inplace=True) #Reiniciar el índice y hacer que su indice inicial se convierta en la primera columna.
        
        df_grafico=filtered_df_reinicio.copy() #Crear una copia del dataframe original
        df_grafico.replace({'Si': 2, 'No': 1}, inplace=True) # Reemplazar los valores "Si" y "No" por 2 y 1

        si_rpta_color='#3D2B8E'
        si_com_color='#badb73'
        no_color='#ffaaa6'

        df_grafico['Color_rpta'] = df_grafico['Rpta actual'].map({2: si_rpta_color, 1: no_color}) # Crear nueva columna para "Asignar colores"
        df_grafico['Texto_rpta'] = df_grafico['Rpta actual'].map({2: 'Si', 1: 'No'}) # Crear nueva columna para "Asignar texto", encima de las barras

        df_grafico['Color_com'] = df_grafico['Comunicación actual'].map({2: si_com_color, 1: no_color}) # Crear nueva columna para "Asignar colores"
        df_grafico['Texto_com'] = df_grafico['Comunicación actual'].map({2: 'Si', 1: 'No'}) # Crear nueva columna para "Asignar texto", encima de las barras

        st.markdown("---") #separador
        col1,col2=st.columns((2)) #Creación arreglo de gráficas (1x2)

        # 6.1.1° Evolución de la respuesta en el tiempo
        with col1:
            st.markdown(f"<p style='font-size: 22px; text-align: Center'>Respuesta de recloser</p>", unsafe_allow_html=True)    
            fig = px.bar(df_grafico, x="Fecha", y="Rpta actual",
                        color='Color_rpta',
                        text='Texto_rpta',
                        template="plotly", # Cambiar la paleta de colores a "plotly"
                        color_discrete_map={si_rpta_color: si_rpta_color,no_color: no_color})
            
            fig.update_layout(showlegend=False) # Ocultar la leyenda.
                # Configuración para mostrar el texto encima de las barras y con tamaño 24
            fig.update_traces(textposition='outside', textfont_size=15) # Config. de las etiquetas de las barras.
            fig.update_layout(xaxis=dict(tickangle=-45, tickfont=dict(size=15)),
                              yaxis=dict(showticklabels=False, range=[0, 2.5]))

            st.plotly_chart(fig, use_container_width=True, height=200) # Graficar el streamlit

        # 6.1.2° Evolución de la comunicación en el tiempo
        with col2:
            st.markdown(f"<p style='font-size: 22px; text-align: Center'>Comunicación de recloser</p>", unsafe_allow_html=True)
            fig = px.bar(df_grafico, x="Fecha", y="Comunicación actual",
                        color='Color_com',
                        text='Texto_com',
                        template="plotly", # Cambiar la paleta de colores a "plotly"
                        color_discrete_map={si_com_color: si_com_color,no_color:no_color})
            
            fig.update_layout(showlegend=False) # Ocultar la leyenda.
                # Configuración para mostrar el texto encima de las barras y con tamaño 24
            fig.update_traces(textposition='outside', textfont_size=15) # Config. de las etiquetas de las barras.
            fig.update_layout(xaxis=dict(tickangle=-45, tickfont=dict(size=15)),
                              yaxis=dict(showticklabels=False, range=[0, 2.5]))
            
            st.plotly_chart(fig, use_container_width=True, height=200)
            
        # 6.1.3° Rectas de respuestas
        st.markdown("---") #separador
        df_aux=df_final.copy()
        
        # Crear el gráfico de líneas con Plotly Express
        fig = px.line()

        # Agregar líneas punteadas hacia arriba en cada fecha
        for date in df_aux['Fecha']:
            fig.add_shape(
                type='line',
                x0=date,
                x1=date,
                y0=-2,
                y1=df_aux['Nro de respuestas'].max()+2,
                line=dict(dash='dash', color='#FFFF93'),
                name='Nro de respuestas'
            )
        
        # Añadir otra línea para 'Nro de respuestas'
        fig.add_trace(
            go.Scatter(
                x=df_aux['Fecha'],
                y=df_aux['Nro de respuestas'],
                mode='lines+markers',  # Incluir línea y puntos
                line=dict(color='blue'), # Color de la línea
                marker=dict(size=10), # Tamaño de los puntos
                name='Nro de respuestas'
            )
        )
        # Añadir otra línea para 'Nro de intermitencias'
        fig.add_trace(
            go.Scatter(
                x=df_aux['Fecha'],
                y=df_aux['Nro de intermitencias'],
                mode='lines+markers',  # Incluir línea y puntos
                line=dict(color='red'), # Color de la línea
                marker=dict(size=10), # Tamaño de los puntos
                name='Nro de intermitencias'
            )
        )
        fig.update_layout(xaxis=dict(tickangle=-45, tickfont=dict(size=15)),
                          yaxis=dict(tickfont=dict(size=15),dtick=3))

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig,use_container_width=True, height=200) #Poner altura y autoajustar en el horizontal.



    except Exception as e:
        st.markdown("...(Espera)")