-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 29, 2020 at 06:46 PM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aplikasihrd_db`
--
CREATE DATABASE IF NOT EXISTS `aplikasihrd_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `aplikasihrd_db`;

-- --------------------------------------------------------

--
-- Table structure for table `gaji`
--

DROP TABLE IF EXISTS `gaji`;
CREATE TABLE `gaji` (
  `id` int(100) NOT NULL,
  `nik` int(100) NOT NULL,
  `tanggal` date DEFAULT NULL,
  `gaji_pokok` int(255) NOT NULL,
  `total_gaji` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `gaji`
--

INSERT INTO `gaji` (`id`, `nik`, `tanggal`, `gaji_pokok`, `total_gaji`) VALUES
(1, 1, '2020-04-27', 3000000, 3600000),
(2, 2, '2020-04-28', 5000000, 6250000),
(3, 6, '2020-04-28', 6000000, 7800000),
(4, 2, '2020-04-29', 5000000, 6250000),
(5, 3, '2020-04-29', 10000000, 15000000);

-- --------------------------------------------------------

--
-- Table structure for table `jabatan`
--

DROP TABLE IF EXISTS `jabatan`;
CREATE TABLE `jabatan` (
  `id` varchar(11) NOT NULL,
  `nama_jabatan` varchar(100) NOT NULL,
  `tunjangan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `jabatan`
--

INSERT INTO `jabatan` (`id`, `nama_jabatan`, `tunjangan`) VALUES
('C01', 'CEO', 50),
('MN01', 'Manager', 30),
('SF01', 'Staff', 20),
('SV01', 'Supervisor', 25);

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

DROP TABLE IF EXISTS `karyawan`;
CREATE TABLE `karyawan` (
  `nik` int(100) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `jabatan` varchar(100) NOT NULL,
  `gaji_pokok` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `telp` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`nik`, `nama`, `jabatan`, `gaji_pokok`, `email`, `telp`) VALUES
(1, 'Admin HRD', 'SF01', 3000000, 'admin@admin.com', '08988347734'),
(2, 'Kevin Laurence', 'SV01', 5000000, 'heathscliff334@gmail.com', '087792923179'),
(3, 'Lala', 'C01', 10000000, 'lalalaurence@gmail.com', '0878468542'),
(4, 'Hartono', 'MN01', 6500000, 'hartono@gmail.com', '08784685468'),
(6, 'Laurence', 'MN01', 6000000, 'laurence@gmail.com', '08784685468'),
(7, 'Kevin', 'C01', 12000000, 's32170010@student.ubm.ac.id', '087819151700');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `nama_lengkap` varchar(255) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `nama_lengkap`, `role`) VALUES
(1, 'admin', 'admin', 'admin', 'admin'),
(4, 'kevin', 'lauren', 'kevin laurence', 'admin'),
(5, 'kevin2', 'lauren', 'Hartono', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gaji`
--
ALTER TABLE `gaji`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jabatan`
--
ALTER TABLE `jabatan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD PRIMARY KEY (`nik`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
