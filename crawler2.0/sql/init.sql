-- auto-generated definition
CREATE TABLE product_comment_detail
(
  id              INT AUTO_INCREMENT
    PRIMARY KEY,
  comment_info_id INT NOT NULL,
  product_id      INT NOT NULL
);

CREATE INDEX product_comment_detail_product_id_7d791171_fk_product_info_id
  ON product_comment_detail (product_id);

CREATE INDEX product_comm_comment_info_id_d5c98461_fk_product_comment_info_id
  ON product_comment_detail (comment_info_id);

-- auto-generated definition
CREATE TABLE product_comment_info
(
  id           INT AUTO_INCREMENT
    PRIMARY KEY,
  content      LONGTEXT    NOT NULL,
  user_name    VARCHAR(50) NOT NULL,
  comment_time DATE        NOT NULL
);

-- auto-generated definition
CREATE TABLE product_download_detail
(
  id         INT AUTO_INCREMENT
    PRIMARY KEY,
  address_id INT NOT NULL,
  product_id INT NOT NULL
);

CREATE INDEX product_download_detail_product_id_b131eef8_fk_product_info_id
  ON product_download_detail (product_id);

CREATE INDEX product_downlo_address_id_ae2589b0_fk_public_download_address_id
  ON product_download_detail (address_id);

-- auto-generated definition
CREATE TABLE product_images_detail
(
  id         INT AUTO_INCREMENT
    PRIMARY KEY,
  image_id   INT NOT NULL,
  product_id INT NOT NULL
);

CREATE INDEX product_images_detail_image_id_f148e4c3_fk_public_images_id
  ON product_images_detail (image_id);

CREATE INDEX product_images_detail_product_id_c8fa26fd_fk_product_info_id
  ON product_images_detail (product_id);

-- auto-generated definition
CREATE TABLE product_info
(
  id              INT AUTO_INCREMENT
    PRIMARY KEY,
  product_name    VARCHAR(200)                        NOT NULL,
  detail          INT                                 NOT NULL,
  status          SMALLINT(6)                         NOT NULL,
  create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  update_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  order_index     INT                                 NULL,
  product_type_id INT                                 NOT NULL,
  source_id       INT                                 NOT NULL
);

CREATE INDEX order_index
  ON product_info (order_index);

CREATE INDEX product_info_product_type_id_c76e5879_fk_product_type_id
  ON product_info (product_type_id);

CREATE INDEX product_info_source_id_63f852a9_fk_public_data_source_id
  ON product_info (source_id);

CREATE INDEX product_name
  ON product_info (product_name);

-- auto-generated definition
CREATE TABLE product_movie_detail
(
  id            INT AUTO_INCREMENT
    PRIMARY KEY,
  product_name  VARCHAR(200)                        NOT NULL,
  product_alias VARCHAR(200)                        NOT NULL,
  rating        VARCHAR(500)                        NULL,
  rating_sum    INT                                 NOT NULL,
  release_time  DATE                                NULL,
  about         LONGTEXT                            NULL,
  content       LONGTEXT                            NULL,
  area          VARCHAR(100)                        NULL,
  status        SMALLINT(6)                         NOT NULL,
  douban_id     INT                                 NULL,
  source_url    VARCHAR(500)                        NULL,
  update_time   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  create_time   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX rating
  ON product_movie_detail (rating);

-- auto-generated definition
CREATE TABLE product_sub_type_detail
(
  id          INT AUTO_INCREMENT
    PRIMARY KEY,
  product_id  INT NOT NULL,
  sub_type_id INT NOT NULL
);

CREATE INDEX product_sub_type_detail_product_id_eb1ef6c1_fk_product_info_id
  ON product_sub_type_detail (product_id);

CREATE INDEX product_sub_type_detail_sub_type_id_585fa800_fk_product_type_id
  ON product_sub_type_detail (sub_type_id);

-- auto-generated definition
CREATE TABLE product_type
(
  id          INT AUTO_INCREMENT
    PRIMARY KEY,
  parent_id   INT                                 NOT NULL,
  `key`       VARCHAR(50)                         NOT NULL,
  name        VARCHAR(50)                         NOT NULL,
  `describe`  VARCHAR(200)                        NULL,
  status      SMALLINT(6)                         NOT NULL,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- auto-generated definition
CREATE TABLE public_data_source
(
  id          INT AUTO_INCREMENT
    PRIMARY KEY,
  source_name VARCHAR(100)                        NOT NULL,
  `key`       VARCHAR(50)                         NOT NULL,
  source_type SMALLINT(6)                         NOT NULL,
  status      SMALLINT(6)                         NOT NULL,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- auto-generated definition
CREATE TABLE public_dictionary
(
  id     INT AUTO_INCREMENT
    PRIMARY KEY,
  `key`  VARCHAR(50)  NOT NULL,
  value  VARCHAR(200) NOT NULL,
  `desc` LONGTEXT     NULL
);

-- auto-generated definition
CREATE TABLE public_download_address
(
  id            INT AUTO_INCREMENT
    PRIMARY KEY,
  download_url  VARCHAR(1000)                       NOT NULL,
  download_type SMALLINT(6)                         NOT NULL,
  status        SMALLINT(6)                         NOT NULL,
  create_time   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- auto-generated definition
CREATE TABLE public_images
(
  id          INT AUTO_INCREMENT
    PRIMARY KEY,
  image       VARCHAR(500)                        NOT NULL,
  img_type    SMALLINT(6)                         NOT NULL,
  status      SMALLINT(6)                         NOT NULL,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- auto-generated definition
CREATE TABLE sensitive_words
(
  id        INT AUTO_INCREMENT
    PRIMARY KEY,
  word      VARCHAR(20) NOT NULL,
  word_type SMALLINT(6) NOT NULL
);

--  ************************

ALTER TABLE `product_info`
  CHANGE COLUMN `update_time` `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  AFTER `create_time`;
ALTER TABLE `product_movie_detail`
  CHANGE COLUMN `update_time` `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  AFTER `create_time`;


INSERT INTO `public_data_source` (`id`, `source_name`, `key`, `source_type`, `status`) VALUES
  (1, 'ibl', 'ibl', 1, 1),
  (2, 'douban', 'douban', 1, 1);

INSERT INTO `product_type` (`id`, `parent_id`, `key`, `name`, `describe`, `status`)
VALUES (1, '0', 'movie', 'movie', 'movie', '1');