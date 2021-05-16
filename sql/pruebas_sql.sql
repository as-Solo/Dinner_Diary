drop database diary

USE diary

SELECT * FROM ciudades
SELECT * FROM paises
SELECT * FROM ciudades
SELECT * FROM municipios
SELECT * FROM etiquetas
SELECT * FROM cp

SELECT * FROM restaurantes where direccion = 'General Ricardos, 19'
SELECT * FROM usuarios
SELECT * FROM visitado

DELETE FROM restaurantes WHERE direccion = 'La mia'



Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column.  To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.
