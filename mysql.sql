SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- --------------------------------------------------------

--
-- Table structure for table `people`
--

CREATE TABLE IF NOT EXISTS `people` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tag_id` varchar(25) NOT NULL,
  `name` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `readings`
--

CREATE TABLE IF NOT EXISTS `readings` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `reader_id` int(11) unsigned NOT NULL,
  `tag_id` varchar(25) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `walls`
--

CREATE TABLE IF NOT EXISTS `walls` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `rope_num` int(11) unsigned NOT NULL,
  `height` int(11) unsigned NOT NULL,
  `reader_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

