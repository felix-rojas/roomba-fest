# roomba-fest

## Template

La carpeta template tiene el ejemplo de la clase con server-client

## Assets

La carpeta [Scripts](./roomba-fest/Assets/Scripts) contiene el [WebClient](./roomba-fest/Assets/Scripts/WebClient.cs) modificado para las llamadas http de Unity

La carpeta Assets contiene el directorio [Server](./roomba-fest/Assets/Scripts/Server), que aloja el código segmentado del servidor de Python y el grid.txt a cargar.

El archivo a correr es [Server.py](./roomba-fest/Assets/Scripts/Server/Server.py) en el folder [Server](./roomba-fest/Assets/Scripts/Server)

El archivo con la grilla es [grid.txt](./roomba-fest/Assets/Scripts/Server/grid.txt) en el folder [Server](./roomba-fest/Assets/Scripts/Server) y es el que el servidor de Python utiliza para cargar la simulación.

Los archivos en el folder [Model](./roomba-fest/Assets/Scripts/Model) son los datos a serializar y las propiedades del agente con las que se instancian.
