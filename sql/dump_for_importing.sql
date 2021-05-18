-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 12, 2021 at 09:13 PM
-- Server version: 10.4.18-MariaDB-log
-- PHP Version: 7.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_bairdjo`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer_contacts`
--

DROP TABLE IF EXISTS `customer_contacts`;
CREATE TABLE `customer_contacts` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  `house_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer_contacts`
--

INSERT INTO `customer_contacts` (`id`, `first_name`, `last_name`, `email`, `phone_number`, `house_id`) VALUES
(1, 'Lawrence', 'Lima', 'lawrence@email.com', '123-456-7890', 1),
(2, 'Mandy', 'Mike', 'mandy@email.com', '234-567-8901', 2),
(3, 'Norman', 'November', 'norman@email.com', '345-678-9012', 3),
(4, 'Ollie', 'Oscar', 'ollie@email.com', '456-789-0123', 4),
(5, 'Paul', 'Papa', 'paul@email.com', '567-890-1234', 5),
(6, 'Pauline', 'Papa', 'pauline@email.com', '678-901-2345', 5);

-- --------------------------------------------------------

--
-- Table structure for table `houses`
--

DROP TABLE IF EXISTS `houses`;
CREATE TABLE `houses` (
  `id` int(11) NOT NULL,
  `street_address` varchar(100) NOT NULL,
  `street_address_2` varchar(100) DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(2) NOT NULL,
  `zip_code` varchar(5) NOT NULL,
  `yard_size_acres` decimal(8,2) NOT NULL,
  `sales_manager_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `houses`
--

INSERT INTO `houses` (`id`, `street_address`, `street_address_2`, `city`, `state`, `zip_code`, `yard_size_acres`, `sales_manager_id`) VALUES
(1, '1 Alpha Road', NULL, 'Lennyville', 'NY', '98765', '1.10', 1),
(2, '2 Beta Street', NULL, 'Lennyville', 'NY', '98765', '1.20', 1),
(3, '3 Charlie Ave', 'Unit 10', 'Lennyville', 'NY', '98765', '1.30', 2),
(4, '4 Delta Court', NULL, 'Lennyville', 'NY', '98765', '1.40', 2),
(5, '5 Echo Lane', NULL, 'Lennyville', 'NY', '98765', '1.50', 3);

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `house_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`id`, `date`, `total_price`, `house_id`) VALUES
(1, '2020-04-01', '55.00', 1),
(2, '2020-04-02', '60.00', 2),
(3, '2020-04-03', '65.00', 3),
(4, '2020-04-04', '70.00', 4),
(5, '2020-04-05', '75.00', 5),
(6, '2020-04-11', '70.00', 4),
(7, '2020-04-12', '75.00', 5);

-- --------------------------------------------------------

--
-- Table structure for table `job_workers`
--

DROP TABLE IF EXISTS `job_workers`;
CREATE TABLE `job_workers` (
  `job_id` int(11) NOT NULL,
  `worker_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `job_workers`
--

INSERT INTO `job_workers` (`job_id`, `worker_id`) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 2),
(3, 3),
(4, 3),
(5, 3),
(6, 1),
(6, 4),
(7, 1),
(7, 4);

-- --------------------------------------------------------

--
-- Table structure for table `lawnmowers`
--

DROP TABLE IF EXISTS `lawnmowers`;
CREATE TABLE `lawnmowers` (
  `id` int(11) NOT NULL,
  `brand` varchar(100) NOT NULL,
  `make_year` int(11) NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `is_functional` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `lawnmowers`
--

INSERT INTO `lawnmowers` (`id`, `brand`, `make_year`, `model_name`, `is_functional`) VALUES
(1, 'Alpha Motors', 2020, 'Slicer1000', 1),
(2, 'Bravo Motors', 2019, 'Mower2000', 1),
(3, 'Charlie Motors', 2018, 'Roarer3000', 1),
(4, 'Delta Motors', 2017, 'Cutter4000', 1),
(5, 'Echo Motors', 2016, 'Chopper5000', 1),
(6, 'Foxtrot Motors', 2015, 'Snipper6000', 0),
(7, 'Golf Motors', 2015, 'Vroomer7000', 1),
(8, 'Hotel Motors', 2015, 'Soarer8000', 1);

-- --------------------------------------------------------

--
-- Table structure for table `sales_managers`
--

DROP TABLE IF EXISTS `sales_managers`;
CREATE TABLE `sales_managers` (
  `id` int(11) NOT NULL,
  `region` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `sales_managers`
--

INSERT INTO `sales_managers` (`id`, `region`, `first_name`, `last_name`, `email`, `phone_number`) VALUES
(1, 'North', 'Zach', 'Zulu', 'zach@lennys.com', '111-111-1111'),
(2, 'South', 'Yara', 'Yankee', 'yara@lennys.com', '222-222-2222'),
(3, 'East', 'Xavier', 'Xray', 'xavier@lennys.com', '333-333-3333');

-- --------------------------------------------------------

--
-- Table structure for table `workers`
--

DROP TABLE IF EXISTS `workers`;
CREATE TABLE `workers` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  `lawnmower_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `workers`
--

INSERT INTO `workers` (`id`, `first_name`, `last_name`, `email`, `phone_number`, `lawnmower_id`) VALUES
(1, 'Adam', 'Alpha', 'adam@lennys.com', '999-999-9999', 1),
(2, 'Brenda', 'Bravo', 'brenda@lennys.com', '888-888-8888', 2),
(3, 'Connor', 'Charlie', 'connor@lennys.com', '777-777-7777', 3),
(4, 'Denise', 'Delta', 'denise@lennys.com', '666-666-6666', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer_contacts`
--
ALTER TABLE `customer_contacts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `house_id` (`house_id`);

--
-- Indexes for table `houses`
--
ALTER TABLE `houses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sales_manager_id` (`sales_manager_id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `house_id` (`house_id`);

--
-- Indexes for table `job_workers`
--
ALTER TABLE `job_workers`
  ADD PRIMARY KEY (`job_id`,`worker_id`),
  ADD KEY `job_id` (`job_id`),
  ADD KEY `worker_id` (`worker_id`);

--
-- Indexes for table `lawnmowers`
--
ALTER TABLE `lawnmowers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sales_managers`
--
ALTER TABLE `sales_managers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `workers`
--
ALTER TABLE `workers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lawnmower_id` (`lawnmower_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer_contacts`
--
ALTER TABLE `customer_contacts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `houses`
--
ALTER TABLE `houses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `lawnmowers`
--
ALTER TABLE `lawnmowers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `sales_managers`
--
ALTER TABLE `sales_managers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `workers`
--
ALTER TABLE `workers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customer_contacts`
--
ALTER TABLE `customer_contacts`
  ADD CONSTRAINT `customer_contacts_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `houses` (`id`);

--
-- Constraints for table `houses`
--
ALTER TABLE `houses`
  ADD CONSTRAINT `houses_ibfk_1` FOREIGN KEY (`sales_manager_id`) REFERENCES `sales_managers` (`id`);

--
-- Constraints for table `jobs`
--
ALTER TABLE `jobs`
  ADD CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `houses` (`id`);

--
-- Constraints for table `job_workers`
--
ALTER TABLE `job_workers`
  ADD CONSTRAINT `job_workers_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`),
  ADD CONSTRAINT `job_workers_ibfk_2` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`);

--
-- Constraints for table `workers`
--
ALTER TABLE `workers`
  ADD CONSTRAINT `workers_ibfk_1` FOREIGN KEY (`lawnmower_id`) REFERENCES `lawnmowers` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
