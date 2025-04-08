-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 07, 2025 at 04:28 PM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `payment_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
CREATE TABLE IF NOT EXISTS `payment` (
  `id` varchar(36) NOT NULL,
  `amount` float NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `booking_id` varchar(36) NOT NULL,
  `payment_type` varchar(20) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `paypal_payment_id` varchar(100) DEFAULT NULL,
  `paypal_sale_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`id`, `amount`, `user_id`, `booking_id`, `payment_type`, `status`, `created_at`, `updated_at`, `paypal_payment_id`, `paypal_sale_id`) VALUES
('0b156404-c8e8-46cd-85cd-0cea33d4f424', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-05 23:11:43', '2025-04-05 23:11:43', 'PAYID-M7YUQLQ5AX13004K49113339', NULL),
('1da45173-a258-4bf3-83cf-71ea20431c2a', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-06 02:04:41', '2025-04-06 02:04:41', 'PAYID-M7YXBOA2ED82748DF205534V', NULL),
('20a27cb0-8248-4747-8844-384481f559d4', 420, 'user123', 'temp_user123', 'flex', 'pending', '2025-04-02 23:57:24', '2025-04-02 23:57:24', 'PAYID-M7WV4YY38L03732PA298324W', NULL),
('29e4cbb5-d7d9-42de-92d5-b041bc5ab4c9', 250, '42', 'flex_test_123', 'flex', 'success', '2025-04-06 02:26:56', '2025-04-06 02:27:28', 'PAYID-M7YXL3Y5ME231210M807640M', '6JJ89354A0549230B'),
('2a121da4-3d50-4ad5-b9e1-632ec0de2bd2', 199.99, 'user_12345', 'booking_67890', 'normal', 'refunded', '2025-03-27 14:20:21', '2025-03-27 14:29:51', 'PAYID-M7SO4JI8V829177HS674560H', '5DA46449E3399354U'),
('2ba23276-01b5-426c-a3e3-f2849c0c9d7f', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-05 21:41:48', '2025-04-05 21:41:48', 'PAYID-M7YTGGY6UR075991R8649507', NULL),
('3d09f0a7-bdf9-4fa8-80f3-5650a66832a3', 330, '1', 'temp_1', 'flex', 'success', '2025-04-06 14:51:13', '2025-04-06 14:51:40', 'PAYID-M7ZCIYA53U1434262237471V', '6HF913046M000114L'),
('4c0bd12b-9668-453b-a0f5-4d6d979a8fd4', 330, '1', 'temp_1', 'flex', 'success', '2025-04-06 03:06:43', '2025-04-06 03:06:50', 'PAYID-M7YX6QQ3CG05050UX488281E', '43957645MK973060K'),
('5f47db42-347e-49df-b2fa-11f2b9363bef', 330, '1', 'temp_1', 'flex', 'success', '2025-04-06 03:05:01', '2025-04-06 03:05:09', 'PAYID-M7YX5XI86A05897JA970443E', '3PB10659N8315363M'),
('5fb3c5ea-f543-4eb3-946c-763154dfd3ed', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-05 20:49:06', '2025-04-05 20:49:06', 'PAYID-M7YSNQQ9BM242676J492091X', NULL),
('67d24a53-731e-4e51-b217-b2ba73a2aefa', 100.5, '12345', '', '', 'refunded', '2025-03-25 17:15:17', '2025-03-26 23:16:12', NULL, NULL),
('899b6321-289f-4ce9-bdc0-e7de6bf68e99', 330, '1', 'temp_1', 'flex', 'success', '2025-04-06 03:02:34', '2025-04-06 03:02:43', 'PAYID-M7YX4SI7L897600TM003721R', '63C295004U185470F'),
('96e6fc30-e9a7-47af-805b-dbdd1294a650', 150, '123', '456', 'flex', 'pending', '2025-04-04 12:36:02', '2025-04-04 12:36:02', 'PAYID-M7XWDMQ8GN75158AG899711B', NULL),
('9b9c7e0e-f719-4ec6-b290-feb3767ae7ff', 330, '1', 'temp_1', 'flex', 'success', '2025-04-07 23:20:48', '2025-04-07 23:21:15', 'PAYID-M7Z62TY2G889670CS549680V', '0A9486582R025241R'),
('a5fe6bff-2576-4dd0-844a-85097fce89d5', 350, '1', 'temp_1', 'flex', 'pending', '2025-04-07 16:44:30', '2025-04-07 16:44:30', 'PAYID-M7ZZA3Q18F46558CS1098224', NULL),
('b662afd3-015e-4282-94e9-71e75986cb69', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-05 20:58:37', '2025-04-05 20:58:37', 'PAYID-M7YSR7I8YX48125008033642', NULL),
('ba07176d-cd3f-4174-9ac2-d0fa8ae4f542', 100.5, '12345678-abcd-1234-abcd-12345678abcd', '98765432-dcba-4321-dcba-98765432dcba', 'normal', 'pending', '2025-03-26 21:49:24', '2025-03-26 21:49:24', NULL, NULL),
('c8217902-2571-492f-8676-fd66b5db5531', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-06 01:13:21', '2025-04-06 01:13:21', 'PAYID-M7YWJMA7W461713B9295732N', NULL),
('c950931b-88c2-4d0b-9513-0d3bc8d21be6', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-05 20:56:32', '2025-04-05 20:56:32', 'PAYID-M7YSQ7Y87X18087PU029390H', NULL),
('cd1c57b6-e629-4ecd-9258-1684c9edbb6b', 250.75, '87654321-dcba-4321-dcba-87654321dcba', '23456789-abcd-2345-abcd-23456789abcd', 'flex', 'refunded', '2025-03-25 18:13:03', '2025-03-26 23:08:49', NULL, NULL),
('cf681f3c-16fe-4a39-ab7b-b5d62f21becc', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-05 22:39:12', '2025-04-05 22:39:12', 'PAYID-M7YUBDY9M67642394328263M', NULL),
('d331a4ba-514e-43fd-9c3b-a42ff07edf7b', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-06 02:08:28', '2025-04-06 02:08:28', 'PAYID-M7YXDHA0HD25056NX096100E', NULL),
('ef9f4898-863e-4052-8a40-43d56b65bd79', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-05 22:40:29', '2025-04-05 22:40:29', 'PAYID-M7YUBXI4RS80846JA291770V', NULL),
('f06dc6ff-d57e-41be-b571-8301b99adf30', 100.5, '12345678-abcd-1234-abcd-12345678abcd', '98765432-dcba-4321-dcba-98765432dcba', 'normal', 'pending', '2025-03-26 22:48:39', '2025-03-26 22:48:39', NULL, NULL),
('f4770f1b-c18f-4fc0-99d6-48cb9271a150', 330, '1', 'temp_1', 'flex', 'pending', '2025-04-06 02:56:01', '2025-04-06 02:56:01', 'PAYID-M7YXZQA3WB57196J5715435W', NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
