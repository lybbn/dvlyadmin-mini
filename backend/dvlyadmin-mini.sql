-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.7.26 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出  表 dvlyadmin_mini.auth_group 结构
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.auth_group 的数据：~0 rows (大约)
DELETE FROM `auth_group`;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.auth_group_permissions 结构
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.auth_group_permissions 的数据：~0 rows (大约)
DELETE FROM `auth_group_permissions`;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.auth_permission 结构
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.auth_permission 的数据：~72 rows (大约)
DELETE FROM `auth_permission`;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add permission', 1, 'add_permission'),
	(2, 'Can change permission', 1, 'change_permission'),
	(3, 'Can delete permission', 1, 'delete_permission'),
	(4, 'Can view permission', 1, 'view_permission'),
	(5, 'Can add group', 2, 'add_group'),
	(6, 'Can change group', 2, 'change_group'),
	(7, 'Can delete group', 2, 'delete_group'),
	(8, 'Can view group', 2, 'view_group'),
	(9, 'Can add content type', 3, 'add_contenttype'),
	(10, 'Can change content type', 3, 'change_contenttype'),
	(11, 'Can delete content type', 3, 'delete_contenttype'),
	(12, 'Can view content type', 3, 'view_contenttype'),
	(13, 'Can add session', 4, 'add_session'),
	(14, 'Can change session', 4, 'change_session'),
	(15, 'Can delete session', 4, 'delete_session'),
	(16, 'Can view session', 4, 'view_session'),
	(17, 'Can add captcha store', 5, 'add_captchastore'),
	(18, 'Can change captcha store', 5, 'change_captchastore'),
	(19, 'Can delete captcha store', 5, 'delete_captchastore'),
	(20, 'Can view captcha store', 5, 'view_captchastore'),
	(21, 'Can add 用户表', 6, 'add_users'),
	(22, 'Can change 用户表', 6, 'change_users'),
	(23, 'Can delete 用户表', 6, 'delete_users'),
	(24, 'Can view 用户表', 6, 'view_users'),
	(25, 'Can add 部门表', 7, 'add_dept'),
	(26, 'Can change 部门表', 7, 'change_dept'),
	(27, 'Can delete 部门表', 7, 'delete_dept'),
	(28, 'Can view 部门表', 7, 'view_dept'),
	(29, 'Can add 菜单表', 8, 'add_menu'),
	(30, 'Can change 菜单表', 8, 'change_menu'),
	(31, 'Can delete 菜单表', 8, 'delete_menu'),
	(32, 'Can view 菜单表', 8, 'view_menu'),
	(33, 'Can add 菜单权限表', 9, 'add_menubutton'),
	(34, 'Can change 菜单权限表', 9, 'change_menubutton'),
	(35, 'Can delete 菜单权限表', 9, 'delete_menubutton'),
	(36, 'Can view 菜单权限表', 9, 'view_menubutton'),
	(37, 'Can add 角色表', 10, 'add_role'),
	(38, 'Can change 角色表', 10, 'change_role'),
	(39, 'Can delete 角色表', 10, 'delete_role'),
	(40, 'Can view 角色表', 10, 'view_role'),
	(41, 'Can add 角色菜单权限表', 11, 'add_rolemenupermission'),
	(42, 'Can change 角色菜单权限表', 11, 'change_rolemenupermission'),
	(43, 'Can delete 角色菜单权限表', 11, 'delete_rolemenupermission'),
	(44, 'Can view 角色菜单权限表', 11, 'view_rolemenupermission'),
	(45, 'Can add 角色接口权限表', 12, 'add_rolemenubuttonpermission'),
	(46, 'Can change 角色接口权限表', 12, 'change_rolemenubuttonpermission'),
	(47, 'Can delete 角色接口权限表', 12, 'delete_rolemenubuttonpermission'),
	(48, 'Can view 角色接口权限表', 12, 'view_rolemenubuttonpermission'),
	(49, 'Can add 操作日志', 13, 'add_operationlog'),
	(50, 'Can change 操作日志', 13, 'change_operationlog'),
	(51, 'Can delete 操作日志', 13, 'delete_operationlog'),
	(52, 'Can view 操作日志', 13, 'view_operationlog'),
	(53, 'Can add 菜单字段表', 14, 'add_menufield'),
	(54, 'Can change 菜单字段表', 14, 'change_menufield'),
	(55, 'Can delete 菜单字段表', 14, 'delete_menufield'),
	(56, 'Can view 菜单字段表', 14, 'view_menufield'),
	(57, 'Can add 登录日志', 15, 'add_loginlog'),
	(58, 'Can change 登录日志', 15, 'change_loginlog'),
	(59, 'Can delete 登录日志', 15, 'delete_loginlog'),
	(60, 'Can view 登录日志', 15, 'view_loginlog'),
	(61, 'Can add 字段权限表', 16, 'add_fieldpermission'),
	(62, 'Can change 字段权限表', 16, 'change_fieldpermission'),
	(63, 'Can delete 字段权限表', 16, 'delete_fieldpermission'),
	(64, 'Can view 字段权限表', 16, 'view_fieldpermission'),
	(65, 'Can add 字典表', 17, 'add_dictionary'),
	(66, 'Can change 字典表', 17, 'change_dictionary'),
	(67, 'Can delete 字典表', 17, 'delete_dictionary'),
	(68, 'Can view 字典表', 17, 'view_dictionary'),
	(69, 'Can add 权限标识表', 18, 'add_button'),
	(70, 'Can change 权限标识表', 18, 'change_button'),
	(71, 'Can delete 权限标识表', 18, 'delete_button'),
	(72, 'Can view 权限标识表', 18, 'view_button'),
	(73, 'Can add 消息通知', 19, 'add_notification'),
	(74, 'Can change 消息通知', 19, 'change_notification'),
	(75, 'Can delete 消息通知', 19, 'delete_notification'),
	(76, 'Can view 消息通知', 19, 'view_notification'),
	(77, 'Can add 消息用户', 20, 'add_notificationusers'),
	(78, 'Can change 消息用户', 20, 'change_notificationusers'),
	(79, 'Can delete 消息用户', 20, 'delete_notificationusers'),
	(80, 'Can view 消息用户', 20, 'view_notificationusers'),
	(81, 'Can add 系统配置表', 21, 'add_systemconfig'),
	(82, 'Can change 系统配置表', 21, 'change_systemconfig'),
	(83, 'Can delete 系统配置表', 21, 'delete_systemconfig'),
	(84, 'Can view 系统配置表', 21, 'view_systemconfig');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.captcha_captchastore 结构
CREATE TABLE IF NOT EXISTS `captcha_captchastore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=InnoDB AUTO_INCREMENT=282 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.captcha_captchastore 的数据：~19 rows (大约)
DELETE FROM `captcha_captchastore`;
/*!40000 ALTER TABLE `captcha_captchastore` DISABLE KEYS */;
INSERT INTO `captcha_captchastore` (`id`, `challenge`, `response`, `hashkey`, `expiration`) VALUES
	(262, '5+7=', '12', '3f8db8448aa4dc6e0b66dcf4dd0676677954c57a', '2025-07-10 15:35:32.256412'),
	(263, '9-4=', '5', '9bf6ccf14db4e21d468aaf1c0576ab10affc1218', '2025-07-10 15:35:34.461158'),
	(264, '5+3=', '8', 'ca45c927222db2bbf48f590e28d82bf645276b86', '2025-07-10 15:35:40.269021'),
	(265, '4*7=', '28', '067ce6c1481a0a1b6a32838441ca19bb9c0a362e', '2025-07-10 15:37:54.653826'),
	(266, '1*1=', '1', 'd70e5d5d26363d7138beb1cc396f61d1db0c5307', '2025-07-10 15:41:20.872218'),
	(267, '3-1=', '2', '893c2109d8ff2dc80ee85a3e8e55cf0a0eede887', '2025-07-10 16:01:18.034790'),
	(268, '9-7=', '2', '9545da077de35cb14167c143aa97522fffa921df', '2025-07-10 16:01:30.855181'),
	(269, '8+7=', '15', '570fb751386521dbe4797bbf612efa896925531e', '2025-07-10 16:03:29.224331'),
	(270, '8+2=', '10', '44f4319bdafd5cab33cfb8d211ad9fc131e3f966', '2025-07-10 16:04:28.092636'),
	(271, '5+9=', '14', '63145df59828db4ee9ca759cc2295a68321ac2c8', '2025-07-10 16:05:42.665587'),
	(272, '4*6=', '24', '37e12db15e614eacef97188f91ff0f824505f036', '2025-07-10 16:05:48.070884'),
	(273, '2-1=', '1', 'ca1f313e7d982129ad63683967a50ef37108c0b4', '2025-07-10 16:09:04.245872'),
	(274, '7*8=', '56', '22c0064e9191026ea2e33cea9c4a9865abe70163', '2025-07-10 16:09:06.410196'),
	(275, '6*5=', '30', 'afa4fbe2681d03c1d160f2b18c9731d83aa8ecd7', '2025-07-10 16:09:18.776511'),
	(276, '7*1=', '7', '3514e9bae290fb4d27dbc95e737e87d027a94df0', '2025-07-10 16:09:28.597445'),
	(277, '10*5=', '50', '12bb78ddb2107d001f6dcd711e83201c09a074bf', '2025-07-10 16:10:56.233024'),
	(279, '8+7=', '15', '1b49bea4ea41173c303a41f0b86bef1b65546faa', '2025-07-13 15:47:22.755477'),
	(280, '3*1=', '3', '05b56eaffb4345842d235f56607d35b9b5d3350e', '2025-07-13 15:47:24.838903');
/*!40000 ALTER TABLE `captcha_captchastore` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.django_content_type 结构
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.django_content_type 的数据：~18 rows (大约)
DELETE FROM `django_content_type`;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(2, 'auth', 'group'),
	(1, 'auth', 'permission'),
	(5, 'captcha', 'captchastore'),
	(3, 'contenttypes', 'contenttype'),
	(18, 'mysystem', 'button'),
	(7, 'mysystem', 'dept'),
	(17, 'mysystem', 'dictionary'),
	(16, 'mysystem', 'fieldpermission'),
	(15, 'mysystem', 'loginlog'),
	(8, 'mysystem', 'menu'),
	(9, 'mysystem', 'menubutton'),
	(14, 'mysystem', 'menufield'),
	(19, 'mysystem', 'notification'),
	(20, 'mysystem', 'notificationusers'),
	(13, 'mysystem', 'operationlog'),
	(10, 'mysystem', 'role'),
	(12, 'mysystem', 'rolemenubuttonpermission'),
	(11, 'mysystem', 'rolemenupermission'),
	(21, 'mysystem', 'systemconfig'),
	(6, 'mysystem', 'users'),
	(4, 'sessions', 'session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.django_migrations 结构
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.django_migrations 的数据：~27 rows (大约)
DELETE FROM `django_migrations`;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-05-24 19:32:18.482847'),
	(2, 'contenttypes', '0002_remove_content_type_name', '2025-05-24 19:32:18.598735'),
	(3, 'auth', '0001_initial', '2025-05-24 19:32:18.975461'),
	(4, 'auth', '0002_alter_permission_name_max_length', '2025-05-24 19:32:19.057249'),
	(5, 'auth', '0003_alter_user_email_max_length', '2025-05-24 19:32:19.064723'),
	(6, 'auth', '0004_alter_user_username_opts', '2025-05-24 19:32:19.072504'),
	(7, 'auth', '0005_alter_user_last_login_null', '2025-05-24 19:32:19.081389'),
	(8, 'auth', '0006_require_contenttypes_0002', '2025-05-24 19:32:19.086228'),
	(9, 'auth', '0007_alter_validators_add_error_messages', '2025-05-24 19:32:19.093224'),
	(10, 'auth', '0008_alter_user_username_max_length', '2025-05-24 19:32:19.101303'),
	(11, 'auth', '0009_alter_user_last_name_max_length', '2025-05-24 19:32:19.109369'),
	(12, 'auth', '0010_alter_group_name_max_length', '2025-05-24 19:32:19.126268'),
	(13, 'auth', '0011_update_proxy_permissions', '2025-05-24 19:32:19.134279'),
	(14, 'auth', '0012_alter_user_first_name_max_length', '2025-05-24 19:32:19.142465'),
	(15, 'captcha', '0001_initial', '2025-05-24 19:32:19.184561'),
	(16, 'captcha', '0002_alter_captchastore_id', '2025-05-24 19:32:19.191878'),
	(17, 'mysystem', '0001_initial', '2025-05-24 19:32:20.460787'),
	(18, 'sessions', '0001_initial', '2025-05-24 19:32:20.522068');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.django_session 结构
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.django_session 的数据：~0 rows (大约)
DELETE FROM `django_session`;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_button 结构
CREATE TABLE IF NOT EXISTS `lyadmin_button` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `value` varchar(64) NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_button_creator_id_8ed6f8c5` (`creator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_button 的数据：~13 rows (大约)
DELETE FROM `lyadmin_button`;
/*!40000 ALTER TABLE `lyadmin_button` DISABLE KEYS */;
INSERT INTO `lyadmin_button` (`id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `name`, `value`, `status`, `creator_id`) VALUES
	('0894442986f249d7949e16a66a2d711b', '0', '', '2025-05-29 15:47:38.496815', '2025-05-29 15:47:38.496815', '查询', 'Search', 1, '0'),
	('222efe9759fa4263a4f7cf468d65a920', '0', '', '2025-06-30 11:39:52.306384', '2025-06-30 11:39:52.306384', '重置密码', 'ResetPass', 1, '0'),
	('26afd041337f430c8297c99407069e1a', '0', '', '2025-05-29 15:45:34.986847', '2025-05-29 15:45:34.986847', '删除', 'Delete', 1, '0'),
	('343578b3c9844ab5b1c6c4fda7fb6d16', '0', '', '2025-05-29 15:45:04.689791', '2025-05-29 15:45:04.689791', '编辑', 'Update', 1, '0'),
	('34714a2169234400b853bab042e5e789', '0', '', '2025-05-29 15:53:11.540581', '2025-05-29 15:47:01.386148', '保存', 'Save', 1, '0'),
	('442960094fcb4237a4fd76ba2794e10f', '0', '', '2025-06-21 16:50:09.825019', '2025-06-21 16:50:09.825019', '导出', 'Export', 1, '0'),
	('651fb535871c47bcb9a90b4efaa0487b', '0', '', '2025-06-24 13:01:00.142920', '2025-06-24 13:01:00.142920', '设置状态', 'SetStatus', 1, '0'),
	('68807789fdc0450cbeaba8b2391bbead', '0', '', '2025-06-20 11:19:36.570284', '2025-06-20 11:19:36.570284', '移动', 'Move', 1, '0'),
	('8e6fe9387f4e4c2f8c85f646c83ce1d8', '0', '', '2025-05-29 15:44:07.829029', '2025-05-29 15:44:07.829029', '新增', 'Create', 1, '0'),
	('9954de2be3bf47aba4188948fc2f7b93', '0', '', '2025-05-29 15:46:54.214165', '2025-05-29 15:46:54.214165', '详情', 'Detail', 1, '0'),
	('f5629f25662f4ba69efb2fe9c1e798b4', '0', '', '2025-06-24 13:59:05.893474', '2025-06-24 13:59:05.893474', '导入', 'Import', 1, '0');
/*!40000 ALTER TABLE `lyadmin_button` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_dept 结构
CREATE TABLE IF NOT EXISTS `lyadmin_dept` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `key` varchar(64) DEFAULT NULL,
  `sort` int(11) NOT NULL,
  `owner` varchar(32) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  `parent_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `lyadmin_dept_creator_id_bb4dafb6` (`creator_id`),
  KEY `lyadmin_dept_parent_id_c856ab90` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_dept 的数据：~3 rows (大约)
DELETE FROM `lyadmin_dept`;
/*!40000 ALTER TABLE `lyadmin_dept` DISABLE KEYS */;
INSERT INTO `lyadmin_dept` (`id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `name`, `key`, `sort`, `owner`, `phone`, `email`, `status`, `creator_id`, `parent_id`) VALUES
	('5e5af490ab0146d09045e6ece736c05f', '0', '', '2025-06-26 09:11:18.425996', '2025-06-17 19:37:03.272479', '财务部门', 'caiwu', 3, '', '', '', 1, '0', '8b304f92647747aabffc7e8750397762'),
	('877641076a3b4a93b2e58e02246dbf3e', '0', '', '2025-06-26 09:11:12.854369', '2025-06-17 19:36:48.642174', '研发部门', 'yanfa', 2, '', '', '', 1, '0', '8b304f92647747aabffc7e8750397762'),
	('8b304f92647747aabffc7e8750397762', '0', '', '2025-06-26 09:11:06.063069', '2025-06-17 19:04:41.821618', 'lyadmin团队', 'lyadmin', 1, '', '', '', 1, '0', NULL);
/*!40000 ALTER TABLE `lyadmin_dept` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_dictionary 结构
CREATE TABLE IF NOT EXISTS `lyadmin_dictionary` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `sort` int(11) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  `parent_id` varchar(100) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `value` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_dictionary_creator_id_f75d1c0b` (`creator_id`),
  KEY `lyadmin_dictionary_parent_id_9d47f813` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_dictionary 的数据：~10 rows (大约)
DELETE FROM `lyadmin_dictionary`;
/*!40000 ALTER TABLE `lyadmin_dictionary` DISABLE KEYS */;
INSERT INTO `lyadmin_dictionary` (`id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `status`, `sort`, `remark`, `creator_id`, `parent_id`, `label`, `value`) VALUES
	('1b999b8fd390470bb39e57b134f841f5', '0', '', '2025-07-06 15:57:09.624650', '2025-07-06 15:57:09.624650', 1, 1, '', '0', '526c712ec30e45a2a1b45174e98420a3', '是', 'true'),
	('23724e0d5c14458e839efc01449ee1b0', '0', '', '2025-07-06 15:55:36.676853', '2025-07-06 15:49:48.870448', 1, 2, '', '0', '526c712ec30e45a2a1b45174e98420a3', '否', 'false'),
	('526c712ec30e45a2a1b45174e98420a3', '0', '', '2025-07-06 11:24:11.314659', '2025-07-06 11:24:11.314659', 1, 29, '', '0', NULL, '是/否-布尔值', 'button_bool'),
	('53623bd2de60426281fd490ef65be9ca', '0', '', '2025-07-06 15:49:34.607270', '2025-07-06 15:49:34.607270', 1, 2, '', '0', 'e19dbebf1e3a49688e62cbc3f42486bc', '女', '1'),
	('6d12f0aa25e14ccbb806b148f215a370', '0', '', '2025-07-06 11:23:20.046712', '2025-07-06 11:16:17.776532', 1, 30, '', '0', NULL, '是/否-数字值', 'button_number'),
	('85e5a570019742c58dc0a31f95aca8c0', '0', '', '2025-07-06 15:31:50.708311', '2025-07-06 15:31:50.708311', 1, 1, '', '0', 'e19dbebf1e3a49688e62cbc3f42486bc', '未知', '0'),
	('97ddad1d630647f3b95616453dd55958', '0', '', '2025-07-06 15:56:01.522537', '2025-07-06 15:56:01.522537', 1, 3, '', '0', 'e19dbebf1e3a49688e62cbc3f42486bc', '男', '2'),
	('a0b67efa43c54b8eabf5042988a887c4', '0', '', '2025-07-06 16:07:26.005560', '2025-07-06 16:07:26.005560', 1, 2, '', '0', '6d12f0aa25e14ccbb806b148f215a370', '否', '0'),
	('ceb419b24926454681c9040389deda5d', '0', '', '2025-07-06 15:57:49.465532', '2025-07-06 15:57:49.465532', 1, 1, '', '0', '6d12f0aa25e14ccbb806b148f215a370', '是', '1'),
	('e19dbebf1e3a49688e62cbc3f42486bc', '0', '', '2025-07-06 11:05:41.542808', '2025-07-06 11:05:41.542808', 1, 1, '', '0', NULL, '性别', 'gender');
/*!40000 ALTER TABLE `lyadmin_dictionary` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_field_permission 结构
CREATE TABLE IF NOT EXISTS `lyadmin_field_permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `can_view` tinyint(1) NOT NULL,
  `can_create` tinyint(1) NOT NULL,
  `can_update` tinyint(1) NOT NULL,
  `field_id` bigint(20) NOT NULL,
  `role_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_field_permission_field_id_d5a3eac4` (`field_id`),
  KEY `lyadmin_field_permission_role_id_90bd14cf` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=259 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_field_permission 的数据：~0 rows (大约)
DELETE FROM `lyadmin_field_permission`;
/*!40000 ALTER TABLE `lyadmin_field_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `lyadmin_field_permission` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_login_log 结构
CREATE TABLE IF NOT EXISTS `lyadmin_login_log` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `ip` varchar(32) DEFAULT NULL,
  `agent` varchar(1500) DEFAULT NULL,
  `browser` varchar(200) DEFAULT NULL,
  `os` varchar(150) DEFAULT NULL,
  `login_type` int(11) NOT NULL,
  `ip_area` varchar(100) DEFAULT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  `msg` varchar(255) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_login_log_creator_id_2aae8b60` (`creator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_login_log 的数据：~0 rows (大约)
DELETE FROM `lyadmin_login_log`;
/*!40000 ALTER TABLE `lyadmin_login_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `lyadmin_login_log` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_menu 结构
CREATE TABLE IF NOT EXISTS `lyadmin_menu` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `icon` varchar(64) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `sort` int(11) DEFAULT NULL,
  `type` smallint(6) NOT NULL,
  `link_url` varchar(255) DEFAULT NULL,
  `web_path` varchar(128) DEFAULT NULL,
  `component` varchar(128) DEFAULT NULL,
  `component_name` varchar(50) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `isautopm` tinyint(1) DEFAULT NULL,
  `cache` tinyint(1) DEFAULT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  `parent_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_menu_creator_id_39b95522` (`creator_id`),
  KEY `lyadmin_menu_parent_id_4a6f3129` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_menu 的数据：~18 rows (大约)
DELETE FROM `lyadmin_menu`;
/*!40000 ALTER TABLE `lyadmin_menu` DISABLE KEYS */;
INSERT INTO `lyadmin_menu` (`id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `icon`, `name`, `sort`, `type`, `link_url`, `web_path`, `component`, `component_name`, `status`, `isautopm`, `cache`, `visible`, `creator_id`, `parent_id`) VALUES
	('01599f73f61848aa811f687b1cfc1588', '0', '', '2025-07-06 10:27:49.284326', '2025-07-06 10:27:49.284326', 'Football', '功能演示', 60, 0, '', '/functionsDemosDirs', '', '', 1, 0, 0, 1, '0', NULL),
	('150e0957200146b3bd0226c45e8031f7', '0', '', '2025-06-19 23:38:50.658405', '2025-05-27 19:23:03.104927', 'Link', 'iframe嵌套', 61, 2, 'https://doc.lybbn.cn', '/docdvlyadmin', '', '', 1, 0, 0, 1, '0', '01599f73f61848aa811f687b1cfc1588'),
	('1b5018bdb5e04698b84da505e8a6b93c', '0', '', '2025-06-20 10:41:09.509479', '2025-06-20 10:41:09.509479', 'TrophyBase', '角色管理', 100, 1, '', '/roleManage', '', 'roleManage', 1, 0, 0, 1, '0', 'af862854dc44410d84b8b2ae5c16c90d'),
	('205910763e0e42fbbc12833d2f7d61bb', '0', '', '2025-07-06 10:25:52.268867', '2025-07-06 10:25:52.268867', 'Reading', '字典管理', 30, 1, '', '/sysDictionary', '', 'sysDictionary', 1, 0, 0, 1, '0', '563092a536194a1493551a0043f1f1a3'),
	('24d2eb79a21141afbe73058cc02545e0', '0', '', '2025-07-03 17:50:53.774912', '2025-07-03 17:50:53.774912', 'ChatLineSquare', '操作日志', 200, 1, '', '/journalManage', '', 'journalManage', 1, 0, 0, 1, '0', 'af862854dc44410d84b8b2ae5c16c90d'),
	('2e9937b37ac94e248e9ed159bfe7b655', '0', '', '2025-05-30 11:59:11.410779', '2025-05-27 16:51:27.224927', 'Collection', '菜单管理', 90, 1, '', '/menuManage', '', 'menuManage', 1, 0, 0, 1, '0', 'af862854dc44410d84b8b2ae5c16c90d'),
	('31552696153b42599ce1faf6fe495824', '0', '', '2025-06-28 22:39:05.420221', '2025-06-28 22:37:29.608094', 'User', '用户管理', 40, 1, '', '/buserManage', '', 'buserManage', 1, 0, 0, 1, '0', 'af862854dc44410d84b8b2ae5c16c90d'),
	('44662b7fe6b54395994f28ed88eaf3f0', '0', '', '2025-07-12 22:54:52.529651', '2025-07-12 22:51:19.303097', 'Message', '我的消息', 30, 1, '', '/myMessage', '', 'myMessage', 1, 0, 0, 1, '0', NULL),
	('4a7a7748387f44dbab72027d8bdc87f7', '0', '', '2025-06-19 22:36:22.877877', '2025-05-27 16:48:37.075299', 'House', '首页', 10, 1, '', '/home', '', 'home', 1, 0, 0, 1, '0', NULL),
	('4f947108c5bf44f2b97e4a80daebf772', '0', '', '2025-07-11 15:23:13.273011', '2025-07-11 15:23:13.273011', 'ChatDotRound', '通知公告', 20, 1, '', '/messagNotice', '', 'messagNotice', 1, 0, 0, 1, '0', '563092a536194a1493551a0043f1f1a3'),
	('563092a536194a1493551a0043f1f1a3', '0', '', '2025-07-06 10:28:00.572624', '2025-07-06 10:24:28.612173', 'Operation', '系统工具', 80, 0, '', '/systemToolsMgDirs', '', '', 1, 0, 0, 1, '0', NULL),
	('6354ba32ae734b5eaa799a65f76deee6', '0', '', '2025-07-07 22:53:48.969388', '2025-07-07 22:53:36.719556', 'Setting', '系统设置', 27, 1, '', '/systemConfig', '', 'systemConfig', 1, 0, 0, 1, '0', '563092a536194a1493551a0043f1f1a3'),
	('8faec98030e443b99ce0d4c636163db7', '0', '', '2025-06-26 10:04:29.302735', '2025-06-26 10:04:29.302735', 'Guide', '权限管理', 120, 1, '', '/authorityManage', '', 'authorityManage', 1, 0, 0, 1, '0', 'af862854dc44410d84b8b2ae5c16c90d'),
	('95227fe101e747908c12b56d2bae5e8e', '0', '', '2025-06-24 17:34:34.764656', '2025-05-30 11:59:59.799346', 'OfficeBuilding', '部门管理', 50, 1, '', '/deptManage', '', 'deptManage', 1, 0, 0, 1, '0', 'af862854dc44410d84b8b2ae5c16c90d'),
	('98870fbaffb348ab9fd16a88e946bf09', '0', '', '2025-06-19 22:11:43.622822', '2025-05-27 16:50:26.693349', 'User', '个人中心', 19, 1, '', '/PersonalCenter', '', 'PersonalCenter', 1, 0, 0, 1, '0', NULL),
	('9ece0330c65e40df8da00190107d908e', '0', '', '2025-06-19 23:39:35.291735', '2025-06-19 23:39:35.292565', 'Link', '外链测试', 60, 3, 'https://doc.lybbn.cn', '/docdvlyadminlink', '', '', 1, 0, 0, 1, '0', '01599f73f61848aa811f687b1cfc1588'),
	('a8b435647f0b4a3f852ec796433e8919', '0', '', '2025-07-06 16:23:15.637839', '2025-07-06 16:23:15.637839', 'AddLocation', '登录日志', 230, 1, '', '/loginLogs', '', 'loginLogs', 1, 0, 0, 1, '0', 'af862854dc44410d84b8b2ae5c16c90d'),
	('af862854dc44410d84b8b2ae5c16c90d', '0', '', '2025-07-06 10:28:11.422074', '2025-05-27 16:52:51.726054', 'Setting', '系统管理', 90, 0, '', '/dirsettingsDirs', '', '', 1, 0, 0, 1, '0', NULL);
/*!40000 ALTER TABLE `lyadmin_menu` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_menu_button 结构
CREATE TABLE IF NOT EXISTS `lyadmin_menu_button` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `value` varchar(64) NOT NULL,
  `api` varchar(64) NOT NULL,
  `method` smallint(6) DEFAULT NULL,
  `menu_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_menu_button_menu_id_74205633` (`menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_menu_button 的数据：~73 rows (大约)
DELETE FROM `lyadmin_menu_button`;
/*!40000 ALTER TABLE `lyadmin_menu_button` DISABLE KEYS */;
INSERT INTO `lyadmin_menu_button` (`id`, `name`, `value`, `api`, `method`, `menu_id`) VALUES
	(1, '查询', 'menuManage:Search', '/api/system/menu/', 0, '2e9937b37ac94e248e9ed159bfe7b655'),
	(2, '新增', 'deptManage:Create', '/api/system/dept/', 1, '95227fe101e747908c12b56d2bae5e8e'),
	(3, '删除', 'deptManage:Delete', '/api/system/dept/{id}/', 3, '95227fe101e747908c12b56d2bae5e8e'),
	(4, '编辑', 'deptManage:Update', '/api/system/dept/{id}/', 2, '95227fe101e747908c12b56d2bae5e8e'),
	(5, '查询', 'deptManage:Search', '/api/system/dept/', 0, '95227fe101e747908c12b56d2bae5e8e'),
	(7, '新增', 'roleManage:Create', '/api/system/role/', 1, '1b5018bdb5e04698b84da505e8a6b93c'),
	(8, '删除', 'roleManage:Delete', '/api/system/role/{id}/', 3, '1b5018bdb5e04698b84da505e8a6b93c'),
	(9, '编辑', 'roleManage:Update', '/api/system/role/{id}/', 2, '1b5018bdb5e04698b84da505e8a6b93c'),
	(10, '查询', 'roleManage:Search', '/api/system/role/', 0, '1b5018bdb5e04698b84da505e8a6b93c'),
	(12, '删除', 'menuManage:Delete', '/api/system/menu/{id}/', 3, '2e9937b37ac94e248e9ed159bfe7b655'),
	(13, '新增', 'menuManage:Create', '/api/system/menu/', 1, '2e9937b37ac94e248e9ed159bfe7b655'),
	(14, '编辑', 'menuManage:Update', '/api/system/menu/{id}/', 2, '2e9937b37ac94e248e9ed159bfe7b655'),
	(15, '移动', 'menuManage:Move', '/api/system/menu/update_sort/', 1, '2e9937b37ac94e248e9ed159bfe7b655'),
	(16, '导出', 'deptManage:Export', '/api/system/dept/export_data/', 1, '95227fe101e747908c12b56d2bae5e8e'),
	(17, '设置状态', 'deptManage:SetStatus', '/api/system/dept/set_status/', 1, '95227fe101e747908c12b56d2bae5e8e'),
	(18, '导入', 'deptManage:Import', '/api/system/dept/import_data/', 1, '95227fe101e747908c12b56d2bae5e8e'),
	(19, '设置状态', 'roleManage:SetStatus', '/api/system/role/set_status/', 1, '1b5018bdb5e04698b84da505e8a6b93c'),
	(20, '查询', 'authorityManage:Search', '/api/system/role_permission/', 0, '8faec98030e443b99ce0d4c636163db7'),
	(21, '保存', 'authorityManage:Save', '/api/system/role_permission/save_permission/', 1, '8faec98030e443b99ce0d4c636163db7'),
	(22, '新增', 'buserManage:Create', '/api/system/user/', 1, '31552696153b42599ce1faf6fe495824'),
	(23, '删除', 'buserManage:Delete', '/api/system/user/{id}/', 3, '31552696153b42599ce1faf6fe495824'),
	(24, '编辑', 'buserManage:Update', '/api/system/user/{id}/', 2, '31552696153b42599ce1faf6fe495824'),
	(25, '查询', 'buserManage:Search', '/api/system/user/', 0, '31552696153b42599ce1faf6fe495824'),
	(27, '导出', 'buserManage:Export', '/api/system/user/export_data/', 1, '31552696153b42599ce1faf6fe495824'),
	(28, '导入', 'buserManage:Import', '/api/system/user/import_data/', 1, '31552696153b42599ce1faf6fe495824'),
	(29, '设置状态', 'buserManage:SetStatus', '/api/system/user/set_status/', 1, '31552696153b42599ce1faf6fe495824'),
	(30, '重置密码', 'buserManage:ResetPass', '/api/system/user/reset_password/', 2, '31552696153b42599ce1faf6fe495824'),
	(31, '按钮查看', 'menuManage:ButtonSearch', '/api/system/button/', 0, '2e9937b37ac94e248e9ed159bfe7b655'),
	(32, '按钮增', 'menuManage:ButtonCreate', '/api/system/button/', 1, '2e9937b37ac94e248e9ed159bfe7b655'),
	(33, '按钮改', 'menuManage:ButtonUpdate', '/api/system/button/{id}/', 2, '2e9937b37ac94e248e9ed159bfe7b655'),
	(34, '按钮删', 'menuManage:ButtonDelete', '/api/system/button/{id}/', 3, '2e9937b37ac94e248e9ed159bfe7b655'),
	(35, '按钮权查', 'menuManage:MenuButtonSearch', '/api/system/menu_button/', 0, '2e9937b37ac94e248e9ed159bfe7b655'),
	(36, '按钮权增', 'menuManage:MenuButtonCreate', '/api/system/menu_button/', 1, '2e9937b37ac94e248e9ed159bfe7b655'),
	(37, '按钮权改', 'menuManage:MenuButtonUpdate', '/api/system/menu_button/{id}/', 2, '2e9937b37ac94e248e9ed159bfe7b655'),
	(38, '按钮权删', 'menuManage:MenuButtonDelete', '/api/system/menu_button/{id}/', 3, '2e9937b37ac94e248e9ed159bfe7b655'),
	(39, '列权查看', 'menuManage:MenuFieldSearch', '/api/system/menu_field/', 0, '2e9937b37ac94e248e9ed159bfe7b655'),
	(40, '列权新增', 'menuManage:MenuFieldCreate', '/api/system/menu_field/', 1, '2e9937b37ac94e248e9ed159bfe7b655'),
	(41, '列权编辑', 'menuManage:MenuFieldUpdate', '/api/system/menu_field/{id}/', 2, '2e9937b37ac94e248e9ed159bfe7b655'),
	(42, '列权删除', 'menuManage:MenuFieldDelete', '/api/system/menu_field/{id}/', 3, '2e9937b37ac94e248e9ed159bfe7b655'),
	(43, '列权批量', 'menuManage:MenuFieldPL', '/api/system/menu_field/auto_create/', 1, '2e9937b37ac94e248e9ed159bfe7b655'),
	(44, '按钮权批', 'menuManage:MenuButtonPL', '/api/system/menu_button/auto_create/', 1, '2e9937b37ac94e248e9ed159bfe7b655'),
	(45, '菜单', 'authorityManage:MenuSearch', '/api/system/role_id_to_menu/{id}/', 0, '8faec98030e443b99ce0d4c636163db7'),
	(47, '查询', 'PersonalCenter:Search', '/api/system/user/user_info/', 0, '98870fbaffb348ab9fd16a88e946bf09'),
	(48, '重置密码', 'PersonalCenter:ResetPass', '/api/system/user/change_password/', 1, '98870fbaffb348ab9fd16a88e946bf09'),
	(49, '编辑', 'PersonalCenter:Update', '/api/system/user/user_info/', 2, '98870fbaffb348ab9fd16a88e946bf09'),
	(50, '修改头像', 'PersonalCenter:UpdateAvatar', '/api/system/user/change_avatar/', 1, '98870fbaffb348ab9fd16a88e946bf09'),
	(51, '查询', 'journalManage:Search', '/api/system/operation_log/', 0, '24d2eb79a21141afbe73058cc02545e0'),
	(52, '删除', 'journalManage:Delete', '/api/system/operation_log/{id}/', 3, '24d2eb79a21141afbe73058cc02545e0'),
	(53, '全部清除', 'journalManage:DeleteAll', '/api/system/operation_log/deletealllogs/', 3, '24d2eb79a21141afbe73058cc02545e0'),
	(54, '日志查询', 'PersonalCenter:GetOPLog', '/api/system/operation_log/getOwnerLogs/', 0, '98870fbaffb348ab9fd16a88e946bf09'),
	(55, '查询', 'sysDictionary:Search', '/api/system/dictionary/', 0, '205910763e0e42fbbc12833d2f7d61bb'),
	(56, '新增', 'sysDictionary:Create', '/api/system/dictionary/', 1, '205910763e0e42fbbc12833d2f7d61bb'),
	(57, '删除', 'sysDictionary:Delete', '/api/system/dictionary/{id}/', 3, '205910763e0e42fbbc12833d2f7d61bb'),
	(58, '编辑', 'sysDictionary:Update', '/api/system/dictionary/{id}/', 2, '205910763e0e42fbbc12833d2f7d61bb'),
	(59, '设置状态', 'sysDictionary:SetStatus', '/api/system/dictionary/set_status/', 1, '205910763e0e42fbbc12833d2f7d61bb'),
	(60, '查询', 'loginLogs:Search', '/api/system/login_log/', 0, 'a8b435647f0b4a3f852ec796433e8919'),
	(61, '删除', 'loginLogs:Delete', '/api/system/login_log/{id}/', 3, 'a8b435647f0b4a3f852ec796433e8919'),
	(62, '全部清除', 'loginLogs:DeleteAll', '/api/system/login_log/deletealllogs/', 3, 'a8b435647f0b4a3f852ec796433e8919'),
	(63, '登录日志', 'PersonalCenter:GetLoginLog', '/api/system/login_log/getOwnerLogs/', 0, '98870fbaffb348ab9fd16a88e946bf09'),
	(64, '新增分组', 'systemConfig:CreateGroup', '/api/system/sysconfig/', 1, '6354ba32ae734b5eaa799a65f76deee6'),
	(65, '新增项', 'systemConfig:CreateContent', '/api/system/sysconfig/', 1, '6354ba32ae734b5eaa799a65f76deee6'),
	(66, '保存', 'systemConfig:Save', '/api/system/sysconfig/{id}/', 2, '6354ba32ae734b5eaa799a65f76deee6'),
	(67, '查询', 'systemConfig:Search', '/api/system/sysconfig/', 0, '6354ba32ae734b5eaa799a65f76deee6'),
	(68, '删除', 'systemConfig:Delete', '/api/system/sysconfig/{id}/', 3, '6354ba32ae734b5eaa799a65f76deee6'),
	(69, '编辑', 'systemConfig:Update', '/api/system/sysconfig/{id}/', 2, '6354ba32ae734b5eaa799a65f76deee6'),
	(70, '查询', 'messagNotice:Search', '/api/system/msg/', 0, '4f947108c5bf44f2b97e4a80daebf772'),
	(71, '新增', 'messagNotice:Create', '/api/system/msg/', 1, '4f947108c5bf44f2b97e4a80daebf772'),
	(72, '删除', 'messagNotice:Delete', '/api/system/msg/{id}/', 3, '4f947108c5bf44f2b97e4a80daebf772'),
	(73, '消息查询', 'PersonalCenter:PMsg', '/api/system/msg/ownmsg/', 0, '98870fbaffb348ab9fd16a88e946bf09'),
	(74, '编辑', 'messagNotice:Update', '/api/system/msg/{id}/', 2, '4f947108c5bf44f2b97e4a80daebf772'),
	(75, '查询', 'myMessage:Search', '/api/system/msg/ownmsg/', 0, '44662b7fe6b54395994f28ed88eaf3f0'),
	(76, '删除', 'myMessage:Delete', '/api/system/msg/delownmsg/', 1, '44662b7fe6b54395994f28ed88eaf3f0'),
	(77, '详情', 'myMessage:Detail', '/api/system/msg/readownmsg/', 1, '44662b7fe6b54395994f28ed88eaf3f0');
/*!40000 ALTER TABLE `lyadmin_menu_button` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_menu_field 结构
CREATE TABLE IF NOT EXISTS `lyadmin_menu_field` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `model` varchar(70) DEFAULT NULL,
  `field_name` varchar(64) NOT NULL,
  `title` varchar(64) NOT NULL,
  `menu_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_menu_field_menu_id_b6970622` (`menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_menu_field 的数据：~11 rows (大约)
DELETE FROM `lyadmin_menu_field`;
/*!40000 ALTER TABLE `lyadmin_menu_field` DISABLE KEYS */;
INSERT INTO `lyadmin_menu_field` (`id`, `model`, `field_name`, `title`, `menu_id`) VALUES
	(39, 'Role', 'id', 'Id', '1b5018bdb5e04698b84da505e8a6b93c'),
	(40, 'Role', 'creator', '创建人', '1b5018bdb5e04698b84da505e8a6b93c'),
	(41, 'Role', 'modifier', '修改人', '1b5018bdb5e04698b84da505e8a6b93c'),
	(42, 'Role', 'dept_belong', '数据归属部门', '1b5018bdb5e04698b84da505e8a6b93c'),
	(43, 'Role', 'update_datetime', '修改时间', '1b5018bdb5e04698b84da505e8a6b93c'),
	(44, 'Role', 'create_datetime', '创建时间', '1b5018bdb5e04698b84da505e8a6b93c'),
	(45, 'Role', 'name', '角色名称', '1b5018bdb5e04698b84da505e8a6b93c'),
	(46, 'Role', 'key', '权限字符', '1b5018bdb5e04698b84da505e8a6b93c'),
	(47, 'Role', 'sort', '角色顺序', '1b5018bdb5e04698b84da505e8a6b93c'),
	(48, 'Role', 'status', '角色状态', '1b5018bdb5e04698b84da505e8a6b93c'),
	(49, 'Role', 'remark', '备注', '1b5018bdb5e04698b84da505e8a6b93c');
/*!40000 ALTER TABLE `lyadmin_menu_field` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_message 结构
CREATE TABLE IF NOT EXISTS `lyadmin_message` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `content` longtext NOT NULL,
  `target_type` smallint(6) NOT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  `tag_type` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_message_creator_id_6cfcc649` (`creator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_message 的数据：~1 rows (大约)
DELETE FROM `lyadmin_message`;
/*!40000 ALTER TABLE `lyadmin_message` DISABLE KEYS */;
INSERT INTO `lyadmin_message` (`id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `title`, `content`, `target_type`, `creator_id`, `tag_type`) VALUES
	('52c13c36bdda427ab72020fa8e0db443', '0', '', '2025-07-12 23:54:21.574644', '2025-07-12 23:10:58.198612', 'dvlyadmin-mini版本发布通知', '<p><span style="color: rgb(86, 156, 214); font-size: 14px;">dvlyadmin-mini</span><span style="color: rgb(0, 0, 0); font-size: 14px;">是专为追求页面极致效果的开发者设计的一套 </span><span style="color: rgb(86, 156, 214); font-size: 14px;">django-vue-lyadmin优化升级</span><span style="color: rgb(204, 204, 204); font-size: 14px;"> </span><span style="color: rgb(0, 0, 0); font-size: 14px;">的精简版。我们通过大量重构架构，去除了无用冗余代码，力求做到小而精。前端采用</span><span style="color: rgb(204, 204, 204); font-size: 14px;"> </span><span style="color: rgb(86, 156, 214); font-size: 14px;">**Vite + Vue 3 + Element Plus**</span><span style="color: rgb(0, 0, 0); font-size: 14px;">，支持适配手机端，助力快速开发项目及提升项目质量！</span></p>', 0, '0', 0);
/*!40000 ALTER TABLE `lyadmin_message` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_message_dept 结构
CREATE TABLE IF NOT EXISTS `lyadmin_message_dept` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `notification_id` varchar(100) NOT NULL,
  `dept_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lyadmin_message_dept_notification_id_dept_id_59f23e18_uniq` (`notification_id`,`dept_id`),
  KEY `lyadmin_message_dept_notification_id_47aff8cb` (`notification_id`),
  KEY `lyadmin_message_dept_dept_id_f48b2b4c` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_message_dept 的数据：~0 rows (大约)
DELETE FROM `lyadmin_message_dept`;
/*!40000 ALTER TABLE `lyadmin_message_dept` DISABLE KEYS */;
/*!40000 ALTER TABLE `lyadmin_message_dept` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_message_role 结构
CREATE TABLE IF NOT EXISTS `lyadmin_message_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `notification_id` varchar(100) NOT NULL,
  `role_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lyadmin_message_role_notification_id_role_id_64b84ba7_uniq` (`notification_id`,`role_id`),
  KEY `lyadmin_message_role_notification_id_1ce413dc` (`notification_id`),
  KEY `lyadmin_message_role_role_id_d3718496` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_message_role 的数据：~0 rows (大约)
DELETE FROM `lyadmin_message_role`;
/*!40000 ALTER TABLE `lyadmin_message_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `lyadmin_message_role` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_message_users 结构
CREATE TABLE IF NOT EXISTS `lyadmin_message_users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_read` tinyint(1) DEFAULT NULL,
  `read_at` datetime(6) DEFAULT NULL,
  `notification_id` varchar(100) NOT NULL,
  `user_id` varchar(100) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_message_users_notification_id_cb1d078c` (`notification_id`),
  KEY `lyadmin_message_users_user_id_90dc6f12` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_message_users 的数据：~2 rows (大约)
DELETE FROM `lyadmin_message_users`;
/*!40000 ALTER TABLE `lyadmin_message_users` DISABLE KEYS */;
INSERT INTO `lyadmin_message_users` (`id`, `is_read`, `read_at`, `notification_id`, `user_id`, `is_delete`) VALUES
	(11, 0, NULL, '52c13c36bdda427ab72020fa8e0db443', '1792aea416944eff9e3845aec6ac88b4', 0),
	(15, 1, '2025-07-13 15:23:52.467418', '52c13c36bdda427ab72020fa8e0db443', '0', 0);
/*!40000 ALTER TABLE `lyadmin_message_users` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_operation_log 结构
CREATE TABLE IF NOT EXISTS `lyadmin_operation_log` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `req_modular` varchar(64) DEFAULT NULL,
  `req_path` longtext,
  `req_body` longtext,
  `req_method` varchar(8) DEFAULT NULL,
  `req_msg` longtext,
  `req_ip` varchar(32) DEFAULT NULL,
  `req_browser` varchar(64) DEFAULT NULL,
  `resp_code` varchar(32) DEFAULT NULL,
  `req_os` varchar(64) DEFAULT NULL,
  `ip_area` varchar(100) DEFAULT NULL,
  `json_result` longtext,
  `status` tinyint(1) NOT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  `creator_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_operation_log_creator_id_7b08f4e1` (`creator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_operation_log 的数据：~0 rows (大约)
DELETE FROM `lyadmin_operation_log`;
/*!40000 ALTER TABLE `lyadmin_operation_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `lyadmin_operation_log` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_role 结构
CREATE TABLE IF NOT EXISTS `lyadmin_role` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `key` varchar(64) NOT NULL,
  `sort` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `key` (`key`),
  KEY `lyadmin_role_creator_id_858b8a61` (`creator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_role 的数据：~1 rows (大约)
DELETE FROM `lyadmin_role`;
/*!40000 ALTER TABLE `lyadmin_role` DISABLE KEYS */;
INSERT INTO `lyadmin_role` (`id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `name`, `key`, `sort`, `status`, `remark`, `creator_id`) VALUES
	('854f77a5df34497a9af1d16379821f2b', '0', '', '2025-06-26 09:22:32.580507', '2025-06-26 09:22:32.580507', '管理员', 'admin', 1, 1, NULL, '0');
/*!40000 ALTER TABLE `lyadmin_role` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_role_menubutton_permission 结构
CREATE TABLE IF NOT EXISTS `lyadmin_role_menubutton_permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `data_scope` smallint(6) NOT NULL,
  `menu_button_id` bigint(20) DEFAULT NULL,
  `role_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_role_menubutton_permission_menu_button_id_44f2d827` (`menu_button_id`),
  KEY `lyadmin_role_menubutton_permission_role_id_810062df` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1753 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_role_menubutton_permission 的数据：~73 rows (大约)
DELETE FROM `lyadmin_role_menubutton_permission`;
/*!40000 ALTER TABLE `lyadmin_role_menubutton_permission` DISABLE KEYS */;
INSERT INTO `lyadmin_role_menubutton_permission` (`id`, `data_scope`, `menu_button_id`, `role_id`) VALUES
	(1680, 5, 48, '854f77a5df34497a9af1d16379821f2b'),
	(1681, 5, 49, '854f77a5df34497a9af1d16379821f2b'),
	(1682, 5, 63, '854f77a5df34497a9af1d16379821f2b'),
	(1683, 5, 73, '854f77a5df34497a9af1d16379821f2b'),
	(1684, 5, 47, '854f77a5df34497a9af1d16379821f2b'),
	(1685, 5, 54, '854f77a5df34497a9af1d16379821f2b'),
	(1686, 5, 50, '854f77a5df34497a9af1d16379821f2b'),
	(1687, 5, 77, '854f77a5df34497a9af1d16379821f2b'),
	(1688, 5, 75, '854f77a5df34497a9af1d16379821f2b'),
	(1689, 5, 76, '854f77a5df34497a9af1d16379821f2b'),
	(1690, 5, 74, '854f77a5df34497a9af1d16379821f2b'),
	(1691, 5, 70, '854f77a5df34497a9af1d16379821f2b'),
	(1692, 5, 71, '854f77a5df34497a9af1d16379821f2b'),
	(1693, 5, 72, '854f77a5df34497a9af1d16379821f2b'),
	(1694, 5, 69, '854f77a5df34497a9af1d16379821f2b'),
	(1695, 5, 67, '854f77a5df34497a9af1d16379821f2b'),
	(1696, 5, 65, '854f77a5df34497a9af1d16379821f2b'),
	(1697, 5, 64, '854f77a5df34497a9af1d16379821f2b'),
	(1698, 5, 68, '854f77a5df34497a9af1d16379821f2b'),
	(1699, 5, 66, '854f77a5df34497a9af1d16379821f2b'),
	(1700, 5, 59, '854f77a5df34497a9af1d16379821f2b'),
	(1701, 5, 58, '854f77a5df34497a9af1d16379821f2b'),
	(1702, 5, 55, '854f77a5df34497a9af1d16379821f2b'),
	(1703, 5, 56, '854f77a5df34497a9af1d16379821f2b'),
	(1704, 5, 57, '854f77a5df34497a9af1d16379821f2b'),
	(1705, 5, 30, '854f77a5df34497a9af1d16379821f2b'),
	(1706, 5, 29, '854f77a5df34497a9af1d16379821f2b'),
	(1707, 5, 24, '854f77a5df34497a9af1d16379821f2b'),
	(1708, 5, 25, '854f77a5df34497a9af1d16379821f2b'),
	(1709, 5, 22, '854f77a5df34497a9af1d16379821f2b'),
	(1710, 5, 27, '854f77a5df34497a9af1d16379821f2b'),
	(1711, 5, 28, '854f77a5df34497a9af1d16379821f2b'),
	(1712, 5, 23, '854f77a5df34497a9af1d16379821f2b'),
	(1713, 5, 17, '854f77a5df34497a9af1d16379821f2b'),
	(1714, 5, 4, '854f77a5df34497a9af1d16379821f2b'),
	(1715, 5, 5, '854f77a5df34497a9af1d16379821f2b'),
	(1716, 5, 2, '854f77a5df34497a9af1d16379821f2b'),
	(1717, 5, 16, '854f77a5df34497a9af1d16379821f2b'),
	(1718, 5, 18, '854f77a5df34497a9af1d16379821f2b'),
	(1719, 5, 3, '854f77a5df34497a9af1d16379821f2b'),
	(1720, 5, 14, '854f77a5df34497a9af1d16379821f2b'),
	(1721, 5, 15, '854f77a5df34497a9af1d16379821f2b'),
	(1722, 5, 1, '854f77a5df34497a9af1d16379821f2b'),
	(1723, 5, 13, '854f77a5df34497a9af1d16379821f2b'),
	(1724, 5, 31, '854f77a5df34497a9af1d16379821f2b'),
	(1725, 5, 35, '854f77a5df34497a9af1d16379821f2b'),
	(1726, 5, 37, '854f77a5df34497a9af1d16379821f2b'),
	(1727, 5, 44, '854f77a5df34497a9af1d16379821f2b'),
	(1728, 5, 36, '854f77a5df34497a9af1d16379821f2b'),
	(1729, 5, 38, '854f77a5df34497a9af1d16379821f2b'),
	(1730, 5, 33, '854f77a5df34497a9af1d16379821f2b'),
	(1731, 5, 32, '854f77a5df34497a9af1d16379821f2b'),
	(1732, 5, 34, '854f77a5df34497a9af1d16379821f2b'),
	(1733, 5, 12, '854f77a5df34497a9af1d16379821f2b'),
	(1734, 5, 41, '854f77a5df34497a9af1d16379821f2b'),
	(1735, 5, 39, '854f77a5df34497a9af1d16379821f2b'),
	(1736, 5, 40, '854f77a5df34497a9af1d16379821f2b'),
	(1737, 5, 43, '854f77a5df34497a9af1d16379821f2b'),
	(1738, 5, 42, '854f77a5df34497a9af1d16379821f2b'),
	(1739, 5, 19, '854f77a5df34497a9af1d16379821f2b'),
	(1740, 5, 9, '854f77a5df34497a9af1d16379821f2b'),
	(1741, 5, 10, '854f77a5df34497a9af1d16379821f2b'),
	(1742, 5, 7, '854f77a5df34497a9af1d16379821f2b'),
	(1743, 5, 8, '854f77a5df34497a9af1d16379821f2b'),
	(1744, 5, 45, '854f77a5df34497a9af1d16379821f2b'),
	(1745, 5, 20, '854f77a5df34497a9af1d16379821f2b'),
	(1746, 5, 21, '854f77a5df34497a9af1d16379821f2b'),
	(1747, 5, 51, '854f77a5df34497a9af1d16379821f2b'),
	(1748, 5, 52, '854f77a5df34497a9af1d16379821f2b'),
	(1749, 5, 53, '854f77a5df34497a9af1d16379821f2b'),
	(1750, 5, 60, '854f77a5df34497a9af1d16379821f2b'),
	(1751, 5, 61, '854f77a5df34497a9af1d16379821f2b'),
	(1752, 5, 62, '854f77a5df34497a9af1d16379821f2b');
/*!40000 ALTER TABLE `lyadmin_role_menubutton_permission` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_role_menubutton_permission_dept 结构
CREATE TABLE IF NOT EXISTS `lyadmin_role_menubutton_permission_dept` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `rolemenubuttonpermission_id` bigint(20) NOT NULL,
  `dept_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lyadmin_role_menubutton__rolemenubuttonpermission_a2aab5ca_uniq` (`rolemenubuttonpermission_id`,`dept_id`),
  KEY `lyadmin_role_menubutton_per_rolemenubuttonpermission_id_52ca0864` (`rolemenubuttonpermission_id`),
  KEY `lyadmin_role_menubutton_permission_dept_dept_id_5f503465` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_role_menubutton_permission_dept 的数据：~0 rows (大约)
DELETE FROM `lyadmin_role_menubutton_permission_dept`;
/*!40000 ALTER TABLE `lyadmin_role_menubutton_permission_dept` DISABLE KEYS */;
/*!40000 ALTER TABLE `lyadmin_role_menubutton_permission_dept` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_role_menu_permission 结构
CREATE TABLE IF NOT EXISTS `lyadmin_role_menu_permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `menu_id` varchar(100) NOT NULL,
  `role_id` varchar(100) NOT NULL,
  `data_scope` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lyadmin_role_menu_permission_menu_id_f7ea8c61` (`menu_id`),
  KEY `lyadmin_role_menu_permission_role_id_528f1e28` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=468 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_role_menu_permission 的数据：~18 rows (大约)
DELETE FROM `lyadmin_role_menu_permission`;
/*!40000 ALTER TABLE `lyadmin_role_menu_permission` DISABLE KEYS */;
INSERT INTO `lyadmin_role_menu_permission` (`id`, `menu_id`, `role_id`, `data_scope`) VALUES
	(450, '4a7a7748387f44dbab72027d8bdc87f7', '854f77a5df34497a9af1d16379821f2b', 4),
	(451, '98870fbaffb348ab9fd16a88e946bf09', '854f77a5df34497a9af1d16379821f2b', 4),
	(452, '44662b7fe6b54395994f28ed88eaf3f0', '854f77a5df34497a9af1d16379821f2b', 4),
	(453, '01599f73f61848aa811f687b1cfc1588', '854f77a5df34497a9af1d16379821f2b', 4),
	(454, '9ece0330c65e40df8da00190107d908e', '854f77a5df34497a9af1d16379821f2b', 4),
	(455, '150e0957200146b3bd0226c45e8031f7', '854f77a5df34497a9af1d16379821f2b', 4),
	(456, '563092a536194a1493551a0043f1f1a3', '854f77a5df34497a9af1d16379821f2b', 4),
	(457, '4f947108c5bf44f2b97e4a80daebf772', '854f77a5df34497a9af1d16379821f2b', 4),
	(458, '6354ba32ae734b5eaa799a65f76deee6', '854f77a5df34497a9af1d16379821f2b', 4),
	(459, '205910763e0e42fbbc12833d2f7d61bb', '854f77a5df34497a9af1d16379821f2b', 4),
	(460, 'af862854dc44410d84b8b2ae5c16c90d', '854f77a5df34497a9af1d16379821f2b', 4),
	(461, '31552696153b42599ce1faf6fe495824', '854f77a5df34497a9af1d16379821f2b', 4),
	(462, '95227fe101e747908c12b56d2bae5e8e', '854f77a5df34497a9af1d16379821f2b', 4),
	(463, '2e9937b37ac94e248e9ed159bfe7b655', '854f77a5df34497a9af1d16379821f2b', 4),
	(464, '1b5018bdb5e04698b84da505e8a6b93c', '854f77a5df34497a9af1d16379821f2b', 4),
	(465, '8faec98030e443b99ce0d4c636163db7', '854f77a5df34497a9af1d16379821f2b', 4),
	(466, '24d2eb79a21141afbe73058cc02545e0', '854f77a5df34497a9af1d16379821f2b', 4),
	(467, 'a8b435647f0b4a3f852ec796433e8919', '854f77a5df34497a9af1d16379821f2b', 4);
/*!40000 ALTER TABLE `lyadmin_role_menu_permission` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_role_menu_permission_dept 结构
CREATE TABLE IF NOT EXISTS `lyadmin_role_menu_permission_dept` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `rolemenupermission_id` bigint(20) NOT NULL,
  `dept_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lyadmin_role_menu_permis_rolemenupermission_id_de_85994b30_uniq` (`rolemenupermission_id`,`dept_id`),
  KEY `lyadmin_role_menu_permission_dept_rolemenupermission_id_62dbd810` (`rolemenupermission_id`),
  KEY `lyadmin_role_menu_permission_dept_dept_id_bec14fd0` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_role_menu_permission_dept 的数据：~0 rows (大约)
DELETE FROM `lyadmin_role_menu_permission_dept`;
/*!40000 ALTER TABLE `lyadmin_role_menu_permission_dept` DISABLE KEYS */;
/*!40000 ALTER TABLE `lyadmin_role_menu_permission_dept` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_system_config 结构
CREATE TABLE IF NOT EXISTS `lyadmin_system_config` (
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `title` varchar(50) NOT NULL,
  `key` varchar(20) NOT NULL,
  `value` longtext,
  `sort` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `data_options` longtext,
  `form_item_type` smallint(6) DEFAULT NULL,
  `rule` longtext,
  `placeholder` varchar(50) DEFAULT NULL,
  `tip` varchar(100) DEFAULT NULL,
  `setting` longtext,
  `creator_id` varchar(100) DEFAULT NULL,
  `parent_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lyadmin_system_config_key_parent_id_97f056cc_uniq` (`key`,`parent_id`),
  KEY `lyadmin_system_config_key_7aeced64` (`key`),
  KEY `lyadmin_system_config_creator_id_bd4f327e` (`creator_id`),
  KEY `lyadmin_system_config_parent_id_2c3a27d0` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_system_config 的数据：~5 rows (大约)
DELETE FROM `lyadmin_system_config`;
/*!40000 ALTER TABLE `lyadmin_system_config` DISABLE KEYS */;
INSERT INTO `lyadmin_system_config` (`id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `title`, `key`, `value`, `sort`, `status`, `data_options`, `form_item_type`, `rule`, `placeholder`, `tip`, `setting`, `creator_id`, `parent_id`) VALUES
	('11da46ef4d494aa0be2ff5958ff98f0b', '0', '', '2025-07-10 16:10:13.620113', '2025-07-08 10:10:49.583026', '登录验证码', 'loginCaptcha', 'true', 8, 1, NULL, 9, NULL, NULL, '登录验证码开启/关闭', NULL, '0', '3593fb777e1e4f77a1e62ed7eb0681a7'),
	('3593fb777e1e4f77a1e62ed7eb0681a7', '0', '', '2025-07-08 09:16:31.279978', '2025-07-08 09:16:31.279978', '基础配置', 'base', NULL, 0, 1, NULL, 0, NULL, NULL, NULL, NULL, '0', NULL),
	('59421c76edb34bc8a7ba622cb6ed8133', '0', '', '2025-07-08 11:31:49.893906', '2025-07-08 09:59:04.263742', 'logo', 'logo', 'http://127.0.0.1:8000/media/platform/2025-07-08/20250708113144_688.png', 10, 1, NULL, 7, NULL, NULL, NULL, NULL, '0', '3593fb777e1e4f77a1e62ed7eb0681a7'),
	('5d66345539d849e4b4ad766e99c0b25f', '0', '', '2025-07-10 10:48:16.768615', '2025-07-08 18:00:59.574827', 'Api白名单', 'apiWhiteList', '[]', 0, 1, NULL, 0, NULL, NULL, NULL, NULL, '0', NULL),
	('8b9a6e5f079e4fbe8627185c2322d9b0', '0', '', '2025-07-10 16:17:33.260218', '2025-07-10 16:12:49.228531', '系统标题', 'systitle', 'dvlyadmin-mini', 5, 1, NULL, 0, NULL, '请输入系统标题', NULL, NULL, '0', '3593fb777e1e4f77a1e62ed7eb0681a7');
/*!40000 ALTER TABLE `lyadmin_system_config` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_users 结构
CREATE TABLE IF NOT EXISTS `lyadmin_users` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `id` varchar(100) NOT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `dept_belong` varchar(100) DEFAULT NULL,
  `update_datetime` datetime(6) DEFAULT NULL,
  `create_datetime` datetime(6) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(60) DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  `name` varchar(40) NOT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `gender` smallint(6) DEFAULT NULL,
  `login_error_nums` int(11) NOT NULL,
  `identity` smallint(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `creator_id` varchar(100) DEFAULT NULL,
  `dept_id` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `lyadmin_users_creator_id_92824513` (`creator_id`),
  KEY `lyadmin_users_dept_id_ba5fbf41` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_users 的数据：~2 rows (大约)
DELETE FROM `lyadmin_users`;
/*!40000 ALTER TABLE `lyadmin_users` DISABLE KEYS */;
INSERT INTO `lyadmin_users` (`password`, `last_login`, `id`, `modifier`, `dept_belong`, `update_datetime`, `create_datetime`, `username`, `email`, `mobile`, `avatar`, `name`, `nickname`, `gender`, `login_error_nums`, `identity`, `is_delete`, `is_staff`, `is_superuser`, `creator_id`, `dept_id`, `is_active`) VALUES
	('pbkdf2_sha256$390000$2Dj9ivbPKFiiZPXstZTQK3$5ymKI10SNdJ1PAOIs9RnQUiuSkko8T088e51wK8LVJ8=', '2025-07-13 15:46:45.585754', '0', NULL, NULL, '2025-07-13 15:46:45.585754', '2025-05-25 09:59:08.255150', 'superadmin', NULL, NULL, NULL, '超级管理员', '超级管理员', NULL, 0, 0, 0, 1, 1, NULL, '', 1),
	('pbkdf2_sha256$390000$aLGgQHxt3Oairx8hYnYN4Z$+tkaUbcKM7fHPsbBpTxIcXO5Lu9ZBchPlMavG/lHhpw=', '2025-07-05 08:51:37.899112', '1792aea416944eff9e3845aec6ac88b4', '0', '', '2025-07-05 08:51:37.904545', '2025-06-30 12:24:34.575727', 'admin', '1042594286@qq.com', '15888888888', '', '管理员', '管理员', 2, 0, 1, 0, 1, 0, '0', '8b304f92647747aabffc7e8750397762', 1);
/*!40000 ALTER TABLE `lyadmin_users` ENABLE KEYS */;

-- 导出  表 dvlyadmin_mini.lyadmin_users_role 结构
CREATE TABLE IF NOT EXISTS `lyadmin_users_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `users_id` varchar(100) NOT NULL,
  `role_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lyadmin_users_role_users_id_role_id_475ae0d5_uniq` (`users_id`,`role_id`),
  KEY `lyadmin_users_role_users_id_25f578a0` (`users_id`),
  KEY `lyadmin_users_role_role_id_0f927f87` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  dvlyadmin_mini.lyadmin_users_role 的数据：~0 rows (大约)
DELETE FROM `lyadmin_users_role`;
/*!40000 ALTER TABLE `lyadmin_users_role` DISABLE KEYS */;
INSERT INTO `lyadmin_users_role` (`id`, `users_id`, `role_id`) VALUES
	(1, '1792aea416944eff9e3845aec6ac88b4', '854f77a5df34497a9af1d16379821f2b');
/*!40000 ALTER TABLE `lyadmin_users_role` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
