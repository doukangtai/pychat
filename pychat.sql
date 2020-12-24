/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : localhost:3306
 Source Schema         : pychat

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 24/12/2020 16:24:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for msg
-- ----------------------------
DROP TABLE IF EXISTS `msg`;
CREATE TABLE `msg`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `datetime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `msg` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of msg
-- ----------------------------
INSERT INTO `msg` VALUES (1, 'root3', '2020-12-24 12:57:45', '我是root3的消息\n');
INSERT INTO `msg` VALUES (2, 'root5', '2020-12-24 12:58:09', 'root5发送的消息\n');
INSERT INTO `msg` VALUES (3, 'root1', '2020-12-24 13:41:01', '用户名为root1的用户发送的消息\n');
INSERT INTO `msg` VALUES (4, 'root1', '2020-12-24 13:45:27', '111\n');
INSERT INTO `msg` VALUES (5, 'root3', '2020-12-24 13:45:59', '333\n');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `verify` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'root1', '202cb962ac59075b964b07152d234b70', 'abc');
INSERT INTO `user` VALUES (2, 'root2', '202cb962ac59075b964b07152d234b70', 'abc');
INSERT INTO `user` VALUES (10, 'root3', '202cb962ac59075b964b07152d234b70', 'abc');
INSERT INTO `user` VALUES (11, 'root4', '202cb962ac59075b964b07152d234b70', 'abc');
INSERT INTO `user` VALUES (13, 'root6', '202cb962ac59075b964b07152d234b70', 'abc');
INSERT INTO `user` VALUES (14, 'root5', 'e10adc3949ba59abbe56e057f20f883e', '123');
INSERT INTO `user` VALUES (15, 'root7', '202cb962ac59075b964b07152d234b70', '123');
INSERT INTO `user` VALUES (16, 'root8', '202cb962ac59075b964b07152d234b70', '123');
INSERT INTO `user` VALUES (17, 'root9', '202cb962ac59075b964b07152d234b70', '123');
INSERT INTO `user` VALUES (18, 'root10', '202cb962ac59075b964b07152d234b70', '123');
INSERT INTO `user` VALUES (19, 'root11', '202cb962ac59075b964b07152d234b70', '123');
INSERT INTO `user` VALUES (20, 'root12', '202cb962ac59075b964b07152d234b70', '123');

SET FOREIGN_KEY_CHECKS = 1;
