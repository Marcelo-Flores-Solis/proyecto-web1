-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 24-12-2025 a las 06:23:33
-- Versión del servidor: 8.4.7
-- Versión de PHP: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `biblioteca`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

DROP TABLE IF EXISTS `libros`;
CREATE TABLE IF NOT EXISTS `libros` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `autor` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categoria` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `img` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sinopsis` text COLLATE utf8mb4_unicode_ci,
  `disponible` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id`, `titulo`, `autor`, `categoria`, `img`, `sinopsis`, `disponible`) VALUES
(1, 'Violet Evergarden', 'Kana Akatsuki', NULL, 'https://m.media-amazon.com/images/M/MV5BMWUwNDFiNjQtYjQ0MC00MTcxLWE0MGQtNTdkYTlhZGU2NDFmXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', 'Una \"Auto Memory Doll\" ex-soldado viaja escribiendo cartas para otros mientras intenta entender qué significa \"Te amo\".', 0),
(2, 'Your Name (Novela)', 'Makoto Shinkai', NULL, 'https://m.media-amazon.com/images/M/MV5BMTIyNzFjNzItZmQ1MC00NzhjLThmMzYtZjRhN2Y3MmM2OGQyXkEyXkFqcGc@._V1_.jpg', 'Mitsuha y Taki, dos estudiantes separados por la distancia, comienzan a intercambiar cuerpos en sueños.', 0),
(3, 'Re:Zero - Empezar de cero', 'Tappei Nagatsuki', NULL, 'https://upload.wikimedia.org/wikipedia/en/3/3c/Re-Zero_kara_Hajimeru_Isekai_Seikatsu_light_novel_volume_1_cover.jpg', 'Subaru es invocado a otro mundo donde descubre que tiene el poder de retroceder el tiempo cada vez que muere.', 1),
(4, 'No Game No Life', 'Yuu Kamiya', NULL, 'https://images-na.ssl-images-amazon.com/images/I/91KqqL5ae0L._AC_UL600_SR600,600_.jpg', 'Dos hermanos gamers invencibles son llevados a un mundo donde todo conflicto se resuelve mediante juegos de ingenio.', 0),
(5, 'Overlord', 'Kugane Maruyama', NULL, 'https://m.media-amazon.com/images/M/MV5BYjNjNDBmZjAtMGZiMS00ODBkLWFjYWItZWQ1ZjEwOGNmZDBjXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', 'Un jugador decide quedarse conectado hasta el final de un juego y se convierte en un poderoso Rey Exánime en un nuevo mundo.', 1),
(6, 'Konosuba', 'Natsume Akatsuki', NULL, 'https://upload.wikimedia.org/wikipedia/en/3/3e/Kono_Subarashii_Sekai_ni_Shukufuku_o%21_light_novel_volume_1_cover.jpg', 'Kazuma reencarna en un mundo de fantasía con una diosa inútil, una maga que solo usa explosiones y una paladín masoquista.', 1),
(7, 'Mushoku Tensei', 'Rifujin na Magonote', NULL, 'https://i5.walmartimages.com/seo/Mushoku-Tensei-Jobless-Reincarnation-Light-Novel-Mushoku-Tensei-Jobless-Reincarnation-Light-Novel-Vol-26-Paperback_aa2905ff-eb1e-49d1-ad24-68c33e659046.7fb646ad4596758a0cad40f9ae1c0ad8.jpeg', 'Un \"nini\" reencarna como un bebé prodigio de la magia y promete vivir su nueva vida al máximo sin arrepentimientos.', 0),
(8, 'Toradora!', 'Yuyuko Takemiya', NULL, 'https://m.media-amazon.com/images/M/MV5BNjEyZmRmMGYtNGY1Zi00MTFiLWE0ZTMtNzUzMWJmMTgzNWE5XkEyXkFqcGc@._V1_.jpg', 'Un chico con cara de delincuente y una chica pequeña pero violenta se alían para ayudarse mutuamente en el amor.', 1),
(9, 'Sword Art Online: Aincrad', 'Reki Kawahara', NULL, 'https://proassetspdlcom.cdnstatics2.com/usuaris/libros/fotos/206/original/portada_sword-art-online-novela-n-01_reki-kawahara_201512161024.jpg', 'Atrapados en un juego de realidad virtual, si mueres en el juego, mueres en la vida real. Kirito debe llegar al piso 100.', 1),
(10, 'Solo Leveling', 'Chugong', NULL, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjjydKUpH1rz3V2N2oTcKX7O3QIMkH_-xqqw&s', 'El cazador más débil del mundo despierta un poder único: un sistema de videojuego que solo él puede ver.', 1),
(11, 'Naruto (Vol. 1)', 'Masashi Kishimoto', NULL, 'https://upload.wikimedia.org/wikipedia/en/9/94/NarutoCoverTankobon1.jpg', 'Naruto Uzumaki es un ninja marginado que sueña con convertirse en Hokage, el líder de su aldea.', 1),
(12, 'One Piece (Vol. 1)', 'Eiichiro Oda', NULL, 'https://upload.wikimedia.org/wikipedia/en/a/a3/One_Piece%2C_Volume_1.jpg', 'Monkey D. Luffy zarpa al mar para encontrar el tesoro legendario One Piece y convertirse en el Rey de los Piratas.', 1),
(13, 'Death Note', 'Tsugumi Ohba', NULL, 'https://upload.wikimedia.org/wikipedia/en/6/6f/Death_Note_Vol_1.jpg', 'Light Yagami encuentra un cuaderno capaz de matar a cualquier persona cuyo nombre sea escrito en él.', 1),
(14, 'Fullmetal Alchemist', 'Hiromu Arakawa', NULL, 'https://i5.walmartimages.com/seo/Hiromu-Arakawa-Fullmetal-Alchemist-Book-1-3-in-1-Edition-Paperback_35db1f51-d0c8-48d2-9b8a-68221112223d_1.67579e085b08f0d657a0992db0719eb7.jpeg', 'Dos hermanos alquimistas buscan la Piedra Filosofal para recuperar sus cuerpos perdidos tras un experimento fallido.', 1),
(15, 'Attack on Titan', 'Hajime Isayama', NULL, 'https://upload.wikimedia.org/wikipedia/en/d/d6/Shingeki_no_Kyojin_manga_volume_1.jpg', 'La humanidad vive rodeada de muros para protegerse de los Titanes. Eren Yeager jura eliminarlos a todos.', 1),
(16, 'Demon Slayer (Kimetsu)', 'Koyoharu Gotouge', NULL, 'https://upload.wikimedia.org/wikipedia/en/0/09/Demon_Slayer_-_Kimetsu_no_Yaiba%2C_volume_1.jpg', 'Tanjiro se convierte en cazador de demonios para encontrar una cura para su hermana Nezuko.', 0),
(17, 'Tokyo Ghoul', 'Sui Ishida', NULL, 'https://upload.wikimedia.org/wikipedia/en/e/e5/Tokyo_Ghoul_volume_1_cover.jpg', 'Ken Kaneki se convierte en mitad ghoul tras sobrevivir a un ataque, y debe aprender a vivir entre dos mundos.', 1),
(18, 'Spy x Family', 'Tatsuya Endo', NULL, 'https://cdn.kobo.com/book-images/07d1ab28-6fb4-4bfd-b125-21354e434b17/1200/1200/False/spy-x-family-vol-1.jpg\n', 'Un espía debe formar una familia falsa para una misión. Sin saberlo, adopta a una telépata y se casa con una asesina.', 1),
(19, 'Chainsaw Man', 'Tatsuki Fujimoto', NULL, 'https://cdn.kobo.com/book-images/f9e6e611-ebd8-4473-8116-d642e619a1cb/1200/1200/False/chainsaw-man-vol-12.jpg\n', 'Denji, un joven pobre que caza demonios, se fusiona con su perro demonio Pochita.', 1),
(20, 'Jujutsu Kaisen', 'Gege Akutami', NULL, 'https://static.wikia.nocookie.net/jujutsu-kaisen/images/8/8c/Jujutsu_Kaisen_Manga_Volumen_25_JP.jpg/revision/latest?cb=20240312225729&path-prefix=es\n', 'Yuji Itadori se traga un objeto maldito para salvar a sus amigos y se convierte en el recipiente de Sukuna.', 1),
(21, 'Don Quijote de la Mancha', 'Miguel de Cervantes', NULL, 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Title_page_first_edition_Don_Quijote.jpg/400px-Title_page_first_edition_Don_Quijote.jpg', 'Un hidalgo pierde la cordura por leer novelas de caballería y sale a buscar aventuras.', 0),
(22, 'El Señor de los Anillos', 'J.R.R. Tolkien', NULL, 'https://www.planetadelibros.com.uy/usuaris/libros/fotos/412/original/411717_portada_el-senor-de-los-anillos-1-la-comunidad-del-anillo_j-r-r-tolkien_202207271304.jpg', 'Frodo Bolsón hereda un anillo que puede destruir el mundo y debe emprender un viaje peligroso.', 1),
(23, 'Cien años de soledad', 'Gabriel García Márquez', NULL, 'https://www.penguinlibros.com/pe/4560061/cien-anos-de-soledad.jpg\n', 'La historia de la familia Buendía a lo largo de siete generaciones en el pueblo de Macondo.', 1),
(24, 'Harry Potter y la Piedra Filosofal', 'J.K. Rowling', NULL, 'https://upload.wikimedia.org/wikipedia/en/6/6b/Harry_Potter_and_the_Philosopher%27s_Stone_Book_Cover.jpg', 'Harry descubre en su cumpleaños número 11 que es un mago y es invitado a Hogwarts.', 1),
(25, 'Dune', 'Frank Herbert', NULL, 'https://upload.wikimedia.org/wikipedia/en/d/de/Dune-Frank_Herbert_%281965%29_First_edition.jpg', 'En el planeta desértico Arrakis, Paul Atreides debe liderar una batalla por el control de la especia.', 1),
(26, 'Orgullo y Prejuicio', 'Jane Austen', NULL, 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/PrideAndPrejudiceTitlePage.jpg/300px-PrideAndPrejudiceTitlePage.jpg', 'Elizabeth Bennet y el Sr. Darcy deben superar sus propios orgullos para descubrir el amor.', 1),
(27, 'El Principito', 'Antoine de Saint-Exupéry', NULL, 'https://upload.wikimedia.org/wikipedia/en/0/05/Littleprince.JPG', 'Un piloto perdido en el desierto se encuentra con un pequeño príncipe de otro planeta.', 1),
(28, 'Frankenstein', 'Mary Shelley', NULL, 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Frankenstein_1818_edition_title_page.jpg/300px-Frankenstein_1818_edition_title_page.jpg', 'El científico Víctor Frankenstein crea una criatura sapiente pero luego la rechaza con horror.', 1),
(29, 'Drácula', 'Bram Stoker', NULL, 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Dracula_1st_ed_cover_reproduction.jpg/300px-Dracula_1st_ed_cover_reproduction.jpg', 'El Conde Drácula intenta mudarse de Transilvania a Inglaterra para encontrar sangre nueva.', 0),
(30, 'Fahrenheit 451', 'Ray Bradbury', NULL, 'https://upload.wikimedia.org/wikipedia/en/d/db/Fahrenheit_451_1st_ed_cover.jpg', 'En una sociedad futurista donde los libros están prohibidos, Guy Montag es un bombero que los quema.', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

DROP TABLE IF EXISTS `prestamos`;
CREATE TABLE IF NOT EXISTS `prestamos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `libro_id` int DEFAULT NULL,
  `fecha_prestamo` date DEFAULT NULL,
  `fecha_devolucion` date DEFAULT NULL,
  `estado` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'activo',
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `libro_id` (`libro_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rol` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'lector',
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password`, `rol`, `fecha_registro`) VALUES
(1, 'Administrador', 'admin@zebralibra.com', '1234', 'admin', '2025-12-23 22:13:40'),
(2, 'ew', 'ramiro@gmail.com', '1212', 'lector', '2025-12-24 01:13:25');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
