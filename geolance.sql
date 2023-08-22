-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 02, 2023 at 02:51 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `geolance`
--

-- --------------------------------------------------------

--
-- Table structure for table `chats`
--

CREATE TABLE `chats` (
  `last_message_content` varchar(20) DEFAULT NULL,
  `last_message_sender_id` int(11) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `chat_members`
--

CREATE TABLE `chat_members` (
  `member_id` int(11) DEFAULT NULL,
  `chat_id` int(11) DEFAULT NULL,
  `member_saxeli` varchar(50) DEFAULT NULL,
  `member_pfp` varchar(90) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `role_rank` int(11) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `deliveries`
--

CREATE TABLE `deliveries` (
  `id` int(11) NOT NULL,
  `gig_id` int(11) DEFAULT NULL,
  `lancer_id` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  `review` float DEFAULT NULL,
  `mindro` int(11) DEFAULT NULL,
  `maxdro` int(11) DEFAULT NULL,
  `dro` int(11) DEFAULT NULL,
  `mitanisdro` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `dms`
--

CREATE TABLE `dms` (
  `id` int(11) NOT NULL,
  `last_message_content` varchar(31) DEFAULT NULL,
  `last_message_sender_id` int(11) DEFAULT NULL,
  `user_one` int(11) DEFAULT NULL,
  `user_two` int(11) DEFAULT NULL,
  `last_message_time` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `user_one_state` varchar(20) DEFAULT 'unseen',
  `user_two_state` varchar(20) DEFAULT 'unseen',
  `last_message_id` int(11) DEFAULT NULL,
  `user_one_seen` int(1) DEFAULT 0,
  `user_two_seen` int(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `dm_msgs`
--

CREATE TABLE `dm_msgs` (
  `id` int(11) NOT NULL,
  `message` varchar(2000) DEFAULT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `message_type` varchar(400) DEFAULT NULL,
  `dmchat_id` int(11) DEFAULT NULL,
  `message_date` varchar(15) DEFAULT NULL,
  `message_dtype` varchar(50) DEFAULT NULL,
  `reply_to_msgid` int(11) DEFAULT NULL,
  `message_status` varchar(15) DEFAULT NULL,
  `message_time` int(11) DEFAULT NULL,
  `seen_by_other` int(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dm_msgs`
--

-- --------------------------------------------------------

--
-- Table structure for table `lancer_params`
--

CREATE TABLE `lancer_params` (
  `id` int(11) NOT NULL,
  `about_me` varchar(400) DEFAULT NULL,
  `ganatleba` varchar(400) DEFAULT NULL,
  `aidi` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lancer_params`
--


-- --------------------------------------------------------

--
-- Table structure for table `lancer_sferos`
--

CREATE TABLE `lancer_sferos` (
  `id` int(11) NOT NULL,
  `sfero` varchar(60) DEFAULT NULL,
  `subsfero` varchar(60) DEFAULT NULL,
  `aidi` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lancer_sferos`
--

--------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `notification_recipient_id` int(11) DEFAULT NULL,
  `notification_img` varchar(200) DEFAULT NULL,
  `notification_title` varchar(100) DEFAULT NULL,
  `notification_description` varchar(1000) DEFAULT NULL,
  `notification_link` varchar(200) DEFAULT NULL,
  `notification_time` varchar(50) DEFAULT NULL,
  `notification_date` varchar(50) DEFAULT NULL,
  `notification_seen_bool` int(1) DEFAULT NULL,
  `notification_subimg` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `orderer_id` int(11) DEFAULT NULL,
  `ordered_service_id` int(11) DEFAULT NULL,
  `order_time` int(11) DEFAULT NULL,
  `order_date` varchar(30) DEFAULT NULL,
  `delivery_time` int(11) DEFAULT NULL,
  `delivery_date` varchar(30) DEFAULT NULL,
  `fasi` float DEFAULT NULL,
  `points_ls_names` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

-- --------------------------------------------------------

--
-- Table structure for table `points`
--

CREATE TABLE `points` (
  `id` int(11) NOT NULL,
  `point` int(11) DEFAULT NULL,
  `fasi` float DEFAULT NULL,
  `dro` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `saxeli` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `points`
--
 

-- --------------------------------------------------------

--
-- Table structure for table `servisebi`
--

CREATE TABLE `servisebi` (
  `id` int(11) NOT NULL,
  `satauri` varchar(80) DEFAULT NULL,
  `agwera` varchar(1000) DEFAULT NULL,
  `fasi` float DEFAULT NULL,
  `suratebi_list` varchar(200) DEFAULT NULL,
  `offer_tipi` varchar(30) DEFAULT NULL,
  `offer_subtipi` varchar(30) DEFAULT NULL,
  `client_raodenoba` int(11) DEFAULT NULL,
  `gamocdileba` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `profile` varchar(50) DEFAULT NULL,
  `main_rating` float DEFAULT 1,
  `pasuxismgebloba_rating` float DEFAULT 1,
  `as_described_rating` float DEFAULT 1,
  `tags` varchar(100) DEFAULT NULL,
  `imgsrc_list` varchar(400) DEFAULT NULL,
  `dro` int(11) DEFAULT NULL,
  `maxfasi` float DEFAULT NULL,
  `maxdro` int(11) DEFAULT NULL,
  `suratebi` varchar(300) DEFAULT NULL,
  `max_clients` int(11) DEFAULT 1,
  `points` int(11) DEFAULT 1,
  `current_orders` int(11) DEFAULT 0,
  `gamocdileba_fasi` int(11) DEFAULT 1,
  `gamocdileba_time` int(11) DEFAULT 1,
  `status` varchar(30) DEFAULT NULL,
  `rated` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `servisebi`
--
-- --------------------------------------------------------

--
-- Table structure for table `servisebis_history`
--

CREATE TABLE `servisebis_history` (
  `id` int(11) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `saxeli` varchar(100) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `xani` int(11) DEFAULT NULL,
  `tipi` varchar(50) DEFAULT NULL,
  `fasi` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `servisebis_history`
--
 
-- --------------------------------------------------------

--
-- Table structure for table `servisebis_reitingi`
--

CREATE TABLE `servisebis_reitingi` (
  `id` int(11) NOT NULL,
  `main_rating` float DEFAULT NULL,
  `rater_id` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `pasuxismgebloba_rating` float DEFAULT NULL,
  `as_described_rating` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `servisebis_reitingi`
--
 
-- --------------------------------------------------------

--
-- Table structure for table `servis_packets`
--

CREATE TABLE `servis_packets` (
  `id` int(11) NOT NULL,
  `saxeli` varchar(100) DEFAULT NULL,
  `agwera` varchar(500) DEFAULT NULL,
  `min_fasi` float DEFAULT NULL,
  `max_fasi` float DEFAULT NULL,
  `fasi` float DEFAULT NULL,
  `assets_list` varchar(1000) DEFAULT NULL,
  `mitanisdro_dge` int(11) DEFAULT NULL,
  `min_mitanisdro_dge` int(11) DEFAULT NULL,
  `max_mitanisdro_dge` int(11) DEFAULT NULL,
  `shemotavazeba` varchar(300) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `site_joins`
--

CREATE TABLE `site_joins` (
  `id` int(11) NOT NULL,
  `ipaddr` varchar(50) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `site_joins`
--
 
-- --------------------------------------------------------

--
-- Table structure for table `stalks`
--

CREATE TABLE `stalks` (
  `stalker_id` int(11) DEFAULT NULL,
  `stalked_id` int(11) DEFAULT NULL,
  `stalk_time` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stalks`
--
 
-- --------------------------------------------------------

--
-- Table structure for table `timeouts`
--

CREATE TABLE `timeouts` (
  `id` int(11) NOT NULL,
  `tipi` varchar(60) DEFAULT NULL,
  `aidi` varchar(60) DEFAULT NULL,
  `dro` int(11) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `timeouts`
--
 
-- --------------------------------------------------------

--
-- Table structure for table `turebi`
--

CREATE TABLE `turebi` (
  `id` int(11) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `general` char(1) DEFAULT 'F',
  `desc_and_exp` char(1) DEFAULT 'F',
  `packets` char(1) DEFAULT 'F',
  `points` char(1) DEFAULT 'F',
  `files` char(1) DEFAULT 'F'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `turebi`
--
 
-- --------------------------------------------------------

--
-- Table structure for table `userips`
--

CREATE TABLE `userips` (
  `id` int(11) NOT NULL,
  `aidi` int(11) DEFAULT NULL,
  `ip` varchar(60) DEFAULT NULL,
  `vcode` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `userips`
--
 

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `saxeli` varchar(15) DEFAULT NULL,
  `gvari` varchar(20) DEFAULT NULL,
  `username` varchar(110) DEFAULT NULL,
  `mail` varchar(120) DEFAULT NULL,
  `password` varchar(61) DEFAULT NULL,
  `vcode` int(11) DEFAULT NULL,
  `sqesi` varchar(15) DEFAULT NULL,
  `ricxvi` varchar(25) DEFAULT NULL,
  `weli` varchar(20) DEFAULT NULL,
  `imgsrc` varchar(120) DEFAULT 'static/default.jpg',
  `angarishi` float DEFAULT 0,
  `imgsize` varchar(15) DEFAULT '100',
  `tve` int(11) DEFAULT NULL,
  `sfero` varchar(60) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `ip` varchar(50) DEFAULT NULL,
  `status` varchar(1) DEFAULT '0',
  `owner_bool` int(1) DEFAULT 0,
  `admin_bool` int(1) DEFAULT 0,
  `join_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--
 
--
-- Indexes for dumped tables
--

--
-- Indexes for table `chats`
--
ALTER TABLE `chats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `deliveries`
--
ALTER TABLE `deliveries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dms`
--
ALTER TABLE `dms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dm_msgs`
--
ALTER TABLE `dm_msgs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `lancer_params`
--
ALTER TABLE `lancer_params`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `lancer_sferos`
--
ALTER TABLE `lancer_sferos`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `points`
--
ALTER TABLE `points`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `servisebi`
--
ALTER TABLE `servisebi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `servisebis_history`
--
ALTER TABLE `servisebis_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `servisebis_reitingi`
--
ALTER TABLE `servisebis_reitingi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `servis_packets`
--
ALTER TABLE `servis_packets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `site_joins`
--
ALTER TABLE `site_joins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stalks`
--
ALTER TABLE `stalks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `timeouts`
--
ALTER TABLE `timeouts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `turebi`
--
ALTER TABLE `turebi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `userips`
--
ALTER TABLE `userips`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chats`
--
ALTER TABLE `chats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `deliveries`
--
ALTER TABLE `deliveries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `dms`
--
ALTER TABLE `dms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- AUTO_INCREMENT for table `dm_msgs`
--
ALTER TABLE `dm_msgs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3327;

--
-- AUTO_INCREMENT for table `lancer_params`
--
ALTER TABLE `lancer_params`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `lancer_sferos`
--
ALTER TABLE `lancer_sferos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1119;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `points`
--
ALTER TABLE `points`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `servisebi`
--
ALTER TABLE `servisebi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=284;

--
-- AUTO_INCREMENT for table `servisebis_history`
--
ALTER TABLE `servisebis_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `servisebis_reitingi`
--
ALTER TABLE `servisebis_reitingi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `servis_packets`
--
ALTER TABLE `servis_packets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `site_joins`
--
ALTER TABLE `site_joins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1630;

--
-- AUTO_INCREMENT for table `stalks`
--
ALTER TABLE `stalks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=415;

--
-- AUTO_INCREMENT for table `timeouts`
--
ALTER TABLE `timeouts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=240;

--
-- AUTO_INCREMENT for table `turebi`
--
ALTER TABLE `turebi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `userips`
--
ALTER TABLE `userips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2022;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
