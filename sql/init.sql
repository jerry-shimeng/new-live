/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
 
CREATE TABLE IF NOT EXISTS `product_comment_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_info_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_comm_comment_info_id_d5c98461_fk_product_comment_info_id` (`comment_info_id`),
  KEY `product_comment_detail_product_id_7d791171_fk_product_info_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `product_comment_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `comment_time` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `product_download_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_downlo_address_id_ae2589b0_fk_public_download_address_id` (`address_id`),
  KEY `product_download_detail_product_id_b131eef8_fk_product_info_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `product_images_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_images_detail_image_id_f148e4c3_fk_public_images_id` (`image_id`),
  KEY `product_images_detail_product_id_c8fa26fd_fk_product_info_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `product_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) NOT NULL,
  `detail` int(11) NOT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `order_index` int(11) DEFAULT NULL,
  `product_type_id` int(11) NOT NULL,
  `source_id` int(11) NOT NULL,
  `hot` tinyint default '0'  NOT null,
  PRIMARY KEY (`id`),
  KEY `product_info_product_type_id_c76e5879_fk_product_type_id` (`product_type_id`),
  KEY `product_info_source_id_63f852a9_fk_public_data_source_id` (`source_id`),
  KEY `order_index` (`order_index`),
  FULLTEXT KEY `product_name` (`product_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `product_movie_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) NOT NULL,
  `product_alias` varchar(200) NOT NULL,
  `rating` VARCHAR(200) NOT NULL,
  `score` double default '0' NOT null,
  `rating_sum` int(11) NOT NULL,
  `release_time` date,
  `about` longtext,
  `content` longtext,
  `area` varchar(100) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `douban_id` int null,
  `source_url` varchar(500) null,
  `update_time` timestamp ON UPDATE CURRENT_TIMESTAMP not null,
	`create_time` timestamp default CURRENT_TIMESTAMP not null,
  PRIMARY KEY (`id`),
  KEY `score` (`score`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `product_sub_type_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `sub_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_sub_type_detail_product_id_eb1ef6c1_fk_product_info_id` (`product_id`),
  KEY `product_sub_type_detail_sub_type_id_585fa800_fk_product_type_id` (`sub_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `product_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `key` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `describe` varchar(200) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `public_data_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_name` varchar(100) NOT NULL,
  `key` varchar(50) NOT NULL,
  `source_type` smallint(6) NOT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `public_download_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `download_url` varchar(1000) NOT NULL,
  `download_type` smallint(6) NOT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `public_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(500) NOT NULL,
  `img_type` smallint(6) NOT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `sensitive_words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(20) NOT NULL,
  `word_type` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

-- 初始化部分数据
 
INSERT INTO `product_type` (`id`, `parent_id`, `key`, `name`, `describe`, `status`, `create_time`) VALUES
  (1, 0, 'movie', 'dy', NULL, 1, '2017-03-29 15:59:39');
 

/*!40000 ALTER TABLE `public_data_source` DISABLE KEYS */;
INSERT INTO `public_data_source` (`id`, `source_name`, `key`, `source_type`, `status`, `create_time`) VALUES
  (1, 'lbl', 'lbl', 1, 1, '2017-03-29 16:01:09'),
  (2, 'douban', 'douban', 1, 1, '2017-03-29 16:01:20');
/*!40000 ALTER TABLE `public_data_source` ENABLE KEYS */;
 