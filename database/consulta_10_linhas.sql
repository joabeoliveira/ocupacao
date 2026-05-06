-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: site_nir:3306
-- Tempo de geração: 30/04/2026 às 14:57
-- Versão do servidor: 9.7.0
-- Versão do PHP: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `nir`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `historico_ocupacao_completo`
--

CREATE TABLE `historico_ocupacao_completo` (
  `id` bigint NOT NULL,
  `data_referencia` date NOT NULL,
  `num_enf` int DEFAULT NULL,
  `leito` int DEFAULT NULL,
  `nome_enfermaria` varchar(100) DEFAULT NULL,
  `status_leito` varchar(50) DEFAULT NULL,
  `aih_paciente` varchar(50) DEFAULT NULL,
  `cns_paciente` varchar(50) DEFAULT NULL,
  `nome_paciente` varchar(255) DEFAULT NULL,
  `sexo` char(1) DEFAULT NULL,
  `data_nasc` date DEFAULT NULL,
  `idade` int DEFAULT NULL,
  `data_internacao` datetime DEFAULT NULL,
  `data_internacao_leito` datetime DEFAULT NULL,
  `suspeita_covid` varchar(20) DEFAULT NULL,
  `pos_covid` varchar(20) DEFAULT NULL,
  `motivo_impedimento` varchar(150) DEFAULT NULL,
  `data_impedimento` datetime DEFAULT NULL,
  `data_sol_reserva` datetime DEFAULT NULL,
  `previsao_intern_reserva` datetime DEFAULT NULL,
  `acompanhamento_data_hora` datetime DEFAULT NULL,
  `prontuario` varchar(50) DEFAULT NULL,
  `cid_10` varchar(50) DEFAULT NULL,
  `codigo_ser` varchar(50) DEFAULT NULL,
  `perfil` varchar(100) DEFAULT NULL,
  `bomba_infusora` varchar(20) DEFAULT NULL,
  `suporte_cirurgico` varchar(20) DEFAULT NULL,
  `suporte_alimentar` varchar(50) DEFAULT NULL,
  `modo_ventilatorio` varchar(100) DEFAULT NULL,
  `observacao` text,
  `cronico` varchar(20) DEFAULT NULL,
  `longa_permanencia` varchar(20) DEFAULT NULL,
  `situacao_motivo_permanencia` varchar(255) DEFAULT NULL,
  `gestante` varchar(20) DEFAULT NULL,
  `inducao_parto` varchar(20) DEFAULT NULL,
  `arbovirose` varchar(20) DEFAULT NULL,
  `viabilidade_dialise_peritoneal` varchar(20) DEFAULT NULL,
  `infeccao_ativa_antibiotico` varchar(20) DEFAULT NULL,
  `historico_cirurgias_abdominais` varchar(20) DEFAULT NULL,
  `doenca_neoplasica_avancada` varchar(20) DEFAULT NULL,
  `hernia_inguinal_reparar` varchar(20) DEFAULT NULL,
  `condicoes_alta_dialise` varchar(20) DEFAULT NULL,
  `inserido_no_trs` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Despejando dados para a tabela `historico_ocupacao_completo`
--

INSERT INTO `historico_ocupacao_completo` (`id`, `data_referencia`, `num_enf`, `leito`, `nome_enfermaria`, `status_leito`, `aih_paciente`, `cns_paciente`, `nome_paciente`, `sexo`, `data_nasc`, `idade`, `data_internacao`, `data_internacao_leito`, `suspeita_covid`, `pos_covid`, `motivo_impedimento`, `data_impedimento`, `data_sol_reserva`, `previsao_intern_reserva`, `acompanhamento_data_hora`, `prontuario`, `cid_10`, `codigo_ser`, `perfil`, `bomba_infusora`, `suporte_cirurgico`, `suporte_alimentar`, `modo_ventilatorio`, `observacao`, `cronico`, `longa_permanencia`, `situacao_motivo_permanencia`, `gestante`, `inducao_parto`, `arbovirose`, `viabilidade_dialise_peritoneal`, `infeccao_ativa_antibiotico`, `historico_cirurgias_abdominais`, `doenca_neoplasica_avancada`, `hernia_inguinal_reparar`, `condicoes_alta_dialise`, `inserido_no_trs`, `created_at`) VALUES
(1673, '2025-01-01', 113, 1, 'CIRURGIA CURTA PERMANENCIA', 'OCUPADO', '3324109976253', '709008867177018', '709008867177018', 'M', '1959-06-22', 65, '2024-12-27 11:13:00', '2024-12-27 11:13:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1674, '2025-01-01', 113, 2, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:07:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1675, '2025-01-01', 113, 3, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:07:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1676, '2025-01-01', 113, 4, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:07:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1677, '2025-01-01', 113, 5, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:08:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1678, '2025-01-01', 113, 6, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:09:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1679, '2025-01-01', 113, 7, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:09:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1680, '2025-01-01', 113, 8, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:09:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1681, '2025-01-01', 113, 9, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:09:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30'),
(1682, '2025-01-01', 113, 10, 'CIRURGIA CURTA PERMANENCIA', 'IMPEDIDO', NULL, NULL, 'IMPEDIDO-Estrutural - Manutenção Predial', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Estrutural - Manutenção Predial', '2024-12-26 19:10:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-24 16:31:30');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `historico_ocupacao_completo`
--
ALTER TABLE `historico_ocupacao_completo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_leito_dia` (`data_referencia`,`num_enf`,`leito`),
  ADD KEY `idx_data_ref` (`data_referencia`),
  ADD KEY `idx_status` (`status_leito`),
  ADD KEY `idx_paciente` (`nome_paciente`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `historico_ocupacao_completo`
--
ALTER TABLE `historico_ocupacao_completo`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=222558;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
