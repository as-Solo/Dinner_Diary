drop database diary

USE diary

SELECT * FROM ciudades
SELECT * FROM paises
SELECT * FROM ciudades
SELECT * FROM municipios
SELECT * FROM etiquetas
SELECT * FROM cp

SELECT * FROM restaurantes
SELECT * FROM usuarios
SELECT * FROM visitado

DELETE FROM visitado WHERE id_visitado = 4

select etiqueta from etiquetas

SELECT restaurantes.id_rest
FROM restaurantes
WHERE restaurantes.nombre = 'Restaurante Italiano San Marcos' AND restaurantes.direccion = 'Calle Doctor Pedro de Castro 1'

SELECT *
FROM restaurantes
WHERE restaurantes.nombre = "Casa Enriqueta"

SELECT *
FROM restaurantes
WHERE restaurantes.busquedas = 2

INSERT INTO restaurantes (restaurantes.busquedas)
VALUES (0)
WHERE restaurantes.nombre = "Casa Enriqueta"

UPDATE restaurantes
SET restaurantes.busquedas = 0
        
SELECT *
FROM etiquetas
WHERE etiquetas.id_etiqueta = 8553


SELECT restaurantes.nombre, restaurantes.latitud, restaurantes.longitud
        
FROM usuarios

INNER JOIN visitado
ON visitado.id_usuario = usuarios.id_usuario

INNER JOIN restaurantes
ON restaurantes.id_rest = visitado.id_rest

WHERE usuarios.id_usuario = 1  

DELETE FROM visitado
WHERE visitado.id_usuario = 26 AND visitado.comentario = "No sé ni dónde está"


SELECT visitado.comentario
FROM visitado
WHERE visitado.id_usuario = 26