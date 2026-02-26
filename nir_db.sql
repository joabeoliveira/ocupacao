-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: site_nir:3306
-- Tempo de geração: 26/02/2026 às 11:39
-- Versão do servidor: 9.6.0
-- Versão do PHP: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `INFORMATION_SCHEMA`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `COLUMNS`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`mysql.infoschema`@`localhost` SQL SECURITY DEFINER VIEW `COLUMNS`  AS SELECT `cat`.`name` AS `TABLE_CATALOG`, `sch`.`name` AS `TABLE_SCHEMA`, `tbl`.`name` AS `TABLE_NAME`, (`col`.`name` collate utf8mb3_tolower_ci) AS `COLUMN_NAME`, `col`.`ordinal_position` AS `ORDINAL_POSITION`, `col`.`default_value_utf8` AS `COLUMN_DEFAULT`, if((`col`.`is_nullable` = 1),'YES','NO') AS `IS_NULLABLE`, substring_index(substring_index(`col`.`column_type_utf8`,'(',1),' ',1) AS `DATA_TYPE`, internal_dd_char_length(`col`.`type`,`col`.`char_length`,`coll`.`name`,0) AS `CHARACTER_MAXIMUM_LENGTH`, internal_dd_char_length(`col`.`type`,`col`.`char_length`,`coll`.`name`,1) AS `CHARACTER_OCTET_LENGTH`, if((`col`.`numeric_precision` = 0),NULL,`col`.`numeric_precision`) AS `NUMERIC_PRECISION`, if(((`col`.`numeric_scale` = 0) and (`col`.`numeric_precision` = 0)),NULL,`col`.`numeric_scale`) AS `NUMERIC_SCALE`, `col`.`datetime_precision` AS `DATETIME_PRECISION`, (case `col`.`type` when 'MYSQL_TYPE_STRING' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_VAR_STRING' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_VARCHAR' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_TINY_BLOB' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_MEDIUM_BLOB' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_BLOB' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_VECTOR' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_LONG_BLOB' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_ENUM' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) when 'MYSQL_TYPE_SET' then if((`cs`.`name` = 'binary'),NULL,`cs`.`name`) else NULL end) AS `CHARACTER_SET_NAME`, (case `col`.`type` when 'MYSQL_TYPE_STRING' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_VAR_STRING' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_VARCHAR' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_TINY_BLOB' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_MEDIUM_BLOB' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_BLOB' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_VECTOR' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_LONG_BLOB' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_ENUM' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) when 'MYSQL_TYPE_SET' then if((`cs`.`name` = 'binary'),NULL,`coll`.`name`) else NULL end) AS `COLLATION_NAME`, `col`.`column_type_utf8` AS `COLUMN_TYPE`, `col`.`column_key` AS `COLUMN_KEY`, internal_get_dd_column_extra((`col`.`generation_expression_utf8` is null),`col`.`is_virtual`,`col`.`is_auto_increment`,`col`.`update_option`,if(length(`col`.`default_option`),true,false),`col`.`options`,`col`.`hidden`,`tbl`.`type`) AS `EXTRA`, get_dd_column_privileges(`sch`.`name`,`tbl`.`name`,`col`.`name`) AS `PRIVILEGES`, ifnull(`col`.`comment`,'') AS `COLUMN_COMMENT`, ifnull(`col`.`generation_expression_utf8`,'') AS `GENERATION_EXPRESSION`, `col`.`srs_id` AS `SRS_ID` FROM (((((`mysql`.`columns` `col` join `mysql`.`tables` `tbl` on((`col`.`table_id` = `tbl`.`id`))) join `mysql`.`schemata` `sch` on((`tbl`.`schema_id` = `sch`.`id`))) join `mysql`.`catalogs` `cat` on((`cat`.`id` = `sch`.`catalog_id`))) join `mysql`.`collations` `coll` on((`col`.`collation_id` = `coll`.`id`))) join `mysql`.`character_sets` `cs` on((`coll`.`character_set_id` = `cs`.`id`))) WHERE ((0 <> internal_get_view_warning_or_error(`sch`.`name`,`tbl`.`name`,`tbl`.`type`,`tbl`.`options`)) AND (0 <> can_access_column(`sch`.`name`,`tbl`.`name`,`col`.`name`)) AND (0 <> is_visible_dd_object(`tbl`.`hidden`,(`col`.`hidden` not in ('Visible','User')),`col`.`options`))) ;

--
-- Despejando dados para a tabela `COLUMNS`
--

INSERT INTO `COLUMNS` (`TABLE_NAME`, `COLUMN_NAME`, `DATA_TYPE`, `IS_NULLABLE`, `COLUMN_KEY`, `COLUMN_TYPE`) VALUES
('cirurgias', 'id', 'int', 'NO', 'PRI', 'int'),
('cirurgias', 'prontuario', 'int', 'NO', '', 'int'),
('cirurgias', 'paciente', 'varchar', 'NO', '', 'varchar(255)'),
('cirurgias', 'clinica_solicitante', 'varchar', 'NO', '', 'varchar(255)'),
('cirurgias', 'cirurgioes', 'varchar', 'NO', '', 'varchar(255)'),
('cirurgias', 'procedimentos', 'varchar', 'NO', '', 'varchar(255)'),
('cirurgias', 'data_internacao', 'datetime', 'NO', '', 'datetime'),
('cirurgias', 'inicio_cirurgia', 'datetime', 'NO', '', 'datetime'),
('cirurgias', 'fim_cirurgia', 'datetime', 'YES', '', 'datetime'),
('cirurgias', 'tempo_internacao_dias', 'float', 'NO', '', 'float'),
('cirurgias', 'duracao_cirurgia_min', 'float', 'YES', '', 'float'),
('historico_ocupacao_completo', 'id', 'bigint', 'NO', 'PRI', 'bigint'),
('historico_ocupacao_completo', 'data_referencia', 'date', 'NO', 'MUL', 'date'),
('historico_ocupacao_completo', 'num_enf', 'int', 'YES', '', 'int'),
('historico_ocupacao_completo', 'leito', 'int', 'YES', '', 'int'),
('historico_ocupacao_completo', 'nome_enfermaria', 'varchar', 'YES', '', 'varchar(100)'),
('historico_ocupacao_completo', 'status_leito', 'varchar', 'YES', 'MUL', 'varchar(50)'),
('historico_ocupacao_completo', 'aih_paciente', 'varchar', 'YES', '', 'varchar(50)'),
('historico_ocupacao_completo', 'cns_paciente', 'varchar', 'YES', '', 'varchar(50)'),
('historico_ocupacao_completo', 'nome_paciente', 'varchar', 'YES', 'MUL', 'varchar(255)'),
('historico_ocupacao_completo', 'sexo', 'char', 'YES', '', 'char(1)'),
('historico_ocupacao_completo', 'data_nasc', 'date', 'YES', '', 'date'),
('historico_ocupacao_completo', 'idade', 'int', 'YES', '', 'int'),
('historico_ocupacao_completo', 'data_internacao', 'datetime', 'YES', '', 'datetime'),
('historico_ocupacao_completo', 'data_internacao_leito', 'datetime', 'YES', '', 'datetime'),
('historico_ocupacao_completo', 'suspeita_covid', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'pos_covid', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'motivo_impedimento', 'varchar', 'YES', '', 'varchar(150)'),
('historico_ocupacao_completo', 'data_impedimento', 'datetime', 'YES', '', 'datetime'),
('historico_ocupacao_completo', 'data_sol_reserva', 'datetime', 'YES', '', 'datetime'),
('historico_ocupacao_completo', 'previsao_intern_reserva', 'datetime', 'YES', '', 'datetime'),
('historico_ocupacao_completo', 'acompanhamento_data_hora', 'datetime', 'YES', '', 'datetime'),
('historico_ocupacao_completo', 'prontuario', 'varchar', 'YES', '', 'varchar(50)'),
('historico_ocupacao_completo', 'cid_10', 'varchar', 'YES', '', 'varchar(50)'),
('historico_ocupacao_completo', 'codigo_ser', 'varchar', 'YES', '', 'varchar(50)'),
('historico_ocupacao_completo', 'perfil', 'varchar', 'YES', '', 'varchar(100)'),
('historico_ocupacao_completo', 'bomba_infusora', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'suporte_cirurgico', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'suporte_alimentar', 'varchar', 'YES', '', 'varchar(50)'),
('historico_ocupacao_completo', 'modo_ventilatorio', 'varchar', 'YES', '', 'varchar(100)'),
('historico_ocupacao_completo', 'observacao', 'text', 'YES', '', 'text'),
('historico_ocupacao_completo', 'cronico', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'longa_permanencia', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'situacao_motivo_permanencia', 'varchar', 'YES', '', 'varchar(255)'),
('historico_ocupacao_completo', 'gestante', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'inducao_parto', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'arbovirose', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'viabilidade_dialise_peritoneal', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'infeccao_ativa_antibiotico', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'historico_cirurgias_abdominais', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'doenca_neoplasica_avancada', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'hernia_inguinal_reparar', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'condicoes_alta_dialise', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'inserido_no_trs', 'varchar', 'YES', '', 'varchar(20)'),
('historico_ocupacao_completo', 'created_at', 'timestamp', 'YES', '', 'timestamp');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
