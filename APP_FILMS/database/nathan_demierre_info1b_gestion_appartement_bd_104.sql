-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: nathan_demierre_info1b_gestion_appartement_bd_104

-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS nathan_demierre_info1b_gestion_appartement_bd_104;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS nathan_demierre_info1b_gestion_appartement_bd_104;

-- Utilisation de cette base de donnée

USE nathan_demierre_info1b_gestion_appartement_bd_104;
-- --------------------------------------------------------


--
-- Table structure for table `t_appartement`
--

CREATE TABLE `t_appartement` (
  `Id_appartement` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_appartement`
--

INSERT INTO `t_appartement` (`Id_appartement`) VALUES
(1);

-- --------------------------------------------------------

--
-- Table structure for table `t_armoir`
--

CREATE TABLE `t_armoir` (
  `Id_armoir` int(11) NOT NULL,
  `Fk_piece` int(11) NOT NULL,
  `Nom_armoir` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_armoir`
--

INSERT INTO `t_armoir` (`Id_armoir`, `Fk_piece`, `Nom_armoir`) VALUES
(1, 1, '');

-- --------------------------------------------------------

--
-- Table structure for table `t_avoir_contenu`
--

CREATE TABLE `t_avoir_contenu` (
  `Id_avoir_contenu` int(11) NOT NULL,
  `Fk_armoir` int(11) NOT NULL,
  `Fk_contenu` int(11) NOT NULL,
  `Nb_contenu` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_avoir_contenu`
--

INSERT INTO `t_avoir_contenu` (`Id_avoir_contenu`, `Fk_armoir`, `Fk_contenu`, `Nb_contenu`) VALUES
(1, 1, 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `t_avoir_droit`
--

CREATE TABLE `t_avoir_droit` (
  `id_avoir_droit` int(11) NOT NULL,
  `Fk_personne` int(11) NOT NULL,
  `Fk_droit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_avoir_droit`
--

INSERT INTO `t_avoir_droit` (`id_avoir_droit`, `Fk_personne`, `Fk_droit`) VALUES
(1, 1, 2),
(2, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `t_avoir_lit`
--

CREATE TABLE `t_avoir_lit` (
  `Id_avoir_lit` int(11) NOT NULL,
  `Fk_piece` int(11) NOT NULL,
  `Fk_lit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_avoir_lit`
--

INSERT INTO `t_avoir_lit` (`Id_avoir_lit`, `Fk_piece`, `Fk_lit`) VALUES
(1, 1, 1),
(2, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `t_contenu`
--

CREATE TABLE `t_contenu` (
  `Id_contenu` int(11) NOT NULL,
  `contenu` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_contenu`
--

INSERT INTO `t_contenu` (`Id_contenu`, `contenu`) VALUES
(1, 'couverturesrdous'),
(2, 'testt'),
(3, 'test'),
(4, 're');

-- --------------------------------------------------------

--
-- Table structure for table `t_droit`
--

CREATE TABLE `t_droit` (
  `id_droit` int(11) NOT NULL,
  `droit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_droit`
--

INSERT INTO `t_droit` (`id_droit`, `droit`) VALUES
(1, 'User'),
(2, 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `t_etat_lit`
--

CREATE TABLE `t_etat_lit` (
  `Id_etat_lit` int(11) NOT NULL,
  `Etat_lit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_etat_lit`
--

INSERT INTO `t_etat_lit` (`Id_etat_lit`, `Etat_lit`) VALUES
(1, 'Fait'),
(2, 'Pas fait');

-- --------------------------------------------------------

--
-- Table structure for table `t_lit`
--

CREATE TABLE `t_lit` (
  `Id_lit` int(11) NOT NULL,
  `Fk_type_lit` int(11) NOT NULL,
  `Fk_etat_lit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_lit`
--

INSERT INTO `t_lit` (`Id_lit`, `Fk_type_lit`, `Fk_etat_lit`) VALUES
(1, 1, 1),
(2, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `t_personne`
--

CREATE TABLE `t_personne` (
  `Id_personne` int(11) NOT NULL,
  `Nom_personne` varchar(50) NOT NULL,
  `Prenom_personne` varchar(50) NOT NULL,
  `Date_naissance_personne` date DEFAULT NULL,
  `Adresse_mail_personne` varchar(100) NOT NULL,
  `MDP_personne` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_personne`
--

INSERT INTO `t_personne` (`Id_personne`, `Nom_personne`, `Prenom_personne`, `Date_naissance_personne`, `Adresse_mail_personne`, `MDP_personne`) VALUES
(1, 'demierre', 'nathan', '2021-03-08', 'nathan.demierre@gmail.com', '*79A8858EDF279DC3B99BA41350FE3CF1ABEFC655');

-- --------------------------------------------------------

--
-- Table structure for table `t_piece`
--

CREATE TABLE `t_piece` (
  `Id_piece` int(11) NOT NULL,
  `Fk_appartement` int(11) NOT NULL,
  `Nom_piece` varchar(50) NOT NULL,
  `Surface_piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_piece`
--

INSERT INTO `t_piece` (`Id_piece`, `Fk_appartement`, `Nom_piece`, `Surface_piece`) VALUES
(1, 1, 'Chambre 1', 12);

-- --------------------------------------------------------

--
-- Table structure for table `t_reservations`
--

CREATE TABLE `t_reservations` (
  `Id_reservations` int(11) NOT NULL,
  `Fk_personne` int(11) NOT NULL,
  `Fk_appartement` int(11) NOT NULL,
  `Date_reservations` date NOT NULL,
  `Nombre_personne` int(11) NOT NULL,
  `Nombre_jour_reservations` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_reservations`
--

INSERT INTO `t_reservations` (`Id_reservations`, `Fk_personne`, `Fk_appartement`, `Date_reservations`, `Nombre_personne`, `Nombre_jour_reservations`) VALUES
(1, 1, 1, '2021-04-02', 5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `t_type_lit`
--

CREATE TABLE `t_type_lit` (
  `Id_type_lit` int(11) NOT NULL,
  `Type_lit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_type_lit`
--

INSERT INTO `t_type_lit` (`Id_type_lit`, `Type_lit`) VALUES
(1, 'Lit simple'),
(2, 'Lit double'),
(3, 'lit superposer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `t_appartement`
--
ALTER TABLE `t_appartement`
  ADD PRIMARY KEY (`Id_appartement`);

--
-- Indexes for table `t_armoir`
--
ALTER TABLE `t_armoir`
  ADD PRIMARY KEY (`Id_armoir`),
  ADD KEY `Fk_piece` (`Fk_piece`);

--
-- Indexes for table `t_avoir_contenu`
--
ALTER TABLE `t_avoir_contenu`
  ADD PRIMARY KEY (`Id_avoir_contenu`),
  ADD KEY `Fk_armoir` (`Fk_armoir`),
  ADD KEY `Fk_contenu` (`Fk_contenu`);

--
-- Indexes for table `t_avoir_droit`
--
ALTER TABLE `t_avoir_droit`
  ADD PRIMARY KEY (`id_avoir_droit`),
  ADD KEY `Fk_personne` (`Fk_personne`),
  ADD KEY `Fk_droit` (`Fk_droit`);

--
-- Indexes for table `t_avoir_lit`
--
ALTER TABLE `t_avoir_lit`
  ADD PRIMARY KEY (`Id_avoir_lit`),
  ADD KEY `Fk_piece` (`Fk_piece`,`Fk_lit`),
  ADD KEY `Fk_lit` (`Fk_lit`);

--
-- Indexes for table `t_contenu`
--
ALTER TABLE `t_contenu`
  ADD PRIMARY KEY (`Id_contenu`);

--
-- Indexes for table `t_droit`
--
ALTER TABLE `t_droit`
  ADD PRIMARY KEY (`id_droit`);

--
-- Indexes for table `t_etat_lit`
--
ALTER TABLE `t_etat_lit`
  ADD PRIMARY KEY (`Id_etat_lit`);

--
-- Indexes for table `t_lit`
--
ALTER TABLE `t_lit`
  ADD PRIMARY KEY (`Id_lit`),
  ADD KEY `Fk_etat_lit` (`Fk_etat_lit`),
  ADD KEY `Fk_type_lit` (`Fk_type_lit`);

--
-- Indexes for table `t_personne`
--
ALTER TABLE `t_personne`
  ADD PRIMARY KEY (`Id_personne`);

--
-- Indexes for table `t_piece`
--
ALTER TABLE `t_piece`
  ADD PRIMARY KEY (`Id_piece`),
  ADD KEY `Fk_appartement` (`Fk_appartement`);

--
-- Indexes for table `t_reservations`
--
ALTER TABLE `t_reservations`
  ADD PRIMARY KEY (`Id_reservations`),
  ADD KEY `Fk_personne` (`Fk_personne`),
  ADD KEY `Fk_appartement` (`Fk_appartement`);

--
-- Indexes for table `t_type_lit`
--
ALTER TABLE `t_type_lit`
  ADD PRIMARY KEY (`Id_type_lit`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `t_appartement`
--
ALTER TABLE `t_appartement`
  MODIFY `Id_appartement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `t_armoir`
--
ALTER TABLE `t_armoir`
  MODIFY `Id_armoir` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `t_avoir_contenu`
--
ALTER TABLE `t_avoir_contenu`
  MODIFY `Id_avoir_contenu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `t_avoir_droit`
--
ALTER TABLE `t_avoir_droit`
  MODIFY `id_avoir_droit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `t_avoir_lit`
--
ALTER TABLE `t_avoir_lit`
  MODIFY `Id_avoir_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `t_contenu`
--
ALTER TABLE `t_contenu`
  MODIFY `Id_contenu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `t_droit`
--
ALTER TABLE `t_droit`
  MODIFY `id_droit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `t_etat_lit`
--
ALTER TABLE `t_etat_lit`
  MODIFY `Id_etat_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `t_lit`
--
ALTER TABLE `t_lit`
  MODIFY `Id_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `t_personne`
--
ALTER TABLE `t_personne`
  MODIFY `Id_personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `t_piece`
--
ALTER TABLE `t_piece`
  MODIFY `Id_piece` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `t_reservations`
--
ALTER TABLE `t_reservations`
  MODIFY `Id_reservations` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `t_type_lit`
--
ALTER TABLE `t_type_lit`
  MODIFY `Id_type_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `t_armoir`
--
ALTER TABLE `t_armoir`
  ADD CONSTRAINT `t_armoir_ibfk_1` FOREIGN KEY (`Fk_piece`) REFERENCES `t_piece` (`Id_piece`);

--
-- Constraints for table `t_avoir_contenu`
--
ALTER TABLE `t_avoir_contenu`
  ADD CONSTRAINT `t_avoir_contenu_ibfk_1` FOREIGN KEY (`Fk_armoir`) REFERENCES `t_armoir` (`Id_armoir`),
  ADD CONSTRAINT `t_avoir_contenu_ibfk_2` FOREIGN KEY (`Fk_contenu`) REFERENCES `t_contenu` (`Id_contenu`);

--
-- Constraints for table `t_avoir_droit`
--
ALTER TABLE `t_avoir_droit`
  ADD CONSTRAINT `t_avoir_droit_ibfk_1` FOREIGN KEY (`Fk_personne`) REFERENCES `t_personne` (`Id_personne`),
  ADD CONSTRAINT `t_avoir_droit_ibfk_2` FOREIGN KEY (`Fk_droit`) REFERENCES `t_droit` (`id_droit`);

--
-- Constraints for table `t_avoir_lit`
--
ALTER TABLE `t_avoir_lit`
  ADD CONSTRAINT `t_avoir_lit_ibfk_1` FOREIGN KEY (`Fk_lit`) REFERENCES `t_lit` (`Id_lit`),
  ADD CONSTRAINT `t_avoir_lit_ibfk_2` FOREIGN KEY (`Fk_piece`) REFERENCES `t_piece` (`Id_piece`);

--
-- Constraints for table `t_lit`
--
ALTER TABLE `t_lit`
  ADD CONSTRAINT `t_lit_ibfk_1` FOREIGN KEY (`Fk_etat_lit`) REFERENCES `t_etat_lit` (`Id_etat_lit`),
  ADD CONSTRAINT `t_lit_ibfk_2` FOREIGN KEY (`Fk_type_lit`) REFERENCES `t_type_lit` (`Id_type_lit`);

--
-- Constraints for table `t_piece`
--
ALTER TABLE `t_piece`
  ADD CONSTRAINT `t_piece_ibfk_1` FOREIGN KEY (`Fk_appartement`) REFERENCES `t_appartement` (`Id_appartement`);

--
-- Constraints for table `t_reservations`
--
ALTER TABLE `t_reservations`
  ADD CONSTRAINT `t_reservations_ibfk_1` FOREIGN KEY (`Fk_personne`) REFERENCES `t_personne` (`Id_personne`),
  ADD CONSTRAINT `t_reservations_ibfk_2` FOREIGN KEY (`Fk_appartement`) REFERENCES `t_appartement` (`Id_appartement`);
COMMIT;