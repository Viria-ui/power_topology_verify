-- ==========================================
-- LINE216 自动化拓扑修复SQL脚本
-- ==========================================

<<<<<<< HEAD
-- 1. 正向修复SQL脚本
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313539','TMP00318364次母线','1799','','1010',''); -- 数据库新增设备 [TMP00313539]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314477','开关03301','1799','','1010',''); -- 数据库新增设备 [TMP00314477]（INSERT，列已对齐真实表结构）
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043886的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043886]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043540的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043540]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043527的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043527]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043532的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043532]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043538的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043538]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043539的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043539]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043534的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043534]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043537的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043537]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043889的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043889]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00046420的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00046420]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043887的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043887]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00046561的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00046561]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043535的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043535]，不改动数据库数据
=======
-- 1. 正向修复 SQL 脚本 (Forward Repair)
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314001','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314001]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314095','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314095]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314123','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314123]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314153','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314153]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000210','站房000011','1799','','1010',''); -- 数据库新增设备 [TMP00000210]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000243','站房000044','1799','','1010',''); -- 数据库新增设备 [TMP00000243]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313598','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313598]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314378','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314378]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314189','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314189]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000267','站房000068','1799','','1010',''); -- 数据库新增设备 [TMP00000267]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314434','故障指示器008','1799','','1010',''); -- 数据库新增设备 [TMP00314434]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314135','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314135]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000225','站房000026','1799','','1010',''); -- 数据库新增设备 [TMP00000225]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313590','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313590]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000255','站房000056','1799','','1010',''); -- 数据库新增设备 [TMP00000255]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314405','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314405]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313541','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313541]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313582','其他','1799','','1010',''); -- 数据库新增设备 [TMP00313582]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314117','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314117]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000256','站房000057','1799','','1010',''); -- 数据库新增设备 [TMP00000256]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314187','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314187]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314042','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314042]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314071','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314071]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314026','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314026]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314099','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314099]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000211','站房000012','1799','','1010',''); -- 数据库新增设备 [TMP00000211]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313565','故障指示器007','1799','','1010',''); -- 数据库新增设备 [TMP00313565]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314014','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314014]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314375','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314375]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314036','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314036]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314004','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314004]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314079','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314079]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314020','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314020]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000253','站房000054','1799','','1010',''); -- 数据库新增设备 [TMP00000253]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314062','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314062]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000234','站房000035','1799','','1010',''); -- 数据库新增设备 [TMP00000234]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314068','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314068]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314048','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314048]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000241','站房000042','1799','','1010',''); -- 数据库新增设备 [TMP00000241]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314179','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314179]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00048670','开关03300','1799','','1010',''); -- 数据库新增设备 [TMP00048670]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314477','开关03301','1799','','1010',''); -- 数据库新增设备 [TMP00314477]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313596','其他','1799','','1010',''); -- 数据库新增设备 [TMP00313596]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314081','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314081]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314181','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314181]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314006','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314006]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314056','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314056]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314121','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314121]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000252','站房000053','1799','','1010',''); -- 数据库新增设备 [TMP00000252]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314129','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314129]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000224','站房000025','1799','','1010',''); -- 数据库新增设备 [TMP00000224]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000258','站房000059','1799','','1010',''); -- 数据库新增设备 [TMP00000258]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000240','站房000041','1799','','1010',''); -- 数据库新增设备 [TMP00000240]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314115','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314115]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314146','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314146]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314172','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314172]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313604','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313604]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314101','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314101]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314022','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314022]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313561','其他','1799','','1010',''); -- 数据库新增设备 [TMP00313561]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313588','其他','1799','','1010',''); -- 数据库新增设备 [TMP00313588]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314158','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314158]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000257','站房000058','1799','','1010',''); -- 数据库新增设备 [TMP00000257]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314054','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314054]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313553','其他','1799','','1010',''); -- 数据库新增设备 [TMP00313553]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314028','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314028]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313584','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313584]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314089','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314089]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314137','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314137]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314087','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314087]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314141','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314141]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314012','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314012]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314093','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314093]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314410','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314410]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000242','站房000043','1799','','1010',''); -- 数据库新增设备 [TMP00000242]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314143','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314143]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314107','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314107]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314034','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314034]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000271','站房000072','1799','','1010',''); -- 数据库新增设备 [TMP00000271]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314167','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314167]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313602','其他','1799','','1010',''); -- 数据库新增设备 [TMP00313602]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314109','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314109]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314165','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314165]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000254','站房000055','1799','','1010',''); -- 数据库新增设备 [TMP00000254]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314040','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314040]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314151','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314151]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000268','站房000069','1799','','1010',''); -- 数据库新增设备 [TMP00000268]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313608','其他','1799','','1010',''); -- 数据库新增设备 [TMP00313608]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313555','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313555]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313539','TMP00318364次母线','1799','','1010',''); -- 数据库新增设备 [TMP00313539]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314073','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314073]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313619','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313619]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000259','站房000060','1799','','1010',''); -- 数据库新增设备 [TMP00000259]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314060','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314060]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314174','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314174]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('AUTO_BackGround_Layer_00ca64ad','BackGround_Layer','1799','','1010',''); -- 数据库新增设备 [AUTO_BackGround_Layer_00ca64ad]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313563','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313563]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314156','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314156]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313808','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313808]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314046','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314046]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00313805','接头','1799','','1010',''); -- 数据库新增设备 [TMP00313805]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314131','接头','1799','','1010',''); -- 数据库新增设备 [TMP00314131]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00314476','其他','1799','','1010',''); -- 数据库新增设备 [TMP00314476]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) VALUES ('TMP00000199','站房006379','1799','','1010',''); -- 数据库新增设备 [TMP00000199]（INSERT，列已对齐真实表结构）
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043713的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043713]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043604的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043604]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043588的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043588]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043708的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043708]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043724的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043724]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043592的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043592]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043601的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043601]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043534的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043534]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043706的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043706]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043590的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043590]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043694的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043694]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043873的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043873]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043537的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043537]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043891的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043891]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043852的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043852]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043853的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043853]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043859的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043859]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043875的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043875]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043889的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043889]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00046562的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00046562]，不改动数据库数据
>>>>>>> origin/main
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043753的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043753]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
<<<<<<< HEAD
-- 请在 SVG 中补画ID=TMP00046562的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00046562]，不改动数据库数据
=======
-- 请在 SVG 中补画ID=TMP00043874的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043874]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043585的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043585]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043878的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043878]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043533的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043533]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043864的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043864]，不改动数据库数据
>>>>>>> origin/main
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043891的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043891]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
<<<<<<< HEAD
-- 请在 SVG 中补画ID=TMP00043533的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043533]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043536的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043536]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043885的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043885]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043890的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043890]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043888的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043888]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043526的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043526]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043525的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043525]，不改动数据库数据
=======
-- 请在 SVG 中补画ID=TMP00043607的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043607]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043879的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043879]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043885的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043885]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043622的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043622]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043702的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043702]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043854的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043854]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043539的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043539]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043615的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043615]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00046420的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00046420]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043602的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043602]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043618的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043618]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043863的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043863]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043617的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043617]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043581的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043581]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043606的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043606]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043700的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043700]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043719的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043719]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043869的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043869]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043538的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043538]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043877的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043877]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043600的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043600]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043623的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043623]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043887的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043887]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043599的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043599]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043707的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043707]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043696的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043696]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043583的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043583]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043723的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043723]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043857的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043857]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043612的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043612]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043851的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043851]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043865的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043865]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043535的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043535]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043714的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043714]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043888的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043888]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043868的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043868]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043872的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043872]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043754的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043754]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043608的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043608]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043587的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043587]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043709的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043709]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043598的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043598]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043697的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043697]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043849的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043849]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043616的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043616]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043881的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043881]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043525的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043525]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043596的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043596]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043751的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043751]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043594的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043594]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043856的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043856]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043610的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043610]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00046561的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00046561]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043698的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043698]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043620的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043620]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043705的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043705]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043605的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043605]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043718的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043718]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043717的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043717]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043619的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043619]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043584的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043584]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043597的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043597]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043582的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043582]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043871的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043871]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043704的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043704]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043722的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043722]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043862的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043862]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043860的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043860]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043586的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043586]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043715的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043715]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043609的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043609]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043848的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043848]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043613的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043613]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043540的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043540]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043712的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043712]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043621的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043621]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043595的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043595]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043701的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043701]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043855的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043855]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043886的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043886]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043720的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043720]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043890的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043890]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043536的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043536]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043699的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043699]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043750的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043750]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043858的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043858]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043695的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043695]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043611的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043611]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043749的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043749]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043526的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043526]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043861的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043861]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043725的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043725]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043591的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043591]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043703的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043703]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043593的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043593]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043589的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043589]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043870的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043870]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043603的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043603]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043614的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043614]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043850的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043850]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043721的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043721]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043866的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043866]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043880的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043880]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043532的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043532]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043527的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043527]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043711的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043711]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043716的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043716]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043876的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043876]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043710的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043710]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043867的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043867]，不改动数据库数据
-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。
-- 请在 SVG 中补画ID=TMP00043755的图层图元以及iec:PSR_Ref元数据标注。 -- SVG侧补画图元[TMP00043755]，不改动数据库数据
>>>>>>> origin/main
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_313565_046158','SVG物理连通补录','TMP00313565','1010'); -- 模型新增物理边 [TMP00313565 -> TMP00046158]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_313539_048670','SVG物理连通补录','TMP00313539','1010'); -- 模型新增物理边 [TMP00313539 -> TMP00048670]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_048670_313541','SVG物理连通补录','TMP00048670','1010'); -- 模型新增物理边 [TMP00048670 -> TMP00313541]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_313553_046027','SVG物理连通补录','TMP00313553','1010'); -- 模型新增物理边 [TMP00313553 -> TMP00046027]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_313561_046027','SVG物理连通补录','TMP00313561','1010'); -- 模型新增物理边 [TMP00313561 -> TMP00046027]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044532_313588','SVG物理连通补录','TMP00044532','1010'); -- 模型新增物理边 [TMP00044532 -> TMP00313588]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044553_313608','SVG物理连通补录','TMP00044553','1010'); -- 模型新增物理边 [TMP00044553 -> TMP00313608]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_046026_313582','SVG物理连通补录','TMP00046026','1010'); -- 模型新增物理边 [TMP00046026 -> TMP00313582]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_313608_046152','SVG物理连通补录','TMP00313608','1010'); -- 模型新增物理边 [TMP00313608 -> TMP00046152]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_313602_046151','SVG物理连通补录','TMP00313602','1010'); -- 模型新增物理边 [TMP00313602 -> TMP00046151]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044596_000224','SVG物理连通补录','TMP00044596','1010'); -- 模型新增物理边 [TMP00044596 -> TMP00000224]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_000224_046150','SVG物理连通补录','TMP00000224','1010'); -- 模型新增物理边 [TMP00000224 -> TMP00046150]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_046145_314001','SVG物理连通补录','TMP00046145','1010'); -- 模型新增物理边 [TMP00046145 -> TMP00314001]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044538_314001','SVG物理连通补录','TMP00044538','1010'); -- 模型新增物理边 [TMP00044538 -> TMP00314001]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044538_314004','SVG物理连通补录','TMP00044538','1010'); -- 模型新增物理边 [TMP00044538 -> TMP00314004]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044529_314012','SVG物理连通补录','TMP00044529','1010'); -- 模型新增物理边 [TMP00044529 -> TMP00314012]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314012_045950','SVG物理连通补录','TMP00314012','1010'); -- 模型新增物理边 [TMP00314012 -> TMP00045950]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314020_045950','SVG物理连通补录','TMP00314020','1010'); -- 模型新增物理边 [TMP00314020 -> TMP00045950]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044529_314020','SVG物理连通补录','TMP00044529','1010'); -- 模型新增物理边 [TMP00044529 -> TMP00314020]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044515_314026','SVG物理连通补录','TMP00044515','1010'); -- 模型新增物理边 [TMP00044515 -> TMP00314026]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314026_045949','SVG物理连通补录','TMP00314026','1010'); -- 模型新增物理边 [TMP00314026 -> TMP00045949]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044515_314034','SVG物理连通补录','TMP00044515','1010'); -- 模型新增物理边 [TMP00044515 -> TMP00314034]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044516_314040','SVG物理连通补录','TMP00044516','1010'); -- 模型新增物理边 [TMP00044516 -> TMP00314040]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314040_045948','SVG物理连通补录','TMP00314040','1010'); -- 模型新增物理边 [TMP00314040 -> TMP00045948]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044516_314046','SVG物理连通补录','TMP00044516','1010'); -- 模型新增物理边 [TMP00044516 -> TMP00314046]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044517_314054','SVG物理连通补录','TMP00044517','1010'); -- 模型新增物理边 [TMP00044517 -> TMP00314054]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314054_045947','SVG物理连通补录','TMP00314054','1010'); -- 模型新增物理边 [TMP00314054 -> TMP00045947]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044517_314060','SVG物理连通补录','TMP00044517','1010'); -- 模型新增物理边 [TMP00044517 -> TMP00314060]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044518_314068','SVG物理连通补录','TMP00044518','1010'); -- 模型新增物理边 [TMP00044518 -> TMP00314068]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044518_314071','SVG物理连通补录','TMP00044518','1010'); -- 模型新增物理边 [TMP00044518 -> TMP00314071]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044519_314079','SVG物理连通补录','TMP00044519','1010'); -- 模型新增物理边 [TMP00044519 -> TMP00314079]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314079_045945','SVG物理连通补录','TMP00314079','1010'); -- 模型新增物理边 [TMP00314079 -> TMP00045945]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044519_314087','SVG物理连通补录','TMP00044519','1010'); -- 模型新增物理边 [TMP00044519 -> TMP00314087]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_046415_314093','SVG物理连通补录','TMP00046415','1010'); -- 模型新增物理边 [TMP00046415 -> TMP00314093]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314093_045944','SVG物理连通补录','TMP00314093','1010'); -- 模型新增物理边 [TMP00314093 -> TMP00045944]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044554_314099','SVG物理连通补录','TMP00044554','1010'); -- 模型新增物理边 [TMP00044554 -> TMP00314099]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044562_314107','SVG物理连通补录','TMP00044562','1010'); -- 模型新增物理边 [TMP00044562 -> TMP00314107]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314107_045943','SVG物理连通补录','TMP00314107','1010'); -- 模型新增物理边 [TMP00314107 -> TMP00045943]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044562_314115','SVG物理连通补录','TMP00044562','1010'); -- 模型新增物理边 [TMP00044562 -> TMP00314115]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044563_314121','SVG物理连通补录','TMP00044563','1010'); -- 模型新增物理边 [TMP00044563 -> TMP00314121]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314121_045942','SVG物理连通补录','TMP00314121','1010'); -- 模型新增物理边 [TMP00314121 -> TMP00045942]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044563_314129','SVG物理连通补录','TMP00044563','1010'); -- 模型新增物理边 [TMP00044563 -> TMP00314129]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044550_314146','SVG物理连通补录','TMP00044550','1010'); -- 模型新增物理边 [TMP00044550 -> TMP00314146]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044550_314141','SVG物理连通补录','TMP00044550','1010'); -- 模型新增物理边 [TMP00044550 -> TMP00314141]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044530_314151','SVG物理连通补录','TMP00044530','1010'); -- 模型新增物理边 [TMP00044530 -> TMP00314151]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044530_314156','SVG物理连通补录','TMP00044530','1010'); -- 模型新增物理边 [TMP00044530 -> TMP00314156]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044520_314165','SVG物理连通补录','TMP00044520','1010'); -- 模型新增物理边 [TMP00044520 -> TMP00314165]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044520_314172','SVG物理连通补录','TMP00044520','1010'); -- 模型新增物理边 [TMP00044520 -> TMP00314172]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044577_314179','SVG物理连通补录','TMP00044577','1010'); -- 模型新增物理边 [TMP00044577 -> TMP00314179]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_314179_045938','SVG物理连通补录','TMP00314179','1010'); -- 模型新增物理边 [TMP00314179 -> TMP00045938]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_044577_314187','SVG物理连通补录','TMP00044577','1010'); -- 模型新增物理边 [TMP00044577 -> TMP00314187]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_045939_314172','SVG物理连通补录','TMP00045939','1010'); -- 模型新增物理边 [TMP00045939 -> TMP00314172]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_045940_314156','SVG物理连通补录','TMP00045940','1010'); -- 模型新增物理边 [TMP00045940 -> TMP00314156]（INSERT，列已对齐真实表结构）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) VALUES ('LN_046112_314146','SVG物理连通补录','TMP00046112','1010'); -- 模型新增物理边 [TMP00046112 -> TMP00314146]（INSERT，列已对齐真实表结构）
<<<<<<< HEAD
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00003760）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003760）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003763）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00003766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00003767）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003776）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003781）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003782）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003784）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003808）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003809）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003810）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003811）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003823）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003824）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003825）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003826）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003827）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003859）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003860）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00003861）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003861）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00003956）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003956）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00003957）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003957）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003958）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00003960）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003960）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00003970）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003970）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00003974）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003974）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003980）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00003980）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003991）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00003993）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003995）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00003996）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00003997）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004020）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004021）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004022）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004023）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004024）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004025）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004029）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004031）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004032）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004035）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004035）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004047）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004048）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004049）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004050）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004052）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004055）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004057）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004058）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004059）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004060）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004062）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004063）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004064）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004065）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004066）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004067）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004071）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004072）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004073）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004074）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004076）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004077）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004078）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004079）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004080）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004083）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004084）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004085）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004086）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004087）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004088）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004091）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004092）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004093）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004094）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004095）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004096）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004097）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004098）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004098）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004099）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004100）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004101）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004101）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004102）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004103）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004103）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004105）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004105）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004106）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004107）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004108）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004109）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004110）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004111）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004112）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004113）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004115）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004116）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004117）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004118）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004119）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004120）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004122）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004125）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004140）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004141）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004142）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004143）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004144）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004145）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004146）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004146）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004147）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004148）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004149）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004150）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004151）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004152）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004153）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004153）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004154）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004154）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004156）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004158）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004160）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004161）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004162）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004162）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004164）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004165）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004166）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004167）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004169）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004170）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004170）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004172）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004173）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004174）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004175）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004176）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004177）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004178）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004179）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004213）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004214）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004214）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004215）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004216）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004216）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004217）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004217）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004218）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004218）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004220）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004231）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004233）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004234）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004234）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004236）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004237）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004238）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004241）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004242）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004249）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004273）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004274）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004347）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004348）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004349）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004349）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004350）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004351）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004351）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004352）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004352）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004353）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004353）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004355）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00004364）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00004365）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004367）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00004367）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00004374）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00004375）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004379）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004382）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004422）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004422）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004433）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004446）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004477）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004478）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004480）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004483）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00004489）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004493）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004520）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004521）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004522）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004523）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004524）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004532）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004533）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004537）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004538）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004539）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004555）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004556）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004577）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004598）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004599）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004600）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004603）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004604）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004604）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004609）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004610）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004611）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004612）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004692）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004693）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004694）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004695）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00004698）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004699）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004731）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004735）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004738）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004739）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004747）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004748）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00004748）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004751）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004759）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004764）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004768）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004825）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004826）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004828）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004828）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004830）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004830）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004831）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004831）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004832）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004832）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004834）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004834）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004834）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004835）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004835）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004837）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004839）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004840）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004841）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004844）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004846）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004847）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004864）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004884）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004886）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00004887）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004887）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00004887）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004889）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004890）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004891）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004892）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004906）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004907）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004915）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004968）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004973）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004974）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004976）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004977）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004990）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004991）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004996）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004997）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00004998）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00004999）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005002）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005019）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005020）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005020）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005031）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00005043）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00005044）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005053）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00005053）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00005128）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00005130）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00005131）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005132）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00005135）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00005137）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00005141）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00005143）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00005144）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00005145）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005146）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005180）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005180）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005184）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005188）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005189）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005190）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005197）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005199）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005202）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005204）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005205）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005207）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005208）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005209）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005211）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005225）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005289）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005289）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005338）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005358）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005358）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005362）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00005363）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005364）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005375）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005376）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005377）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005378）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005380）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005381）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005382）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005384）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005399）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005401）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005402）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005408）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005409）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005411）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005412）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005415）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005416）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005417）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005418）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005419）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005420）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005421）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005422）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005426）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005433）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005434）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005435）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005436）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005437）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005438）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005439）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005440）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005443）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005444）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005445）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005446）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005454）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005466）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005467）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005467）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005475）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005477）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005480）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005482）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005483）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005532）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005536）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005544）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005586）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005586）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005589）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005600）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005602）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005603）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005604）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005605）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005606）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005609）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005615）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005685）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005686）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00005705）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005705）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005782）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005784）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005785）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005803）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005879）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005885）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005894）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005895）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005900）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005907）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005908）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00005919）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00005920）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00005922）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005923）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005924）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00005928）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005936）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005945）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005947）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005965）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005966）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005969）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005972）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00005975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006015）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006038）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006059）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006060）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006065）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006071）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006074）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006088）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006090）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006098）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006099）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006100）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006101）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006102）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006104）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006106）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006107）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006108）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006156）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00006162）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00006163）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00006164）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00006165）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006220）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006221）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006222）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006223）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006262）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006263）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006362）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006369）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00006369）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00006371）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006371）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00006371）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00006376）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006376）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00006376）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006424）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006430）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006431）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006432）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006474）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006476）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006477）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00006503）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006503）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006506）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006508）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006540）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00006547）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006548）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006552）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006569）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00006570）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00006571）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00006573）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00006574）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00006576）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00006578）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006580）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00006593）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006646）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006669）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006688）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006695）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00006695）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00006766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006767）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00006785）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006785）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006817）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00006818）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006818）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006819）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006820）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00006821）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00007028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00007030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00007031）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007032）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00007067）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007067）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00007072）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007072）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007181）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00007338）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007338）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007384）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007448）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007449）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00007450）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007453）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007477）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007488）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007490）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007654）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007655）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007656）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007657）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007663）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007664）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007667）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007669）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007670）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007789）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007790）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007796）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007810）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007812）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007813）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007814）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007816）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007817）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007819）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007820）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007821）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007824）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007826）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007827）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007828）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007830）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007831）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007833）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007834）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007838）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00007839）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007839）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007881）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007882）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007885）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007886）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00007887）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007888）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007940）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007948）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007950）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007953）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00007969）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007970）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00007976）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008015）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008018）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008021）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008036）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008042）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008069）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008076）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008082）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008084）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008088）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008089）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008090）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008092）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008093）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008097）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008098）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008099）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008102）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008103）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008104）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008106）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008108）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008110）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008111）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008112）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008117）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008118）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008119）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008120）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008121）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008122）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008123）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008123）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008124）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008124）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00008125）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008126）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008127）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008128）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008129）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008130）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00008134）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008136）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00008139）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008140）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00008142）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008147）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008151）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008153）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008154）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008158）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008160）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008177）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008181）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008183）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008184）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008185）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008186）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008188）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008195）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008196）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008199）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008200）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008201）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008201）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008202）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008203）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008204）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008205）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008206）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008207）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008208）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008211）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008213）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008214）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008215）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008216）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008217）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008220）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008221）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008222）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008223）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008224）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008225）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008228）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008229）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008230）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008231）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008232）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008233）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008237）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008238）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008240）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008241）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008244）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008245）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008246）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008247）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008248）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008250）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008251）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008252）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008253）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008253）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008255）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008256）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008265）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008271）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008273）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008299）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008309）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008313）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008316）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008320）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008321）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00008322）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008325）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008326）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008352）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008353）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008354）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008355）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008356）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008358）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008360）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008365）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008389）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008395）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008431）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008432）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008433）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008434）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008436）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008437）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008438）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008443）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008448）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008450）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008454）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008455）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008459）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008460）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00008460）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008461）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008462）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008462）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008463）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008464）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008464）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008467）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008469）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008472）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008491）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008492）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008493）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008495）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008497）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008498）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008499）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008500）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008501）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008502）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008503）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008508）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008509）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008510）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008511）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008512）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008512）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008513）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008514）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008524）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008528）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008530）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008531）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008533）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008543）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008543）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008546）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008549）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008647）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008654）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008655）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008657）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008659）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008660）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008663）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008664）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008668）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008669）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008670）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008671）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008672）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008673）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008674）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008675）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008676）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008677）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008680）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008680）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00008680）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008681）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008682）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008683）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008696）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008698）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008699）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008702）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008703）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008706）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008709）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008713）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008714）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008715）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008721）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008722）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008729）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008731）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008734）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008737）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008746）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008749）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008756）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008790）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008791）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008793）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008802）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008802）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008803）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008804）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008805）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008806）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008807）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008807）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008817）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008820）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008821）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008822）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008823）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008828）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008831）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008835）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008837）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008838）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008839）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008906）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008917）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008919）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008920）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008951）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008955）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008956）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008957）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008961）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008964）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008966）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008968）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008981）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00008982）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00008984）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00008984）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008987）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00008988）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008991）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00008992）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00008999）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009000）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009001）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009003）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009005）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009012）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009012）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009017）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009017）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009024）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009029）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009032）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009038）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009040）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009043）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009044）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009052）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009054）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009056）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009057）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009061）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009065）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009067）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009068）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009070）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009071）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009072）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009073）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009074）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009075）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009086）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009088）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009093）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009096）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009101）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009105）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009126）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009128）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009130）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009132）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009144）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009144）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009169）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009170）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009199）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009201）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009204）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009217）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009218）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009219）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009222）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009223）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009223）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009225）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009225）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009227）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009227）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009228）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009228）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009236）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009237）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009238）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009245）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009247）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009248）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009252）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009255）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009293）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009293）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009299）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009300）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009301）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009302）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009306）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009307）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009308）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009309）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009323）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009326）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009327）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009328）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009336）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009341）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009341）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009342）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009342）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009343）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009344）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009345）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009356）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009358）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009359）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009360）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009360）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009361）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009368）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009372）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009373）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009374）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009386）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009410）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009416）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009419）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009431）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009432）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009433）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009434）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009445）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009474）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009480）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00009505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009517）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009526）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009527）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009528）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009530）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009533）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009558）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009562）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009570）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009572）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009584）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009589）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009590）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009591）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009593）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00009601）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00009602）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00009604）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009605）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009606）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009607）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009608）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009609）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009610）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009611）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009612）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009613）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009616）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009617）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009626）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009626）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009627）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009628）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009628）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009629）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009630）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009631）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009632）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009633）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009634）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009635）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009636）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009637）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009638）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009645）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009646）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009647）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009668）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009679）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009714）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009726）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009729）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009733）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00009736）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009737）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009748）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009750）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009751）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009752）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009753）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009754）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009756）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009757）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009758）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009759）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009760）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009760）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009761）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00009761）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009762）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00009765）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009774）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009779）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009793）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009817）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009822）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009899）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009909）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009909）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009911）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009912）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009913）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009930）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009931）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009945）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00009992）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009992）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009994）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009995）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009996）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00009998）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00009999）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010013）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010022）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010023）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010025）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010031）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010032）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010035）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010036）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010037）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010037）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010042）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010042）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010043）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010044）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010045）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010046）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010058）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010063）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010082）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010083）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010084）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010085）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010086）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010087）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010091）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010092）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010100）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010102）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010103）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010104）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010109）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010122）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010123）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010134）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010136）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010136）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010137）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010139）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010139）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010140）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010142）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010143）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010143）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00010144）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010146）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010146）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010148）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010151）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010153）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010156）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010156）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010161）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010161）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010162）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010163）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010164）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010165）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010166）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010166）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010173）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010173）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010177）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010179）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010180）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010190）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010191）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010193）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010194）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010195）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010195）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010198）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010199）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010201）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010203）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010205）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010207）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010210）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010211）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010216）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010221）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010226）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010229）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010232）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010233）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010234）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010236）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010237）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010238）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010238）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010240）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010242）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010242）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010243）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00010253）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010254）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010254）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010255）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010256）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010256）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010257）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010258）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010260）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010261）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010262）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010263）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010265）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010265）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010270）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010271）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010274）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010276）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010278）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010281）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010289）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010296）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010297）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010298）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010299）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010300）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010301）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010302）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010304）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010309）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010311）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010312）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010313）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010313）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010314）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010315）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010330）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010332）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010347）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010348）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010349）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010350）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010354）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010354）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010356）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010363）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010364）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010365）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010366）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010368）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010373）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010381）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010384）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010390）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010411）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010420）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010433）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010436）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010437）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010440）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010441）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010442）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010443）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010445）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010447）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010448）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010449）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010449）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010452）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010454）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010455）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010459）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010464）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010467）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010469）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010484）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010485）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010488）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010491）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010494）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010506）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010507）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010508）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010509）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010510）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010512）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010513）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010514）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010515）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010517）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010518）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010523）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010524）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010525）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010526）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010527）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010530）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010533）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010534）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010535）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010555）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010557）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010558）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010560）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010564）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010566）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010567）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010570）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010571）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010572）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010573）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010578）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010584）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010584）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010585）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010585）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010587）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00010607）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010608）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010609）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010610）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010611）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010612）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010613）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010614）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010616）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010620）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010621）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010623）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010626）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010627）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010627）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010681）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010682）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010683）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010683）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010685）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010686）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010686）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010688）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010688）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010689）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010689）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010690）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010691）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010692）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010695）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010698）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010704）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010707）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010713）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010714）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010716）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010718）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010721）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010723）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010724）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010725）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010730）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010731）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010732）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010735）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00010740）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010741）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010744）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00010745）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010754）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010755）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010756）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010762）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010763）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010764）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010768）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010769）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010772）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010773）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010774）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010774）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010775）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010776）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010777）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010778）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010781）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010781）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010784）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010785）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010790）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010792）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010793）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010795）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010796）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010798）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010811）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010821）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010826）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010832）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010835）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010838）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010840）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010841）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010842）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010863）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010869）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010879）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010894）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010895）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00010897）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010897）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00010897）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010903）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010903）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010910）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010914）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010918）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010924）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010926）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010927）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010929）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010929）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010932）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010933）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010934）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010935）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010935）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010936）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010937）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010937）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010939）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010940）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010943）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010946）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010947）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010952）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010955）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010955）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010957）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010957）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010958）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010960）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010961）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010966）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010970）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010974）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010977）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010978）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010979）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010983）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010988）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010989）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00010991）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00010991）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010992）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010993）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00010994）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00010994）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00010997）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011001）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011001）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011002）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011003）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011004）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011005）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011006）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011007）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011007）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011010）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011011）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011013）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011014）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011017）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011018）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011019）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011031）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011035）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011036）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011039）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011040）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011044）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011045）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011047）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011048）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011052）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011053）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011054）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011056）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011057）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011058）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011061）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011062）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011064）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011065）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011068）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011069）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011070）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011078）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011079）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011080）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011081）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011082）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011083）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011084）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011085）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011086）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011087）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011088）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011089）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011090）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011091）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011092）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011093）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011095）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011099）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011100）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011103）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011104）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011105）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011106）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011107）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011109）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011109）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011129）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011131）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011133）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011137）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011137）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011143）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011163）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011164）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011164）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011165）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011165）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011166）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011167）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011169）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011171）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011172）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011173）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011175）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011177）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011178）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011178）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011179）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011179）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011181）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011183）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011185）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011185）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011186）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011189）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011190）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011191）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011194）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011195）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011199）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011200）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011204）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00011207）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011207）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011208）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011209）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011210）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011211）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011213）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011214）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011217）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011218）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011219）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011221）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011222）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011226）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011227）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011231）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011232）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011238）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011240）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011242）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011244）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011245）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011246）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011256）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011264）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011266）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011278）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011281）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011285）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011294）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011294）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011295）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011296）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011297）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011302）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011302）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011303）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011304）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011305）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011306）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011309）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011310）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011312）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011313）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011316）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011325）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011327）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011329）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011333）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011334）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011335）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011336）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011337）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011340）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011351）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011353）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011354）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011355）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011356）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011358）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011361）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011363）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011364）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011366）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011367）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011370）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011371）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011372）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011373）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011374）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011377）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011380）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011398）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00011398）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011400）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011400）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011403）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011403）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011404）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011405）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011405）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011406）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011406）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011407）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011407）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011410）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011410）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011411）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011414）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011415）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011417）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011418）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011418）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011423）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011423）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011424）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011424）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011427）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011427）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011432）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011432）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011435）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011435）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011436）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011437）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011439）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011441）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011442）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011442）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011445）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011445）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011447）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011451）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011452）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011452）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011453）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011453）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011454）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011479）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011480）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011481）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011482）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011483）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011486）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011487）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011491）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011494）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011497）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011497）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011499）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011502）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011502）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011503）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011503）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011504）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011504）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011506）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011507）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011507）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011509）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011509）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011510）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011511）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011512）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011513）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011514）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011514）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011522）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011523）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011524）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011528）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011529）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011530）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011536）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011545）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011547）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011548）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011550）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011553）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011555）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011560）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011561）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011563）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011573）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011577）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011578）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011579）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011580）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011581）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011582）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011583）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011583）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011584）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011585）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011586）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011587）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011588）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011599）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011600）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011601）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00011633）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011634）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011636）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011639）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011642）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011645）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011647）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011656）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011657）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011658）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011659）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011660）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011661）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011666）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011670）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011671）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011674）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011678）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011680）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011684）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011691）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011692）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011694）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011695）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011696）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011697）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011697）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011702）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011703）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011705）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011707）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011708）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011709）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011710）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011711）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011712）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011715）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011716）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011719）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011721）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011722）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011723）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011726）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011732）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011733）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011734）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011736）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011743）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011745）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011746）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011754）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011755）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011756）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00011757）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011757）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011759）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011761）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011763）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011769）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011770）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011775）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011778）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011781）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011784）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011785）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011788）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011789）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011790）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011791）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011791）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011792）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011793）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011793）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011794）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011795）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011796）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011797）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011797）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011798）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011799）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011799）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011800）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011801）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011801）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011802）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011803）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011804）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011807）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011811）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011812）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011813）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011814）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011815）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011816）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011817）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011820）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011831）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011832）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00011836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011837）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011845）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011848）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011849）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011852）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011854）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011855）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011857）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011858）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011859）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011860）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011861）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011862）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011863）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011865）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011866）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011867）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011867）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011869）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011873）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011879）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011880）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011881）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011882）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011883）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011890）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011896）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011900）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011904）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011910）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011911）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011912）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011916）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011917）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00011918）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011920）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011923）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011927）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011939）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011944）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00011952）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011956）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011958）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011959）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011960）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011962）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011964）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011966）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011968）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011969）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011972）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011973）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011974）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011979）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011980）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011985）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011988）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011993）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011995）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00011996）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00011999）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012001）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012003）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012004）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012005）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012006）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012007）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012008）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012009）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012021）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012022）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012023）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012024）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012029）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012037）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012038）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012040）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012042）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012046）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012047）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012053）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012055）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012062）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012067）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012070）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012071）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00012078）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00012080）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012089）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012091）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012094）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012095）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012097）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012099）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012103）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012105）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012107）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012108）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012109）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012111）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012113）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012114）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012115）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012118）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012122）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012126）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012127）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012128）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012130）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012132）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012134）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012135）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012137）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012139）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012140）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012153）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012155）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012156）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012158）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012160）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012161）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012162）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012163）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012170）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012171）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012176）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012177）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012185）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012186）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012198）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012200）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012202）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012208）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012209）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012210）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012211）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012212）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012213）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012214）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012223）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012226）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012227）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012228）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012229）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012230）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012231）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012232）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012234）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012236）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012237）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012238）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012240）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012243）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012244）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012245）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012247）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012248）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012249）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00012250）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012253）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012254）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012256）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012260）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012264）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012265）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012266）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012268）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012269）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012274）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012277）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012292）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012294）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012296）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012299）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012308）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012317）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012321）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012322）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012324）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012340）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012341）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012346）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012347）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012352）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012353）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012358）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012359）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012361）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012364）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012365）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012366）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012368）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012369）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012370）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012372）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012373）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012374）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012375）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012376）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012377）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012378）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012379）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012380）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012383）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012384）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012386）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012387）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012388）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012389）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012390）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012391）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012392）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012393）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012394）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012404）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012405）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012406）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012408）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012409）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012410）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012411）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012412）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012413）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012414）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012442）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012445）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012451）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012452）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012455）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012457）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012525）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012527）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012530）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012533）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012535）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012538）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012539）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012540）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012544）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012553）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012556）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012557）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012559）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012561）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012563）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012570）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012575）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012578）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012579）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012580）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012586）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012587）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012589）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012591）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012594）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012595）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012598）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012605）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012606）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012608）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012609）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012611）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012613）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012616）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012617）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012619）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012641）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012642）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012643）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012645）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012646）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012647）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012648）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012650）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012655）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012658）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012659）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012663）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012672）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012673）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012674）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012676）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012679）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012680）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012683）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012686）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012687）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012689）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012691）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012694）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012695）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012696）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012699）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012700）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012701）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012702）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012703）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012704）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012707）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012708）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012709）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012712）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012713）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012714）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012715）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012716）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012717）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012718）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012719）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012720）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012721）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012722）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012724）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012725）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012726）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012729）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012730）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012731）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012732）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012733）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012735）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012736）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012737）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012740）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012742）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012743）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012744）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012745）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012746）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012748）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012749）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012750）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012751）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012752）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012755）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012757）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012760）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012763）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012771）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012774）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012775）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012776）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012777）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012778）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012779）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012780）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012782）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012786）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012787）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012795）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012796）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012799）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012804）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012806）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012808）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012809）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012812）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012813）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012815）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012816）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012819）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012822）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012823）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012824）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012827）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012828）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012830）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012833）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012838）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012840）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012842）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012843）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012844）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012846）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012848）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012850）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012856）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012857）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012858）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012866）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012872）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012874）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012878）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012880）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012883）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012885）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00012903）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012905）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012906）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012907）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012908）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012909）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012910）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012911）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012913）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012914）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012916）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012924）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012925）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00012927）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012928）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00012930）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012932）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012933）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012935）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00012936）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012940）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012941）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012944）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012945）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012947）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012948）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012952）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012953）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012956）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012961）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012962）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012963）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012965）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012966）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012968）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012969）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012971）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012977）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012978）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012979）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00012982）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012983）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012984）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012987）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012990）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00012997）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013004）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013011）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013014）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00013033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013036）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013037）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013038）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013039）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013040）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013042）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013043）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013069）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013070）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013071）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013088）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013089）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013091）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013095）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013100）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013102）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013103）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013106）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013107）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013109）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013113）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013115）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013116）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013131）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013133）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013137）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013138）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013139）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013140）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013141）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013144）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013148）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013150）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013151）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013152）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013156）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013160）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013162）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013165）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013167）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013169）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013180）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013182）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013191）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013198）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013199）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013209）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013214）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013223）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013225）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013231）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013234）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013240）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013243）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013246）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013249）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013250）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013253）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00013259）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013260）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013261）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013262）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013263）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013268）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013284）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013293）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013295）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013296）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013298）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013299）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013302）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013311）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013312）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013314）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013326）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013327）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013334）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013335）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013336）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013337）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013338）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013339）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013341）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013343）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013344）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013345）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013348）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013353）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013360）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013361）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013362）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013363）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013370）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013371）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013375）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013387）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013388）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013389）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013390）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013392）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013394）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013395）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013397）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013398）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013401）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013402）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013403）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013408）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013413）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013415）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013416）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013418）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013420）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013422）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013424）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013428）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013430）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013431）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013440）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013444）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013451）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013454）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013465）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013466）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013489）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013490）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013495）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013496）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013497）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013499）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013501）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013502）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013503）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013504）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013506）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013509）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013513）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013515）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013516）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013517）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013518）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013520）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013521）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013529）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013537）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013578）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013579）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013580）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013604）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013606）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013619）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013623）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013625）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013626）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013629）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013630）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013633）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013634）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013635）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013636）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013638）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013642）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013643）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013649）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013651）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013652）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013653）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013663）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013665）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013666）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013668）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013670）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013671）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013672）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013673）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013674）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013676）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013677）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013680）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013682）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013684）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013685）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013688）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013689）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013693）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013694）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013698）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013699）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013702）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013707）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013708）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013709）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013710）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013712）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013713）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013714）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013716）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013719）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013721）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013722）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013725）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013727）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013728）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013729）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013732）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013734）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013739）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013745）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013746）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013747）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013752）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013753）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013756）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013757）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013759）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013760）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013761）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013764）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013767）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013771）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013772）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013773）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013780）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013783）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013787）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013796）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013804）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013805）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013807）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013808）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013809）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013811）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013813）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013814）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013815）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013823）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013824）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013825）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013826）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013828）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013829）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013830）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013834）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013835）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013840）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013842）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013847）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013852）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013853）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013854）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013855）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013856）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013857）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013859）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013861）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013871）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013875）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013877）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00013880）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013882）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013883）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013885）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013886）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013890）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013893）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013894）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013897）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013899）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013901）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013902）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013911）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013914）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013915）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013917）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013918）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013925）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013926）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013927）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013930）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013938）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013939）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013941）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013942）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013943）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013945）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013946）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00013947）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013948）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013950）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00013951）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013952）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013953）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00013954）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013955）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00013958）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013959）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013961）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00013962）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013964）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013965）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013966）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013968）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013974）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013977）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013978）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013979）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00013981）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013983）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00013984）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014001）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014002）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014002）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014004）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014005）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014007）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014024）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014025）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014034）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014036）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014038）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014042）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014043）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014048）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014050）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014053）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014054）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014055）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014057）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014058）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014060）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014064）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014065）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014068）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014071）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014072）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014074）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014076）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014077）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014079）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014080）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014083）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014090）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014091）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014092）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014094）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014095）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014096）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014097）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014098）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014104）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014105）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014108）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014110）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014117）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014119）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014120）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014121）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014126）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014127）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014129）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014133）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014141）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014142）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014144）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014145）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014146）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014147）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014148）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014149）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014150）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014153）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014154）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014155）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014156）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014158）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014159）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014166）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014168）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014172）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014173）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014174）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014175）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014176）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014181）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014183）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014185）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014186）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014190）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014191）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014193）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014194）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014195）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014201）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014203）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014207）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014208）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014215）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014218）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014220）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014221）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014223）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014234）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014237）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014242）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014243）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014245）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014249）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014250）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014254）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014258）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014264）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014267）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014268）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014269）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014272）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014273）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014274）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014275）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014275）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014277）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014282）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014283）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014285）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014287）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014288）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014289）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014291）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014292）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014293）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014294）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014295）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014296）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014300）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014302）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014303）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014305）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014305）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014306）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014311）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014314）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014315）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014316）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014326）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014327）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014332）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014335）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014340）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014342）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014343）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014344）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014346）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014351）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014352）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014354）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014356）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014357）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014358）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014360）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014361）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014365）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014366）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014368）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014371）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014373）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014374）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014375）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014376）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014378）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014380）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014383）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014389）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014392）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014395）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014396）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014397）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014398）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014399）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014400）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014401）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014403）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014405）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014406）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014407）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014407）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014409）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014410）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014412）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014413）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014415）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014416）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014417）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014419）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014421）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014426）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014427）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014428）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014431）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014433）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014434）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014436）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014439）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014440）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014442）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014443）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014445）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014446）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014448）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014449）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014451）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014452）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014453）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014455）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014459）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014461）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014464）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014465）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014466）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014467）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014468）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014469）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014470）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014477）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014479）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014482）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014484）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014485）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014486）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014490）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014495）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014497）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014500）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014505）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014506）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014509）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014510）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014512）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014515）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014517）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014519）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014523）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014530）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014550）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014551）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014552）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014553）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014556）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014559）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014562）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014565）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014568）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014572）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014575）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014582）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014589）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014591）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014597）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014602）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014604）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014607）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014608）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014611）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014618）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014620）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014621）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014625）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014641）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014642）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014647）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014649）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014656）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014657）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014660）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014661）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014665）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014666）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014670）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014671）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014672）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014673）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014677）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014679）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014690）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014691）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00014699）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E07（设备=TMP00014701）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014704）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014705）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014706）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014707）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014708）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014709）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014712）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014713）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014715）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014716）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014717）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014721）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014725）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00014726）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014729）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014730）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014732）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014734）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014735）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014737）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014742）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014743）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014744）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014745）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014746）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014747）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014749）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014751）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014752）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014754）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014755）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014756）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014757）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014759）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014760）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014761）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014762）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014764）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014766）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014770）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014773）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014774）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014776）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014778）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014779）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014781）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014782）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014784）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014785）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014786）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014788）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014793）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014796）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014800）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014802）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014803）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014804）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014805）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014806）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014807）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014812）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014813）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014814）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014819）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014820）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014821）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014822）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014823）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014826）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014830）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014833）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014835）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014837）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014839）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014841）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014844）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014848）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014850）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014857）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014860）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014863）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014864）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014868）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014869）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014870）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014871）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014872）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014874）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014875）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014876）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014877）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014880）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014881）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014882）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014884）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014894）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014895）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014896）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014900）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014901）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014906）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014909）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014910）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014914）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014915）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014916）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014917）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014919）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014922）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014928）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014929）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014930）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014931）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014936）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00014936）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00014958）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014968）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00014975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00014975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00014977）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00014977）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014983）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014988）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00014997）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015001）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015003）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015006）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015007）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015008）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015012）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015013）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015013）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015015）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015017）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015018）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015023）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015024）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015025）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015029）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015031）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015032）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015033）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015035）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015036）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015038）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015039）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015040）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015041）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015043）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015044）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015045）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015047）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015048）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015059）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015062）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015065）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015067）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015070）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015072）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015076）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015077）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015080）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015083）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015084）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015091）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015093）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015094）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015099）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015102）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015109）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015110）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015117）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015122）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015123）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015125）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015126）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015179）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015180）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015183）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015185）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015186）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015191）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015192）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015193）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015195）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015197）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015198）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015199）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015204）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015204）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015206）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015209）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015209）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015219）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015225）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015225）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015226）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015228）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015231）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015232）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015233）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015234）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015235）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015236）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015239）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015240）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015241）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015242）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015243）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015244）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015245）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015246）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015251）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015255）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015257）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015259）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015260）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015263）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015264）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015265）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015275）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015276）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00015282）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015284）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015285）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015287）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015288）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015291）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00015291）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015293）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015297）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015299）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015300）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015302）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015303）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015304）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015305）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015307）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015312）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015320）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015324）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015325）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015327）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015328）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015331）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015348）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015349）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015351）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015357）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015359）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015362）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015365）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015366）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015372）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015377）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015380）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015390）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015392）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015397）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015399）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015400）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015400）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015402）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015404）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015411）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015419）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015420）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015428）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015430）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015431）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015459）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015542）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015555）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015557）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015602）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015631）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015632）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015633）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015633）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015635）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015637）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015639）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015641）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015642）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015642）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015661）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015665）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015666）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015667）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015669）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015670）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015671）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015673）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015675）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015676）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015680）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015682）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015685）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015693）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015694）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00015695）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E05（设备=TMP00015696）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015697）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015698）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015699）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015699）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015700）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015700）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015702）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015703）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015705）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015705）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015709）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015711）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015727）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015728）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015729）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015730）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015731）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015732）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015747）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015767）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015769）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015774）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015777）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015782）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015785）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015786）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015787）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015790）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015791）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015791）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015792）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015793）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015795）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E02（设备=TMP00015801）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015805）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E03（设备=TMP00015807）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015811）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015811）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015812）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015812）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015821）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015821）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015823）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E06（设备=TMP00015823）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E01（设备=TMP00015836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：RULE-E04（设备=TMP00015836）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00043623）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045931）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045932）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045933）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045934）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045935）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045936）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045937）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045938）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045939）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045940）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045941）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045942）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045943）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045944）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045945）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045946）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045947）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045948）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045949）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045950）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045951）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045952）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045953）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045954）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045955）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045956）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045957）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045958）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045959）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045960）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045961）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045962）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045963）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045964）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045965）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045966）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045967）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045968）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045969）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045970）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045971）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045972）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045973）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045974）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045975）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045976）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045977）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045978）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045979）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045980）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045981）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045982）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045983）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045984）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045985）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045986）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045987）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045988）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045989）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045990）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045991）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045992）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045993）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045994）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045995）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045996）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045997）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045998）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00045999）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046000）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046001）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046002）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046003）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046004）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046005）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046006）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046007）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046008）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046009）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046010）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046011）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046012）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046013）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046014）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046015）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046016）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046017）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046018）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046019）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046020）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046021）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046022）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046023）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046024）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046025）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046026）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046027）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046028）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：开关设备单端悬空，端子数量不足（设备=TMP00046029）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：拓扑断点（设备=TMP00043532）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：拓扑断点（设备=TMP00043534）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：拓扑断点（设备=TMP00043535）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：拓扑断点（设备=TMP00043540）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000012）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000022）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000023）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000029）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000030）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000031）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000035）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000049）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000053）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000057）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000061）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000069）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000083）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000096）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000098）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000100）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000108）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000110）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000111）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000112）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000114）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000122）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000130）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000131）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000132）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000135）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000140）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000143）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000148）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000150）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000152）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000154）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000157）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000161）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000163）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000169）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000174）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000178）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000182）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000184）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：主配网接口校验(4.1漏拼/4.2错拼)（设备=TMP00000187）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：非计划合环（设备=TMP00043893）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：非计划合环（设备=TMP00044305）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：非计划合环（设备=TMP00044306）
-- 该缺陷需人工复核，无自动修复SQL。 -- 待人工复核：非计划合环（设备=TMP00044363）
=======
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044986'; -- 修正设备[TMP00044986]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044322'; -- 修正设备[TMP00044322]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045352'; -- 修正设备[TMP00045352]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045473'; -- 修正设备[TMP00045473]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044821'; -- 修正设备[TMP00044821]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045872'; -- 修正设备[TMP00045872]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045322'; -- 修正设备[TMP00045322]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045578'; -- 修正设备[TMP00045578]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045535'; -- 修正设备[TMP00045535]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045770'; -- 修正设备[TMP00045770]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045866'; -- 修正设备[TMP00045866]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046580'; -- 修正设备[TMP00046580]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045815'; -- 修正设备[TMP00045815]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045529'; -- 修正设备[TMP00045529]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044819'; -- 修正设备[TMP00044819]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044801'; -- 修正设备[TMP00044801]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045492'; -- 修正设备[TMP00045492]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045500'; -- 修正设备[TMP00045500]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044319'; -- 修正设备[TMP00044319]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044278'; -- 修正设备[TMP00044278]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044965'; -- 修正设备[TMP00044965]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045455'; -- 修正设备[TMP00045455]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044907'; -- 修正设备[TMP00044907]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046467'; -- 修正设备[TMP00046467]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045075'; -- 修正设备[TMP00045075]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045339'; -- 修正设备[TMP00045339]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045902'; -- 修正设备[TMP00045902]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043907'; -- 修正设备[TMP00043907]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046475'; -- 修正设备[TMP00046475]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044928'; -- 修正设备[TMP00044928]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045435'; -- 修正设备[TMP00045435]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045986'; -- 修正设备[TMP00045986]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045663'; -- 修正设备[TMP00045663]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045009'; -- 修正设备[TMP00045009]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045732'; -- 修正设备[TMP00045732]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044129'; -- 修正设备[TMP00044129]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044137'; -- 修正设备[TMP00044137]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045904'; -- 修正设备[TMP00045904]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045583'; -- 修正设备[TMP00045583]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044109'; -- 修正设备[TMP00044109]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044532'; -- 修正设备[TMP00044532]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045848'; -- 修正设备[TMP00045848]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044848'; -- 修正设备[TMP00044848]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045309'; -- 修正设备[TMP00045309]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045779'; -- 修正设备[TMP00045779]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044248'; -- 修正设备[TMP00044248]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045325'; -- 修正设备[TMP00045325]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044835'; -- 修正设备[TMP00044835]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046566'; -- 修正设备[TMP00046566]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044777'; -- 修正设备[TMP00044777]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045896'; -- 修正设备[TMP00045896]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045550'; -- 修正设备[TMP00045550]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045874'; -- 修正设备[TMP00045874]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046447'; -- 修正设备[TMP00046447]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044351'; -- 修正设备[TMP00044351]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044861'; -- 修正设备[TMP00044861]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046413'; -- 修正设备[TMP00046413]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044834'; -- 修正设备[TMP00044834]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044771'; -- 修正设备[TMP00044771]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044284'; -- 修正设备[TMP00044284]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045343'; -- 修正设备[TMP00045343]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046442'; -- 修正设备[TMP00046442]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045699'; -- 修正设备[TMP00045699]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044267'; -- 修正设备[TMP00044267]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045819'; -- 修正设备[TMP00045819]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043902'; -- 修正设备[TMP00043902]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044378'; -- 修正设备[TMP00044378]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046153'; -- 修正设备[TMP00046153]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045423'; -- 修正设备[TMP00045423]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045519'; -- 修正设备[TMP00045519]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046128'; -- 修正设备[TMP00046128]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044760'; -- 修正设备[TMP00044760]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046354'; -- 修正设备[TMP00046354]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045024'; -- 修正设备[TMP00045024]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046480'; -- 修正设备[TMP00046480]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046131'; -- 修正设备[TMP00046131]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046469'; -- 修正设备[TMP00046469]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045763'; -- 修正设备[TMP00045763]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044898'; -- 修正设备[TMP00044898]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044944'; -- 修正设备[TMP00044944]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046311'; -- 修正设备[TMP00046311]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045979'; -- 修正设备[TMP00045979]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045366'; -- 修正设备[TMP00045366]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045850'; -- 修正设备[TMP00045850]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045835'; -- 修正设备[TMP00045835]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045074'; -- 修正设备[TMP00045074]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043921'; -- 修正设备[TMP00043921]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044279'; -- 修正设备[TMP00044279]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045515'; -- 修正设备[TMP00045515]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045797'; -- 修正设备[TMP00045797]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046328'; -- 修正设备[TMP00046328]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045678'; -- 修正设备[TMP00045678]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045965'; -- 修正设备[TMP00045965]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044831'; -- 修正设备[TMP00044831]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045988'; -- 修正设备[TMP00045988]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044064'; -- 修正设备[TMP00044064]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046347'; -- 修正设备[TMP00046347]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044806'; -- 修正设备[TMP00044806]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045801'; -- 修正设备[TMP00045801]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045766'; -- 修正设备[TMP00045766]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045450'; -- 修正设备[TMP00045450]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045294'; -- 修正设备[TMP00045294]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044311'; -- 修正设备[TMP00044311]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044257'; -- 修正设备[TMP00044257]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045429'; -- 修正设备[TMP00045429]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043917'; -- 修正设备[TMP00043917]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044302'; -- 修正设备[TMP00044302]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044784'; -- 修正设备[TMP00044784]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045727'; -- 修正设备[TMP00045727]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045062'; -- 修正设备[TMP00045062]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046122'; -- 修正设备[TMP00046122]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044022'; -- 修正设备[TMP00044022]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044520'; -- 修正设备[TMP00044520]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044851'; -- 修正设备[TMP00044851]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045808'; -- 修正设备[TMP00045808]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045392'; -- 修正设备[TMP00045392]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044946'; -- 修正设备[TMP00044946]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045402'; -- 修正设备[TMP00045402]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044799'; -- 修正设备[TMP00044799]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045878'; -- 修正设备[TMP00045878]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045814'; -- 修正设备[TMP00045814]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045823'; -- 修正设备[TMP00045823]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046570'; -- 修正设备[TMP00046570]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045682'; -- 修正设备[TMP00045682]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045992'; -- 修正设备[TMP00045992]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046308'; -- 修正设备[TMP00046308]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045078'; -- 修正设备[TMP00045078]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044595'; -- 修正设备[TMP00044595]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045671'; -- 修正设备[TMP00045671]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045405'; -- 修正设备[TMP00045405]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044168'; -- 修正设备[TMP00044168]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045977'; -- 修正设备[TMP00045977]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045654'; -- 修正设备[TMP00045654]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045318'; -- 修正设备[TMP00045318]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044945'; -- 修正设备[TMP00044945]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045721'; -- 修正设备[TMP00045721]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045330'; -- 修正设备[TMP00045330]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044800'; -- 修正设备[TMP00044800]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045418'; -- 修正设备[TMP00045418]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044793'; -- 修正设备[TMP00044793]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046330'; -- 修正设备[TMP00046330]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044839'; -- 修正设备[TMP00044839]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045865'; -- 修正设备[TMP00045865]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044903'; -- 修正设备[TMP00044903]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044875'; -- 修正设备[TMP00044875]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045521'; -- 修正设备[TMP00045521]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044368'; -- 修正设备[TMP00044368]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044273'; -- 修正设备[TMP00044273]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045626'; -- 修正设备[TMP00045626]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045306'; -- 修正设备[TMP00045306]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045972'; -- 修正设备[TMP00045972]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044813'; -- 修正设备[TMP00044813]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045718'; -- 修正设备[TMP00045718]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045453'; -- 修正设备[TMP00045453]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045789'; -- 修正设备[TMP00045789]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044980'; -- 修正设备[TMP00044980]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046144'; -- 修正设备[TMP00046144]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045019'; -- 修正设备[TMP00045019]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045949'; -- 修正设备[TMP00045949]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044142'; -- 修正设备[TMP00044142]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045433'; -- 修正设备[TMP00045433]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044838'; -- 修正设备[TMP00044838]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044866'; -- 修正设备[TMP00044866]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044346'; -- 修正设备[TMP00044346]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045055'; -- 修正设备[TMP00045055]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044114'; -- 修正设备[TMP00044114]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045976'; -- 修正设备[TMP00045976]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045048'; -- 修正设备[TMP00045048]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046564'; -- 修正设备[TMP00046564]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046601'; -- 修正设备[TMP00046601]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045984'; -- 修正设备[TMP00045984]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045772'; -- 修正设备[TMP00045772]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045414'; -- 修正设备[TMP00045414]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044554'; -- 修正设备[TMP00044554]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046410'; -- 修正设备[TMP00046410]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044893'; -- 修正设备[TMP00044893]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045568'; -- 修正设备[TMP00045568]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045537'; -- 修正设备[TMP00045537]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046010'; -- 修正设备[TMP00046010]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045981'; -- 修正设备[TMP00045981]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044978'; -- 修正设备[TMP00044978]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044963'; -- 修正设备[TMP00044963]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045870'; -- 修正设备[TMP00045870]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045443'; -- 修正设备[TMP00045443]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045302'; -- 修正设备[TMP00045302]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044577'; -- 修正设备[TMP00044577]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046432'; -- 修正设备[TMP00046432]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045989'; -- 修正设备[TMP00045989]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045852'; -- 修正设备[TMP00045852]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045820'; -- 修正设备[TMP00045820]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045337'; -- 修正设备[TMP00045337]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045595'; -- 修正设备[TMP00045595]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043895'; -- 修正设备[TMP00043895]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045369'; -- 修正设备[TMP00045369]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044357'; -- 修正设备[TMP00044357]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045037'; -- 修正设备[TMP00045037]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046532'; -- 修正设备[TMP00046532]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045032'; -- 修正设备[TMP00045032]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046552'; -- 修正设备[TMP00046552]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044596'; -- 修正设备[TMP00044596]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046157'; -- 修正设备[TMP00046157]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044846'; -- 修正设备[TMP00044846]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045792'; -- 修正设备[TMP00045792]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043916'; -- 修正设备[TMP00043916]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046006'; -- 修正设备[TMP00046006]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045411'; -- 修正设备[TMP00045411]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045466'; -- 修正设备[TMP00045466]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044370'; -- 修正设备[TMP00044370]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044987'; -- 修正设备[TMP00044987]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045005'; -- 修正设备[TMP00045005]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045941'; -- 修正设备[TMP00045941]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044929'; -- 修正设备[TMP00044929]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044066'; -- 修正设备[TMP00044066]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044827'; -- 修正设备[TMP00044827]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046453'; -- 修正设备[TMP00046453]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046574'; -- 修正设备[TMP00046574]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045308'; -- 修正设备[TMP00045308]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046450'; -- 修正设备[TMP00046450]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045574'; -- 修正设备[TMP00045574]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044899'; -- 修正设备[TMP00044899]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045479'; -- 修正设备[TMP00045479]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045756'; -- 修正设备[TMP00045756]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045562'; -- 修正设备[TMP00045562]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045491'; -- 修正设备[TMP00045491]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046020'; -- 修正设备[TMP00046020]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046007'; -- 修正设备[TMP00046007]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044814'; -- 修正设备[TMP00044814]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044288'; -- 修正设备[TMP00044288]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046461'; -- 修正设备[TMP00046461]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045828'; -- 修正设备[TMP00045828]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045416'; -- 修正设备[TMP00045416]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044773'; -- 修正设备[TMP00044773]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045729'; -- 修正设备[TMP00045729]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043923'; -- 修正设备[TMP00043923]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045695'; -- 修正设备[TMP00045695]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044139'; -- 修正设备[TMP00044139]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044337'; -- 修正设备[TMP00044337]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044798'; -- 修正设备[TMP00044798]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046600'; -- 修正设备[TMP00046600]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044356'; -- 修正设备[TMP00044356]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046127'; -- 修正设备[TMP00046127]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045049'; -- 修正设备[TMP00045049]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045605'; -- 修正设备[TMP00045605]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044940'; -- 修正设备[TMP00044940]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045504'; -- 修正设备[TMP00045504]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044365'; -- 修正设备[TMP00044365]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045622'; -- 修正设备[TMP00045622]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045945'; -- 修正设备[TMP00045945]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045742'; -- 修正设备[TMP00045742]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046356'; -- 修正设备[TMP00046356]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044882'; -- 修正设备[TMP00044882]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046440'; -- 修正设备[TMP00046440]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045601'; -- 修正设备[TMP00045601]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045843'; -- 修正设备[TMP00045843]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045716'; -- 修正设备[TMP00045716]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045760'; -- 修正设备[TMP00045760]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045432'; -- 修正设备[TMP00045432]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044931'; -- 修正设备[TMP00044931]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046156'; -- 修正设备[TMP00046156]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044934'; -- 修正设备[TMP00044934]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045401'; -- 修正设备[TMP00045401]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044252'; -- 修正设备[TMP00044252]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044024'; -- 修正设备[TMP00044024]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045781'; -- 修正设备[TMP00045781]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045360'; -- 修正设备[TMP00045360]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045680'; -- 修正设备[TMP00045680]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045685'; -- 修正设备[TMP00045685]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045445'; -- 修正设备[TMP00045445]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044363'; -- 修正设备[TMP00044363]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044104'; -- 修正设备[TMP00044104]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044941'; -- 修正设备[TMP00044941]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045046'; -- 修正设备[TMP00045046]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045298'; -- 修正设备[TMP00045298]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044075'; -- 修正设备[TMP00044075]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045698'; -- 修正设备[TMP00045698]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045438'; -- 修正设备[TMP00045438]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044058'; -- 修正设备[TMP00044058]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045599'; -- 修正设备[TMP00045599]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046483'; -- 修正设备[TMP00046483]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045620'; -- 修正设备[TMP00045620]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044076'; -- 修正设备[TMP00044076]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044786'; -- 修正设备[TMP00044786]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046460'; -- 修正设备[TMP00046460]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044538'; -- 修正设备[TMP00044538]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045465'; -- 修正设备[TMP00045465]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044063'; -- 修正设备[TMP00044063]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045738'; -- 修正设备[TMP00045738]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045531'; -- 修正设备[TMP00045531]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045545'; -- 修正设备[TMP00045545]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044318'; -- 修正设备[TMP00044318]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044349'; -- 修正设备[TMP00044349]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044795'; -- 修正设备[TMP00044795]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045829'; -- 修正设备[TMP00045829]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044270'; -- 修正设备[TMP00044270]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045816'; -- 修正设备[TMP00045816]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045059'; -- 修正设备[TMP00045059]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044966'; -- 修正设备[TMP00044966]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044329'; -- 修正设备[TMP00044329]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045041'; -- 修正设备[TMP00045041]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045629'; -- 修正设备[TMP00045629]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044515'; -- 修正设备[TMP00044515]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046018'; -- 修正设备[TMP00046018]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045547'; -- 修正设备[TMP00045547]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045071'; -- 修正设备[TMP00045071]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045856'; -- 修正设备[TMP00045856]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044339'; -- 修正设备[TMP00044339]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046334'; -- 修正设备[TMP00046334]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046576'; -- 修正设备[TMP00046576]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044517'; -- 修正设备[TMP00044517]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046004'; -- 修正设备[TMP00046004]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045788'; -- 修正设备[TMP00045788]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045643'; -- 修正设备[TMP00045643]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046316'; -- 修正设备[TMP00046316]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046141'; -- 修正设备[TMP00046141]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044883'; -- 修正设备[TMP00044883]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044985'; -- 修正设备[TMP00044985]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045888'; -- 修正设备[TMP00045888]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046002'; -- 修正设备[TMP00046002]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045580'; -- 修正设备[TMP00045580]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045407'; -- 修正设备[TMP00045407]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045039'; -- 修正设备[TMP00045039]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046110'; -- 修正设备[TMP00046110]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046419'; -- 修正设备[TMP00046419]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045081'; -- 修正设备[TMP00045081]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044919'; -- 修正设备[TMP00044919]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045957'; -- 修正设备[TMP00045957]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045938'; -- 修正设备[TMP00045938]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045497'; -- 修正设备[TMP00045497]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044113'; -- 修正设备[TMP00044113]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046324'; -- 修正设备[TMP00046324]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045404'; -- 修正设备[TMP00045404]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046415'; -- 修正设备[TMP00046415]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044972'; -- 修正设备[TMP00044972]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044449'; -- 修正设备[TMP00044449]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045813'; -- 修正设备[TMP00045813]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045703'; -- 修正设备[TMP00045703]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045630'; -- 修正设备[TMP00045630]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046457'; -- 修正设备[TMP00046457]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044976'; -- 修正设备[TMP00044976]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046319'; -- 修正设备[TMP00046319]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044290'; -- 修正设备[TMP00044290]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045603'; -- 修正设备[TMP00045603]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046497'; -- 修正设备[TMP00046497]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044312'; -- 修正设备[TMP00044312]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045524'; -- 修正设备[TMP00045524]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045012'; -- 修正设备[TMP00045012]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045863'; -- 修正设备[TMP00045863]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045436'; -- 修正设备[TMP00045436]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045358'; -- 修正设备[TMP00045358]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044258'; -- 修正设备[TMP00044258]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044025'; -- 修正设备[TMP00044025]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044336'; -- 修正设备[TMP00044336]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046486'; -- 修正设备[TMP00046486]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045864'; -- 修正设备[TMP00045864]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045991'; -- 修正设备[TMP00045991]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045044'; -- 修正设备[TMP00045044]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046129'; -- 修正设备[TMP00046129]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045679'; -- 修正设备[TMP00045679]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045736'; -- 修正设备[TMP00045736]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044289'; -- 修正设备[TMP00044289]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046531'; -- 修正设备[TMP00046531]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044297'; -- 修正设备[TMP00044297]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045043'; -- 修正设备[TMP00045043]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045483'; -- 修正设备[TMP00045483]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044925'; -- 修正设备[TMP00044925]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045690'; -- 修正设备[TMP00045690]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044209'; -- 修正设备[TMP00044209]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044325'; -- 修正设备[TMP00044325]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043924'; -- 修正设备[TMP00043924]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046577'; -- 修正设备[TMP00046577]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044804'; -- 修正设备[TMP00044804]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045300'; -- 修正设备[TMP00045300]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044261'; -- 修正设备[TMP00044261]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045544'; -- 修正设备[TMP00045544]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046459'; -- 修正设备[TMP00046459]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043903'; -- 修正设备[TMP00043903]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045964'; -- 修正设备[TMP00045964]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045317'; -- 修正设备[TMP00045317]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046019'; -- 修正设备[TMP00046019]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044133'; -- 修正设备[TMP00044133]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045798'; -- 修正设备[TMP00045798]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045289'; -- 修正设备[TMP00045289]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046314'; -- 修正设备[TMP00046314]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045824'; -- 修正设备[TMP00045824]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046344'; -- 修正设备[TMP00046344]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045955'; -- 修正设备[TMP00045955]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046117'; -- 修正设备[TMP00046117]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045723'; -- 修正设备[TMP00045723]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045320'; -- 修正设备[TMP00045320]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044870'; -- 修正设备[TMP00044870]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045608'; -- 修正设备[TMP00045608]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046575'; -- 修正设备[TMP00046575]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044361'; -- 修正设备[TMP00044361]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045069'; -- 修正设备[TMP00045069]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046431'; -- 修正设备[TMP00046431]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046448'; -- 修正设备[TMP00046448]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044778'; -- 修正设备[TMP00044778]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045670'; -- 修正设备[TMP00045670]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045751'; -- 修正设备[TMP00045751]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045553'; -- 修正设备[TMP00045553]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045719'; -- 修正设备[TMP00045719]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044949'; -- 修正设备[TMP00044949]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046343'; -- 修正设备[TMP00046343]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046436'; -- 修正设备[TMP00046436]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045564'; -- 修正设备[TMP00045564]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044935'; -- 修正设备[TMP00044935]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045011'; -- 修正设备[TMP00045011]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045001'; -- 修正设备[TMP00045001]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045027'; -- 修正设备[TMP00045027]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045954'; -- 修正设备[TMP00045954]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045484'; -- 修正设备[TMP00045484]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045861'; -- 修正设备[TMP00045861]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045825'; -- 修正设备[TMP00045825]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046479'; -- 修正设备[TMP00046479]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044867'; -- 修正设备[TMP00044867]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045658'; -- 修正设备[TMP00045658]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044269'; -- 修正设备[TMP00044269]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045079'; -- 修正设备[TMP00045079]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045571'; -- 修正设备[TMP00045571]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045705'; -- 修正设备[TMP00045705]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046148'; -- 修正设备[TMP00046148]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046411'; -- 修正设备[TMP00046411]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046024'; -- 修正设备[TMP00046024]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044347'; -- 修正设备[TMP00044347]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045572'; -- 修正设备[TMP00045572]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045590'; -- 修正设备[TMP00045590]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046468'; -- 修正设备[TMP00046468]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045901'; -- 修正设备[TMP00045901]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046445'; -- 修正设备[TMP00046445]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044272'; -- 修正设备[TMP00044272]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045383'; -- 修正设备[TMP00045383]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043900'; -- 修正设备[TMP00043900]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045594'; -- 修正设备[TMP00045594]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045961'; -- 修正设备[TMP00045961]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045884'; -- 修正设备[TMP00045884]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045740'; -- 修正设备[TMP00045740]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044306'; -- 修正设备[TMP00044306]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045747'; -- 修正设备[TMP00045747]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045540'; -- 修正设备[TMP00045540]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046340'; -- 修正设备[TMP00046340]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044950'; -- 修正设备[TMP00044950]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045546'; -- 修正设备[TMP00045546]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046519'; -- 修正设备[TMP00046519]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046444'; -- 修正设备[TMP00046444]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045730'; -- 修正设备[TMP00045730]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045621'; -- 修正设备[TMP00045621]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045458'; -- 修正设备[TMP00045458]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044936'; -- 修正设备[TMP00044936]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045858'; -- 修正设备[TMP00045858]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044841'; -- 修正设备[TMP00044841]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045889'; -- 修正设备[TMP00045889]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044815'; -- 修正设备[TMP00044815]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045711'; -- 修正设备[TMP00045711]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044377'; -- 修正设备[TMP00044377]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044843'; -- 修正设备[TMP00044843]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044023'; -- 修正设备[TMP00044023]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045543'; -- 修正设备[TMP00045543]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044860'; -- 修正设备[TMP00044860]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045033'; -- 修正设备[TMP00045033]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046443'; -- 修正设备[TMP00046443]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045344'; -- 修正设备[TMP00045344]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045083'; -- 修正设备[TMP00045083]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045934'; -- 修正设备[TMP00045934]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045528'; -- 修正设备[TMP00045528]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046119'; -- 修正设备[TMP00046119]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045396'; -- 修正设备[TMP00045396]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044342'; -- 修正设备[TMP00044342]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045589'; -- 修正设备[TMP00045589]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046476'; -- 修正设备[TMP00046476]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046456'; -- 修正设备[TMP00046456]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044938'; -- 修正设备[TMP00044938]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045452'; -- 修正设备[TMP00045452]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046317'; -- 修正设备[TMP00046317]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044563'; -- 修正设备[TMP00044563]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044338'; -- 修正设备[TMP00044338]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044933'; -- 修正设备[TMP00044933]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044255'; -- 修正设备[TMP00044255]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046433'; -- 修正设备[TMP00046433]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045903'; -- 修正设备[TMP00045903]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044141'; -- 修正设备[TMP00044141]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043894'; -- 修正设备[TMP00043894]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044979'; -- 修正设备[TMP00044979]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045617'; -- 修正设备[TMP00045617]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045047'; -- 修正设备[TMP00045047]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044909'; -- 修正设备[TMP00044909]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045612'; -- 修正设备[TMP00045612]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045891'; -- 修正设备[TMP00045891]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046017'; -- 修正设备[TMP00046017]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045507'; -- 修正设备[TMP00045507]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045342'; -- 修正设备[TMP00045342]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045566'; -- 修正设备[TMP00045566]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045050'; -- 修正设备[TMP00045050]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044943'; -- 修正设备[TMP00044943]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045065'; -- 修正设备[TMP00045065]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046595'; -- 修正设备[TMP00046595]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046569'; -- 修正设备[TMP00046569]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046424'; -- 修正设备[TMP00046424]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045510'; -- 修正设备[TMP00045510]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044901'; -- 修正设备[TMP00044901]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045796'; -- 修正设备[TMP00045796]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044984'; -- 修正设备[TMP00044984]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044894'; -- 修正设备[TMP00044894]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046584'; -- 修正设备[TMP00046584]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046137'; -- 修正设备[TMP00046137]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045936'; -- 修正设备[TMP00045936]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044989'; -- 修正设备[TMP00044989]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045757'; -- 修正设备[TMP00045757]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044902'; -- 修正设备[TMP00044902]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045606'; -- 修正设备[TMP00045606]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045428'; -- 修正设备[TMP00045428]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045712'; -- 修正设备[TMP00045712]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044857'; -- 修正设备[TMP00044857]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045614'; -- 修正设备[TMP00045614]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045980'; -- 修正设备[TMP00045980]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045350'; -- 修正设备[TMP00045350]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045696'; -- 修正设备[TMP00045696]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044285'; -- 修正设备[TMP00044285]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045393'; -- 修正设备[TMP00045393]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044918'; -- 修正设备[TMP00044918]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045460'; -- 修正设备[TMP00045460]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045555'; -- 修正设备[TMP00045555]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045363'; -- 修正设备[TMP00045363]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045817'; -- 修正设备[TMP00045817]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044820'; -- 修正设备[TMP00044820]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046349'; -- 修正设备[TMP00046349]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045539'; -- 修正设备[TMP00045539]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046318'; -- 修正设备[TMP00046318]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045672'; -- 修正设备[TMP00045672]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044808'; -- 修正设备[TMP00044808]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044210'; -- 修正设备[TMP00044210]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044968'; -- 修正设备[TMP00044968]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044366'; -- 修正设备[TMP00044366]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044890'; -- 修正设备[TMP00044890]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046105'; -- 修正设备[TMP00046105]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044331'; -- 修正设备[TMP00044331]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044307'; -- 修正设备[TMP00044307]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044380'; -- 修正设备[TMP00044380]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045364'; -- 修正设备[TMP00045364]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045327'; -- 修正设备[TMP00045327]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045409'; -- 修正设备[TMP00045409]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044959'; -- 修正设备[TMP00044959]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045403'; -- 修正设备[TMP00045403]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044250'; -- 修正设备[TMP00044250]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045488'; -- 修正设备[TMP00045488]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044956'; -- 修正设备[TMP00044956]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045563'; -- 修正设备[TMP00045563]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045787'; -- 修正设备[TMP00045787]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045647'; -- 修正设备[TMP00045647]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044516'; -- 修正设备[TMP00044516]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046417'; -- 修正设备[TMP00046417]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046581'; -- 修正设备[TMP00046581]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044994'; -- 修正设备[TMP00044994]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044923'; -- 修正设备[TMP00044923]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044982'; -- 修正设备[TMP00044982]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046116'; -- 修正设备[TMP00046116]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044762'; -- 修正设备[TMP00044762]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045371'; -- 修正设备[TMP00045371]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044872'; -- 修正设备[TMP00044872]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046332'; -- 修正设备[TMP00046332]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045851'; -- 修正设备[TMP00045851]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044911'; -- 修正设备[TMP00044911]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045490'; -- 修正设备[TMP00045490]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045777'; -- 修正设备[TMP00045777]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045875'; -- 修正设备[TMP00045875]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044367'; -- 修正设备[TMP00044367]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045809'; -- 修正设备[TMP00045809]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045380'; -- 修正设备[TMP00045380]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045831'; -- 修正设备[TMP00045831]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044824'; -- 修正设备[TMP00044824]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044353'; -- 修正设备[TMP00044353]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045326'; -- 修正设备[TMP00045326]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045077'; -- 修正设备[TMP00045077]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045997'; -- 修正设备[TMP00045997]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045724'; -- 修正设备[TMP00045724]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045660'; -- 修正设备[TMP00045660]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045389'; -- 修正设备[TMP00045389]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044359'; -- 修正设备[TMP00044359]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046136'; -- 修正设备[TMP00046136]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045769'; -- 修正设备[TMP00045769]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045953'; -- 修正设备[TMP00045953]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045931'; -- 修正设备[TMP00045931]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045061'; -- 修正设备[TMP00045061]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045527'; -- 修正设备[TMP00045527]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045556'; -- 修正设备[TMP00045556]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045419'; -- 修正设备[TMP00045419]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045767'; -- 修正设备[TMP00045767]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046594'; -- 修正设备[TMP00046594]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045060'; -- 修正设备[TMP00045060]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044263'; -- 修正设备[TMP00044263]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044817'; -- 修正设备[TMP00044817]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044448'; -- 修正设备[TMP00044448]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046135'; -- 修正设备[TMP00046135]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044772'; -- 修正设备[TMP00044772]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045425'; -- 修正设备[TMP00045425]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045734'; -- 修正设备[TMP00045734]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046446'; -- 修正设备[TMP00046446]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044765'; -- 修正设备[TMP00044765]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045702'; -- 修正设备[TMP00045702]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046359'; -- 修正设备[TMP00046359]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045370'; -- 修正设备[TMP00045370]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046341'; -- 修正设备[TMP00046341]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045944'; -- 修正设备[TMP00045944]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045847'; -- 修正设备[TMP00045847]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044947'; -- 修正设备[TMP00044947]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045867'; -- 修正设备[TMP00045867]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045669'; -- 修正设备[TMP00045669]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045472'; -- 修正设备[TMP00045472]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045970'; -- 修正设备[TMP00045970]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044260'; -- 修正设备[TMP00044260]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046329'; -- 修正设备[TMP00046329]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044287'; -- 修正设备[TMP00044287]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046027'; -- 修正设备[TMP00046027]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046573'; -- 修正设备[TMP00046573]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044854'; -- 修正设备[TMP00044854]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044836'; -- 修正设备[TMP00044836]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045971'; -- 修正设备[TMP00045971]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045993'; -- 修正设备[TMP00045993]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045653'; -- 修正设备[TMP00045653]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046482'; -- 修正设备[TMP00046482]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046596'; -- 修正设备[TMP00046596]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046104'; -- 修正设备[TMP00046104]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045688'; -- 修正设备[TMP00045688]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045297'; -- 修正设备[TMP00045297]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045415'; -- 修正设备[TMP00045415]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044070'; -- 修正设备[TMP00044070]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045812'; -- 修正设备[TMP00045812]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045487'; -- 修正设备[TMP00045487]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044131'; -- 修正设备[TMP00044131]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045667'; -- 修正设备[TMP00045667]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044071'; -- 修正设备[TMP00044071]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046458'; -- 修正设备[TMP00046458]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043898'; -- 修正设备[TMP00043898]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046322'; -- 修正设备[TMP00046322]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045749'; -- 修正设备[TMP00045749]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045536'; -- 修正设备[TMP00045536]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046452'; -- 修正设备[TMP00046452]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045581'; -- 修正设备[TMP00045581]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045948'; -- 修正设备[TMP00045948]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044291'; -- 修正设备[TMP00044291]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045345'; -- 修正设备[TMP00045345]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044862'; -- 修正设备[TMP00044862]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045085'; -- 修正设备[TMP00045085]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045879'; -- 修正设备[TMP00045879]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046008'; -- 修正设备[TMP00046008]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045054'; -- 修正设备[TMP00045054]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044853'; -- 修正设备[TMP00044853]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045846'; -- 修正设备[TMP00045846]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045549'; -- 修正设备[TMP00045549]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045943'; -- 修正设备[TMP00045943]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045053'; -- 修正设备[TMP00045053]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044829'; -- 修正设备[TMP00044829]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045478'; -- 修正设备[TMP00045478]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044951'; -- 修正设备[TMP00044951]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045554'; -- 修正设备[TMP00045554]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044764'; -- 修正设备[TMP00044764]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044779'; -- 修正设备[TMP00044779]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044326'; -- 修正设备[TMP00044326]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043922'; -- 修正设备[TMP00043922]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046138'; -- 修正设备[TMP00046138]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045837'; -- 修正设备[TMP00045837]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046315'; -- 修正设备[TMP00046315]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045375'; -- 修正设备[TMP00045375]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045593'; -- 修正设备[TMP00045593]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045470'; -- 修正设备[TMP00045470]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044790'; -- 修正设备[TMP00044790]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044074'; -- 修正设备[TMP00044074]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044768'; -- 修正设备[TMP00044768]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046551'; -- 修正设备[TMP00046551]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045633'; -- 修正设备[TMP00045633]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044282'; -- 修正设备[TMP00044282]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046152'; -- 修正设备[TMP00046152]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045895'; -- 修正设备[TMP00045895]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045030'; -- 修正设备[TMP00045030]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044896'; -- 修正设备[TMP00044896]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045591'; -- 修正设备[TMP00045591]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045018'; -- 修正设备[TMP00045018]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044796'; -- 修正设备[TMP00044796]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045517'; -- 修正设备[TMP00045517]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045785'; -- 修正设备[TMP00045785]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045516'; -- 修正设备[TMP00045516]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045604'; -- 修正设备[TMP00045604]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045804'; -- 修正设备[TMP00045804]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044265'; -- 修正设备[TMP00044265]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044345'; -- 修正设备[TMP00044345]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045607'; -- 修正设备[TMP00045607]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046011'; -- 修正设备[TMP00046011]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044259'; -- 修正设备[TMP00044259]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044953'; -- 修正设备[TMP00044953]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046339'; -- 修正设备[TMP00046339]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045985'; -- 修正设备[TMP00045985]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045799'; -- 修正设备[TMP00045799]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044957'; -- 修正设备[TMP00044957]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044849'; -- 修正设备[TMP00044849]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046363'; -- 修正设备[TMP00046363]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045664'; -- 修正设备[TMP00045664]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045974'; -- 修正设备[TMP00045974]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045755'; -- 修正设备[TMP00045755]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044997'; -- 修正设备[TMP00044997]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044062'; -- 修正设备[TMP00044062]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046464'; -- 修正设备[TMP00046464]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045942'; -- 修正设备[TMP00045942]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045887'; -- 修正设备[TMP00045887]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044904'; -- 修正设备[TMP00044904]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043908'; -- 修正设备[TMP00043908]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045469'; -- 修正设备[TMP00045469]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044766'; -- 修正设备[TMP00044766]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046355'; -- 修正设备[TMP00046355]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045015'; -- 修正设备[TMP00045015]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044913'; -- 修正设备[TMP00044913]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045834'; -- 修正设备[TMP00045834]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045935'; -- 修正设备[TMP00045935]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045052'; -- 修正设备[TMP00045052]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044837'; -- 修正设备[TMP00044837]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044550'; -- 修正设备[TMP00044550]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046111'; -- 修正设备[TMP00046111]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044868'; -- 修正设备[TMP00044868]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046454'; -- 修正设备[TMP00046454]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044371'; -- 修正设备[TMP00044371]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045365'; -- 修正设备[TMP00045365]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044299'; -- 修正设备[TMP00044299]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045982'; -- 修正设备[TMP00045982]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045034'; -- 修正设备[TMP00045034]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044334'; -- 修正设备[TMP00044334]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044321'; -- 修正设备[TMP00044321]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046321'; -- 修正设备[TMP00046321]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045677'; -- 修正设备[TMP00045677]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044314'; -- 修正设备[TMP00044314]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045854'; -- 修正设备[TMP00045854]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045728'; -- 修正设备[TMP00045728]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044897'; -- 修正设备[TMP00044897]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045684'; -- 修正设备[TMP00045684]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044998'; -- 修正设备[TMP00044998]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045509'; -- 修正设备[TMP00045509]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045548'; -- 修正设备[TMP00045548]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045338'; -- 修正设备[TMP00045338]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046012'; -- 修正设备[TMP00046012]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044917'; -- 修正设备[TMP00044917]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045883'; -- 修正设备[TMP00045883]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046106'; -- 修正设备[TMP00046106]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045700'; -- 修正设备[TMP00045700]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045639'; -- 修正设备[TMP00045639]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045374'; -- 修正设备[TMP00045374]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044268'; -- 修正设备[TMP00044268]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046323'; -- 修正设备[TMP00046323]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045720'; -- 修正设备[TMP00045720]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045291'; -- 修正设备[TMP00045291]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044855'; -- 修正设备[TMP00044855]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045388'; -- 修正设备[TMP00045388]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045066'; -- 修正设备[TMP00045066]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044891'; -- 修正设备[TMP00044891]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045967'; -- 修正设备[TMP00045967]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045538'; -- 修正设备[TMP00045538]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045683'; -- 修正设备[TMP00045683]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045446'; -- 修正设备[TMP00045446]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044770'; -- 修正设备[TMP00044770]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045648'; -- 修正设备[TMP00045648]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045995'; -- 修正设备[TMP00045995]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043896'; -- 修正设备[TMP00043896]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045694'; -- 修正设备[TMP00045694]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045709'; -- 修正设备[TMP00045709]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045937'; -- 修正设备[TMP00045937]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045016'; -- 修正设备[TMP00045016]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046455'; -- 修正设备[TMP00046455]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044876'; -- 修正设备[TMP00044876]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045624'; -- 修正设备[TMP00045624]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046132'; -- 修正设备[TMP00046132]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045853'; -- 修正设备[TMP00045853]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045795'; -- 修正设备[TMP00045795]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045748'; -- 修正设备[TMP00045748]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046143'; -- 修正设备[TMP00046143]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044264'; -- 修正设备[TMP00044264]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045662'; -- 修正设备[TMP00045662]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044995'; -- 修正设备[TMP00044995]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045557'; -- 修正设备[TMP00045557]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046427'; -- 修正设备[TMP00046427]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046015'; -- 修正设备[TMP00046015]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044212'; -- 修正设备[TMP00044212]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046426'; -- 修正设备[TMP00046426]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044844'; -- 修正设备[TMP00044844]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045513'; -- 修正设备[TMP00045513]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045357'; -- 修正设备[TMP00045357]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044335'; -- 修正设备[TMP00044335]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045676'; -- 修正设备[TMP00045676]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045842'; -- 修正设备[TMP00045842]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045833'; -- 修正设备[TMP00045833]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044130'; -- 修正设备[TMP00044130]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045743'; -- 修正设备[TMP00045743]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046466'; -- 修正设备[TMP00046466]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045489'; -- 修正设备[TMP00045489]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045480'; -- 修正设备[TMP00045480]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045427'; -- 修正设备[TMP00045427]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045441'; -- 修正设备[TMP00045441]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044280'; -- 修正设备[TMP00044280]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045006'; -- 修正设备[TMP00045006]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046434'; -- 修正设备[TMP00046434]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044785'; -- 修正设备[TMP00044785]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044874'; -- 修正设备[TMP00044874]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045451'; -- 修正设备[TMP00045451]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044374'; -- 修正设备[TMP00044374]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044315'; -- 修正设备[TMP00044315]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046423'; -- 修正设备[TMP00046423]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044277'; -- 修正设备[TMP00044277]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045761'; -- 修正设备[TMP00045761]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046485'; -- 修正设备[TMP00046485]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045457'; -- 修正设备[TMP00045457]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045885'; -- 修正设备[TMP00045885]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045023'; -- 修正设备[TMP00045023]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046578'; -- 修正设备[TMP00046578]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044818'; -- 修正设备[TMP00044818]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045567'; -- 修正设备[TMP00045567]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045057'; -- 修正设备[TMP00045057]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045084'; -- 修正设备[TMP00045084]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045020'; -- 修正设备[TMP00045020]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045035'; -- 修正设备[TMP00045035]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044788'; -- 修正设备[TMP00044788]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045862'; -- 修正设备[TMP00045862]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045508'; -- 修正设备[TMP00045508]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046026'; -- 修正设备[TMP00046026]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046023'; -- 修正设备[TMP00046023]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046150'; -- 修正设备[TMP00046150]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046001'; -- 修正设备[TMP00046001]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046000'; -- 修正设备[TMP00046000]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045810'; -- 修正设备[TMP00045810]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045713'; -- 修正设备[TMP00045713]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045674'; -- 修正设备[TMP00045674]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045367'; -- 修正设备[TMP00045367]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045963'; -- 修正设备[TMP00045963]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045007'; -- 修正设备[TMP00045007]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046009'; -- 修正设备[TMP00046009]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045692'; -- 修正设备[TMP00045692]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045673'; -- 修正设备[TMP00045673]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045689'; -- 修正设备[TMP00045689]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045952'; -- 修正设备[TMP00045952]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045056'; -- 修正设备[TMP00045056]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045026'; -- 修正设备[TMP00045026]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045598'; -- 修正设备[TMP00045598]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044859'; -- 修正设备[TMP00044859]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045561'; -- 修正设备[TMP00045561]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045444'; -- 修正设备[TMP00045444]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045324'; -- 修正设备[TMP00045324]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046568'; -- 修正设备[TMP00046568]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044991'; -- 修正设备[TMP00044991]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045686'; -- 修正设备[TMP00045686]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045602'; -- 修正设备[TMP00045602]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046121'; -- 修正设备[TMP00046121]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046604'; -- 修正设备[TMP00046604]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046125'; -- 修正设备[TMP00046125]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045329'; -- 修正设备[TMP00045329]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043910'; -- 修正设备[TMP00043910]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044073'; -- 修正设备[TMP00044073]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045467'; -- 修正设备[TMP00045467]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046585'; -- 修正设备[TMP00046585]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046435'; -- 修正设备[TMP00046435]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045793'; -- 修正设备[TMP00045793]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045675'; -- 修正设备[TMP00045675]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045305'; -- 修正设备[TMP00045305]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044927'; -- 修正设备[TMP00044927]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045750'; -- 修正设备[TMP00045750]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046439'; -- 修正设备[TMP00046439]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044775'; -- 修正设备[TMP00044775]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045890'; -- 修正设备[TMP00045890]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045379'; -- 修正设备[TMP00045379]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045004'; -- 修正设备[TMP00045004]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045565'; -- 修正设备[TMP00045565]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044932'; -- 修正设备[TMP00044932]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045354'; -- 修正设备[TMP00045354]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044912'; -- 修正设备[TMP00044912]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045873'; -- 修正设备[TMP00045873]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046571'; -- 修正设备[TMP00046571]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044791'; -- 修正设备[TMP00044791]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045386'; -- 修正设备[TMP00045386]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046507'; -- 修正设备[TMP00046507]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045384'; -- 修正设备[TMP00045384]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044797'; -- 修正设备[TMP00044797]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045530'; -- 修正设备[TMP00045530]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045969'; -- 修正设备[TMP00045969]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046326'; -- 修正设备[TMP00046326]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044880'; -- 修正设备[TMP00044880]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046602'; -- 修正设备[TMP00046602]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044761'; -- 修正设备[TMP00044761]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045017'; -- 修正设备[TMP00045017]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044358'; -- 修正设备[TMP00044358]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045356'; -- 修正设备[TMP00045356]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044112'; -- 修正设备[TMP00044112]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044871'; -- 修正设备[TMP00044871]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045359'; -- 修正设备[TMP00045359]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045067'; -- 修正设备[TMP00045067]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044847'; -- 修正设备[TMP00044847]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045794'; -- 修正设备[TMP00045794]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044295'; -- 修正设备[TMP00044295]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045000'; -- 修正设备[TMP00045000]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046142'; -- 修正设备[TMP00046142]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045726'; -- 修正设备[TMP00045726]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044886'; -- 修正设备[TMP00044886]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045512'; -- 修正设备[TMP00045512]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045331'; -- 修正设备[TMP00045331]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046421'; -- 修正设备[TMP00046421]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046353'; -- 修正设备[TMP00046353]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045307'; -- 修正设备[TMP00045307]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043920'; -- 修正设备[TMP00043920]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045558'; -- 修正设备[TMP00045558]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045623'; -- 修正设备[TMP00045623]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045844'; -- 修正设备[TMP00045844]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044864'; -- 修正设备[TMP00044864]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046496'; -- 修正设备[TMP00046496]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044167'; -- 修正设备[TMP00044167]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046438'; -- 修正设备[TMP00046438]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044763'; -- 修正设备[TMP00044763]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045575'; -- 修正设备[TMP00045575]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045501'; -- 修正设备[TMP00045501]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045417'; -- 修正设备[TMP00045417]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045708'; -- 修正设备[TMP00045708]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044068'; -- 修正设备[TMP00044068]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044350'; -- 修正设备[TMP00044350]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045002'; -- 修正设备[TMP00045002]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045022'; -- 修正设备[TMP00045022]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045744'; -- 修正设备[TMP00045744]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045385'; -- 修正设备[TMP00045385]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044828'; -- 修正设备[TMP00044828]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045522'; -- 修正设备[TMP00045522]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045410'; -- 修正设备[TMP00045410]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043909'; -- 修正设备[TMP00043909]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046140'; -- 修正设备[TMP00046140]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044065'; -- 修正设备[TMP00044065]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045644'; -- 修正设备[TMP00045644]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044889'; -- 修正设备[TMP00044889]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045880'; -- 修正设备[TMP00045880]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045959'; -- 修正设备[TMP00045959]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045826'; -- 修正设备[TMP00045826]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046465'; -- 修正设备[TMP00046465]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045426'; -- 修正设备[TMP00045426]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044256'; -- 修正设备[TMP00044256]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044352'; -- 修正设备[TMP00044352]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046313'; -- 修正设备[TMP00046313]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044905'; -- 修正设备[TMP00044905]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045877'; -- 修正设备[TMP00045877]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045876'; -- 修正设备[TMP00045876]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044309'; -- 修正设备[TMP00044309]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044376'; -- 修正设备[TMP00044376]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044832'; -- 修正设备[TMP00044832]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045456'; -- 修正设备[TMP00045456]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045714'; -- 修正设备[TMP00045714]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044323'; -- 修正设备[TMP00044323]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044072'; -- 修正设备[TMP00044072]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045471'; -- 修正设备[TMP00045471]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044811'; -- 修正设备[TMP00044811]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046430'; -- 修正设备[TMP00046430]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045587'; -- 修正设备[TMP00045587]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046522'; -- 修正设备[TMP00046522]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045304'; -- 修正设备[TMP00045304]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045983'; -- 修正设备[TMP00045983]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045394'; -- 修正设备[TMP00045394]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044794'; -- 修正设备[TMP00044794]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046472'; -- 修正设备[TMP00046472]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044364'; -- 修正设备[TMP00044364]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044293'; -- 修正设备[TMP00044293]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045764'; -- 修正设备[TMP00045764]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046579'; -- 修正设备[TMP00046579]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045376'; -- 修正设备[TMP00045376]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046114'; -- 修正设备[TMP00046114]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045494'; -- 修正设备[TMP00045494]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045822'; -- 修正设备[TMP00045822]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044324'; -- 修正设备[TMP00044324]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045990'; -- 修正设备[TMP00045990]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044372'; -- 修正设备[TMP00044372]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045860'; -- 修正设备[TMP00045860]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045335'; -- 修正设备[TMP00045335]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045640'; -- 修正设备[TMP00045640]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046565'; -- 修正设备[TMP00046565]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046016'; -- 修正设备[TMP00046016]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045010'; -- 修正设备[TMP00045010]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046481'; -- 修正设备[TMP00046481]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044914'; -- 修正设备[TMP00044914]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044169'; -- 修正设备[TMP00044169]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046588'; -- 修正设备[TMP00046588]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044967'; -- 修正设备[TMP00044967]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046154'; -- 修正设备[TMP00046154]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044915'; -- 修正设备[TMP00044915]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045559'; -- 修正设备[TMP00045559]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045312'; -- 修正设备[TMP00045312]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046365'; -- 修正设备[TMP00046365]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045600'; -- 修正设备[TMP00045600]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045068'; -- 修正设备[TMP00045068]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044948'; -- 修正设备[TMP00044948]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045892'; -- 修正设备[TMP00045892]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045737'; -- 修正设备[TMP00045737]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045827'; -- 修正设备[TMP00045827]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045421'; -- 修正设备[TMP00045421]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044954'; -- 修正设备[TMP00044954]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045652'; -- 修正设备[TMP00045652]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046022'; -- 修正设备[TMP00046022]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044884'; -- 修正设备[TMP00044884]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044780'; -- 修正设备[TMP00044780]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045301'; -- 修正设备[TMP00045301]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044802'; -- 修正设备[TMP00044802]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045733'; -- 修正设备[TMP00045733]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044922'; -- 修正设备[TMP00044922]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045038'; -- 修正设备[TMP00045038]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045746'; -- 修正设备[TMP00045746]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046348'; -- 修正设备[TMP00046348]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044983'; -- 修正设备[TMP00044983]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045569'; -- 修正设备[TMP00045569]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046335'; -- 修正设备[TMP00046335]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045722'; -- 修正设备[TMP00045722]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045008'; -- 修正设备[TMP00045008]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045420'; -- 修正设备[TMP00045420]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046352'; -- 修正设备[TMP00046352]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045791'; -- 修正设备[TMP00045791]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044274'; -- 修正设备[TMP00044274]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045619'; -- 修正设备[TMP00045619]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045868'; -- 修正设备[TMP00045868]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045397'; -- 修正设备[TMP00045397]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044842'; -- 修正设备[TMP00044842]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046362'; -- 修正设备[TMP00046362]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044281'; -- 修正设备[TMP00044281]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044330'; -- 修正设备[TMP00044330]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045293'; -- 修正设备[TMP00045293]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045292'; -- 修正设备[TMP00045292]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044340'; -- 修正设备[TMP00044340]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044921'; -- 修正设备[TMP00044921]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046437'; -- 修正设备[TMP00046437]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045638'; -- 修正设备[TMP00045638]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044138'; -- 修正设备[TMP00044138]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044990'; -- 修正设备[TMP00044990]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044327'; -- 修正设备[TMP00044327]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045514'; -- 修正设备[TMP00045514]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044128'; -- 修正设备[TMP00044128]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046589'; -- 修正设备[TMP00046589]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046416'; -- 修正设备[TMP00046416]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044807'; -- 修正设备[TMP00044807]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045440'; -- 修正设备[TMP00045440]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044969'; -- 修正设备[TMP00044969]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045296'; -- 修正设备[TMP00045296]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045838'; -- 修正设备[TMP00045838]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044783'; -- 修正设备[TMP00044783]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045725'; -- 修正设备[TMP00045725]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044782'; -- 修正设备[TMP00044782]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045323'; -- 修正设备[TMP00045323]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044207'; -- 修正设备[TMP00044207]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045782'; -- 修正设备[TMP00045782]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045576'; -- 修正设备[TMP00045576]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045774'; -- 修正设备[TMP00045774]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046013'; -- 修正设备[TMP00046013]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045778'; -- 修正设备[TMP00045778]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045859'; -- 修正设备[TMP00045859]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045551'; -- 修正设备[TMP00045551]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044067'; -- 修正设备[TMP00044067]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045086'; -- 修正设备[TMP00045086]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044992'; -- 修正设备[TMP00044992]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045449'; -- 修正设备[TMP00045449]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046108'; -- 修正设备[TMP00046108]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045347'; -- 修正设备[TMP00045347]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046470'; -- 修正设备[TMP00046470]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044362'; -- 修正设备[TMP00044362]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044803'; -- 修正设备[TMP00044803]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045758'; -- 修正设备[TMP00045758]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046598'; -- 修正设备[TMP00046598]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044981'; -- 修正设备[TMP00044981]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046592'; -- 修正设备[TMP00046592]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045773'; -- 修正设备[TMP00045773]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045841'; -- 修正设备[TMP00045841]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044354'; -- 修正设备[TMP00044354]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046337'; -- 修正设备[TMP00046337]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045496'; -- 修正设备[TMP00045496]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046333'; -- 修正设备[TMP00046333]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045962'; -- 修正设备[TMP00045962]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043901'; -- 修正设备[TMP00043901]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044924'; -- 修正设备[TMP00044924]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046124'; -- 修正设备[TMP00046124]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045340'; -- 修正设备[TMP00045340]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046112'; -- 修正设备[TMP00046112]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046477'; -- 修正设备[TMP00046477]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045434'; -- 修正设备[TMP00045434]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044344'; -- 修正设备[TMP00044344]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044840'; -- 修正设备[TMP00044840]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045681'; -- 修正设备[TMP00045681]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045351'; -- 修正设备[TMP00045351]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044930'; -- 修正设备[TMP00044930]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045332'; -- 修正设备[TMP00045332]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045697'; -- 修正设备[TMP00045697]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046474'; -- 修正设备[TMP00046474]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045040'; -- 修正设备[TMP00045040]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044977'; -- 修正设备[TMP00044977]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046338'; -- 修正设备[TMP00046338]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044826'; -- 修正设备[TMP00044826]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045454'; -- 修正设备[TMP00045454]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044887'; -- 修正设备[TMP00044887]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044303'; -- 修正设备[TMP00044303]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045412'; -- 修正设备[TMP00045412]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044881'; -- 修正设备[TMP00044881]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046590'; -- 修正设备[TMP00046590]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045811'; -- 修正设备[TMP00045811]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045377'; -- 修正设备[TMP00045377]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044975'; -- 修正设备[TMP00044975]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045584'; -- 修正设备[TMP00045584]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044275'; -- 修正设备[TMP00044275]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044906'; -- 修正设备[TMP00044906]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045036'; -- 修正设备[TMP00045036]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045940'; -- 修正设备[TMP00045940]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044850'; -- 修正设备[TMP00044850]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045437'; -- 修正设备[TMP00045437]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045745'; -- 修正设备[TMP00045745]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044271'; -- 修正设备[TMP00044271]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045336'; -- 修正设备[TMP00045336]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045857'; -- 修正设备[TMP00045857]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044313'; -- 修正设备[TMP00044313]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045072'; -- 修正设备[TMP00045072]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046463'; -- 修正设备[TMP00046463]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045741'; -- 修正设备[TMP00045741]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044341'; -- 修正设备[TMP00044341]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044283'; -- 修正设备[TMP00044283]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043897'; -- 修正设备[TMP00043897]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044892'; -- 修正设备[TMP00044892]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046418'; -- 修正设备[TMP00046418]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046451'; -- 修正设备[TMP00046451]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046449'; -- 修正设备[TMP00046449]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045424'; -- 修正设备[TMP00045424]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045649'; -- 修正设备[TMP00045649]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044787'; -- 修正设备[TMP00044787]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045505'; -- 修正设备[TMP00045505]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044888'; -- 修正设备[TMP00044888]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045768'; -- 修正设备[TMP00045768]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045520'; -- 修正设备[TMP00045520]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046320'; -- 修正设备[TMP00046320]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045615'; -- 修正设备[TMP00045615]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045706'; -- 修正设备[TMP00045706]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044955'; -- 修正设备[TMP00044955]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045463'; -- 修正设备[TMP00045463]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044292'; -- 修正设备[TMP00044292]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045021'; -- 修正设备[TMP00045021]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044059'; -- 修正设备[TMP00044059]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046149'; -- 修正设备[TMP00046149]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044833'; -- 修正设备[TMP00044833]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045348'; -- 修正设备[TMP00045348]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044767'; -- 修正设备[TMP00044767]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045430'; -- 修正设备[TMP00045430]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044964'; -- 修正设备[TMP00044964]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045618'; -- 修正设备[TMP00045618]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045659'; -- 修正设备[TMP00045659]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045080'; -- 修正设备[TMP00045080]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045739'; -- 修正设备[TMP00045739]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044519'; -- 修正设备[TMP00044519]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044355'; -- 修正设备[TMP00044355]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045775'; -- 修正设备[TMP00045775]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044789'; -- 修正设备[TMP00044789]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044107'; -- 修正设备[TMP00044107]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045975'; -- 修正设备[TMP00045975]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044077'; -- 修正设备[TMP00044077]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044375'; -- 修正设备[TMP00044375]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044106'; -- 修正设备[TMP00044106]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045655'; -- 修正设备[TMP00045655]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043893'; -- 修正设备[TMP00043893]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045413'; -- 修正设备[TMP00045413]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046145'; -- 修正设备[TMP00046145]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045310'; -- 修正设备[TMP00045310]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046462'; -- 修正设备[TMP00046462]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045609'; -- 修正设备[TMP00045609]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045346'; -- 修正设备[TMP00045346]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045495'; -- 修正设备[TMP00045495]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044865'; -- 修正设备[TMP00044865]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046563'; -- 修正设备[TMP00046563]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044961'; -- 修正设备[TMP00044961]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045731'; -- 修正设备[TMP00045731]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046028'; -- 修正设备[TMP00046028]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045355'; -- 修正设备[TMP00045355]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043914'; -- 修正设备[TMP00043914]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045493'; -- 修正设备[TMP00045493]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045448'; -- 修正设备[TMP00045448]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045628'; -- 修正设备[TMP00045628]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046331'; -- 修正设备[TMP00046331]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046583'; -- 修正设备[TMP00046583]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044060'; -- 修正设备[TMP00044060]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046336'; -- 修正设备[TMP00046336]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046021'; -- 修正设备[TMP00046021]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044822'; -- 修正设备[TMP00044822]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046429'; -- 修正设备[TMP00046429]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044973'; -- 修正设备[TMP00044973]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046342'; -- 修正设备[TMP00046342]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044962'; -- 修正设备[TMP00044962]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046587'; -- 修正设备[TMP00046587]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046473'; -- 修正设备[TMP00046473]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045951'; -- 修正设备[TMP00045951]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044246'; -- 修正设备[TMP00044246]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044576'; -- 修正设备[TMP00044576]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045807'; -- 修正设备[TMP00045807]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044333'; -- 修正设备[TMP00044333]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045805'; -- 修正设备[TMP00045805]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045613'; -- 修正设备[TMP00045613]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045999'; -- 修正设备[TMP00045999]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046471'; -- 修正设备[TMP00046471]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046358'; -- 修正设备[TMP00046358]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045314'; -- 修正设备[TMP00045314]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045631'; -- 修正设备[TMP00045631]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044379'; -- 修正设备[TMP00044379]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045315'; -- 修正设备[TMP00045315]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045031'; -- 修正设备[TMP00045031]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045830'; -- 修正设备[TMP00045830]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044105'; -- 修正设备[TMP00044105]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045582'; -- 修正设备[TMP00045582]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046005'; -- 修正设备[TMP00046005]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044110'; -- 修正设备[TMP00044110]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044332'; -- 修正设备[TMP00044332]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046120'; -- 修正设备[TMP00046120]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046107'; -- 修正设备[TMP00046107]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045051'; -- 修正设备[TMP00045051]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045333'; -- 修正设备[TMP00045333]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044926'; -- 修正设备[TMP00044926]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045897'; -- 修正设备[TMP00045897]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045946'; -- 修正设备[TMP00045946]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045303'; -- 修正设备[TMP00045303]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046412'; -- 修正设备[TMP00046412]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045464'; -- 修正设备[TMP00045464]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044830'; -- 修正设备[TMP00044830]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045637'; -- 修正设备[TMP00045637]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044301'; -- 修正设备[TMP00044301]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045616'; -- 修正设备[TMP00045616]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045295'; -- 修正设备[TMP00045295]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046307'; -- 修正设备[TMP00046307]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045806'; -- 修正设备[TMP00045806]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045391'; -- 修正设备[TMP00045391]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044348'; -- 修正设备[TMP00044348]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045523'; -- 修正设备[TMP00045523]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045881'; -- 修正设备[TMP00045881]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045973'; -- 修正设备[TMP00045973]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045387'; -- 修正设备[TMP00045387]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044942'; -- 修正设备[TMP00044942]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046428'; -- 修正设备[TMP00046428]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045506'; -- 修正设备[TMP00045506]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045893'; -- 修正设备[TMP00045893]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046146'; -- 修正设备[TMP00046146]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045431'; -- 修正设备[TMP00045431]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044308'; -- 修正设备[TMP00044308]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044805'; -- 修正设备[TMP00044805]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046351'; -- 修正设备[TMP00046351]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045715'; -- 修正设备[TMP00045715]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045657'; -- 修正设备[TMP00045657]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045642'; -- 修正设备[TMP00045642]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045518'; -- 修正设备[TMP00045518]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045042'; -- 修正设备[TMP00045042]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046159'; -- 修正设备[TMP00046159]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044021'; -- 修正设备[TMP00044021]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044825'; -- 修正设备[TMP00044825]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045481'; -- 修正设备[TMP00045481]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044328'; -- 修正设备[TMP00044328]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044999'; -- 修正设备[TMP00044999]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045596'; -- 修正设备[TMP00045596]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045754'; -- 修正设备[TMP00045754]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045474'; -- 修正设备[TMP00045474]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046366'; -- 修正设备[TMP00046366]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045625'; -- 修正设备[TMP00045625]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046586'; -- 修正设备[TMP00046586]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044211'; -- 修正设备[TMP00044211]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045665'; -- 修正设备[TMP00045665]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044952'; -- 修正设备[TMP00044952]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045073'; -- 修正设备[TMP00045073]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044111'; -- 修正设备[TMP00044111]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045998'; -- 修正设备[TMP00045998]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045611'; -- 修正设备[TMP00045611]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046025'; -- 修正设备[TMP00046025]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045832'; -- 修正设备[TMP00045832]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044845'; -- 修正设备[TMP00044845]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046151'; -- 修正设备[TMP00046151]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044852'; -- 修正设备[TMP00044852]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045399'; -- 修正设备[TMP00045399]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043904'; -- 修正设备[TMP00043904]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045871'; -- 修正设备[TMP00045871]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045960'; -- 修正设备[TMP00045960]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046126'; -- 修正设备[TMP00046126]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045950'; -- 修正设备[TMP00045950]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045650'; -- 修正设备[TMP00045650]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045886'; -- 修正设备[TMP00045886]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044769'; -- 修正设备[TMP00044769]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045442'; -- 修正设备[TMP00045442]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045786'; -- 修正设备[TMP00045786]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045610'; -- 修正设备[TMP00045610]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045475'; -- 修正设备[TMP00045475]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046029'; -- 修正设备[TMP00046029]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044971'; -- 修正设备[TMP00044971]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044996'; -- 修正设备[TMP00044996]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044873'; -- 修正设备[TMP00044873]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044810'; -- 修正设备[TMP00044810]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045776'; -- 修正设备[TMP00045776]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046360'; -- 修正设备[TMP00046360]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045070'; -- 修正设备[TMP00045070]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044253'; -- 修正设备[TMP00044253]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044108'; -- 修正设备[TMP00044108]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045803'; -- 修正设备[TMP00045803]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046312'; -- 修正设备[TMP00046312]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045932'; -- 修正设备[TMP00045932]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044776'; -- 修正设备[TMP00044776]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045839'; -- 修正设备[TMP00045839]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044266'; -- 修正设备[TMP00044266]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044530'; -- 修正设备[TMP00044530]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046422'; -- 修正设备[TMP00046422]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045597'; -- 修正设备[TMP00045597]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045717'; -- 修正设备[TMP00045717]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046441'; -- 修正设备[TMP00046441]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045968'; -- 修正设备[TMP00045968]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045499'; -- 修正设备[TMP00045499]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044078'; -- 修正设备[TMP00044078]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044305'; -- 修正设备[TMP00044305]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045818'; -- 修正设备[TMP00045818]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045845'; -- 修正设备[TMP00045845]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045836'; -- 修正设备[TMP00045836]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045400'; -- 修正设备[TMP00045400]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046134'; -- 修正设备[TMP00046134]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045082'; -- 修正设备[TMP00045082]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044450'; -- 修正设备[TMP00044450]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044310'; -- 修正设备[TMP00044310]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046582'; -- 修正设备[TMP00046582]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045570'; -- 修正设备[TMP00045570]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044298'; -- 修正设备[TMP00044298]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045573'; -- 修正设备[TMP00045573]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045635'; -- 修正设备[TMP00045635]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045311'; -- 修正设备[TMP00045311]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045087'; -- 修正设备[TMP00045087]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044908'; -- 修正设备[TMP00044908]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045704'; -- 修正设备[TMP00045704]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044316'; -- 修正设备[TMP00044316]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046414'; -- 修正设备[TMP00046414]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045800'; -- 修正设备[TMP00045800]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045526'; -- 修正设备[TMP00045526]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045869'; -- 修正设备[TMP00045869]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046484'; -- 修正设备[TMP00046484]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043918'; -- 修正设备[TMP00043918]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045552'; -- 修正设备[TMP00045552]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044858'; -- 修正设备[TMP00044858]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045840'; -- 修正设备[TMP00045840]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046572'; -- 修正设备[TMP00046572]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045588'; -- 修正设备[TMP00045588]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044823'; -- 修正设备[TMP00044823]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046599'; -- 修正设备[TMP00046599]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044970'; -- 修正设备[TMP00044970]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044993'; -- 修正设备[TMP00044993]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045485'; -- 修正设备[TMP00045485]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046014'; -- 修正设备[TMP00046014]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045646'; -- 修正设备[TMP00045646]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045503'; -- 修正设备[TMP00045503]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045395'; -- 修正设备[TMP00045395]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044262'; -- 修正设备[TMP00044262]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046158'; -- 修正设备[TMP00046158]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044885'; -- 修正设备[TMP00044885]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045882'; -- 修正设备[TMP00045882]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045900'; -- 修正设备[TMP00045900]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044320'; -- 修正设备[TMP00044320]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045459'; -- 修正设备[TMP00045459]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045641'; -- 修正设备[TMP00045641]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045003'; -- 修正设备[TMP00045003]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044879'; -- 修正设备[TMP00044879]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045693'; -- 修正设备[TMP00045693]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044910'; -- 修正设备[TMP00044910]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045477'; -- 修正设备[TMP00045477]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045790'; -- 修正设备[TMP00045790]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044300'; -- 修正设备[TMP00044300]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046593'; -- 修正设备[TMP00046593]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046109'; -- 修正设备[TMP00046109]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045390'; -- 修正设备[TMP00045390]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045687'; -- 修正设备[TMP00045687]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046345'; -- 修正设备[TMP00046345]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045784'; -- 修正设备[TMP00045784]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045422'; -- 修正设备[TMP00045422]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045759'; -- 修正设备[TMP00045759]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045381'; -- 修正设备[TMP00045381]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045013'; -- 修正设备[TMP00045013]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044061'; -- 修正设备[TMP00044061]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045502'; -- 修正设备[TMP00045502]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045666'; -- 修正设备[TMP00045666]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045439'; -- 修正设备[TMP00045439]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046123'; -- 修正设备[TMP00046123]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045577'; -- 修正设备[TMP00045577]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044878'; -- 修正设备[TMP00044878]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046147'; -- 修正设备[TMP00046147]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045025'; -- 修正设备[TMP00045025]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045462'; -- 修正设备[TMP00045462]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045368'; -- 修正设备[TMP00045368]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046115'; -- 修正设备[TMP00046115]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045321'; -- 修正设备[TMP00045321]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044369'; -- 修正设备[TMP00044369]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045533'; -- 修正设备[TMP00045533]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044208'; -- 修正设备[TMP00044208]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046113'; -- 修正设备[TMP00046113]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044877'; -- 修正设备[TMP00044877]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045064'; -- 修正设备[TMP00045064]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044286'; -- 修正设备[TMP00044286]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044304'; -- 修正设备[TMP00044304]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045372'; -- 修正设备[TMP00045372]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044960'; -- 修正设备[TMP00044960]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045045'; -- 修正设备[TMP00045045]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044132'; -- 修正设备[TMP00044132]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044781'; -- 修正设备[TMP00044781]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046567'; -- 修正设备[TMP00046567]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045802'; -- 修正设备[TMP00045802]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045752'; -- 修正设备[TMP00045752]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045996'; -- 修正设备[TMP00045996]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043899'; -- 修正设备[TMP00043899]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045586'; -- 修正设备[TMP00045586]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045753'; -- 修正设备[TMP00045753]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044317'; -- 修正设备[TMP00044317]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045651'; -- 修正设备[TMP00045651]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045701'; -- 修正设备[TMP00045701]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046603'; -- 修正设备[TMP00046603]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045290'; -- 修正设备[TMP00045290]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044816'; -- 修正设备[TMP00044816]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045771'; -- 修正设备[TMP00045771]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044531'; -- 修正设备[TMP00044531]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043911'; -- 修正设备[TMP00043911]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045821'; -- 修正设备[TMP00045821]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045482'; -- 修正设备[TMP00045482]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043912'; -- 修正设备[TMP00043912]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044343'; -- 修正设备[TMP00044343]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045014'; -- 修正设备[TMP00045014]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045341'; -- 修正设备[TMP00045341]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046364'; -- 修正设备[TMP00046364]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045656'; -- 修正设备[TMP00045656]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045636'; -- 修正设备[TMP00045636]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045361'; -- 修正设备[TMP00045361]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045063'; -- 修正设备[TMP00045063]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044553'; -- 修正设备[TMP00044553]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045691'; -- 修正设备[TMP00045691]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046139'; -- 修正设备[TMP00046139]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046133'; -- 修正设备[TMP00046133]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045958'; -- 修正设备[TMP00045958]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046591'; -- 修正设备[TMP00046591]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043913'; -- 修正设备[TMP00043913]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045447'; -- 修正设备[TMP00045447]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045994'; -- 修正设备[TMP00045994]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044856'; -- 修正设备[TMP00044856]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044812'; -- 修正设备[TMP00044812]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046597'; -- 修正设备[TMP00046597]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045585'; -- 修正设备[TMP00045585]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044247'; -- 修正设备[TMP00044247]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045632'; -- 修正设备[TMP00045632]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045966'; -- 修正设备[TMP00045966]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045532'; -- 修正设备[TMP00045532]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046361'; -- 修正设备[TMP00046361]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045058'; -- 修正设备[TMP00045058]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044937'; -- 修正设备[TMP00044937]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046346'; -- 修正设备[TMP00046346]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045406'; -- 修正设备[TMP00045406]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045762'; -- 修正设备[TMP00045762]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043905'; -- 修正设备[TMP00043905]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045498'; -- 修正设备[TMP00045498]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044103'; -- 修正设备[TMP00044103]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044863'; -- 修正设备[TMP00044863]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046309'; -- 修正设备[TMP00046309]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045579'; -- 修正设备[TMP00045579]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045627'; -- 修正设备[TMP00045627]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045542'; -- 修正设备[TMP00045542]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045899'; -- 修正设备[TMP00045899]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045668'; -- 修正设备[TMP00045668]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044916'; -- 修正设备[TMP00044916]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045468'; -- 修正设备[TMP00045468]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044276'; -- 修正设备[TMP00044276]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045382'; -- 修正设备[TMP00045382]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045898'; -- 修正设备[TMP00045898]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046478'; -- 修正设备[TMP00046478]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044774'; -- 修正设备[TMP00044774]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044988'; -- 修正设备[TMP00044988]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045661'; -- 修正设备[TMP00045661]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044895'; -- 修正设备[TMP00044895]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044974'; -- 修正设备[TMP00044974]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044254'; -- 修正设备[TMP00044254]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046155'; -- 修正设备[TMP00046155]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044251'; -- 修正设备[TMP00044251]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046367'; -- 修正设备[TMP00046367]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045476'; -- 修正设备[TMP00045476]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046118'; -- 修正设备[TMP00046118]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046523'; -- 修正设备[TMP00046523]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044381'; -- 修正设备[TMP00044381]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044809'; -- 修正设备[TMP00044809]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045707'; -- 修正设备[TMP00045707]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046357'; -- 修正设备[TMP00046357]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044958'; -- 修正设备[TMP00044958]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045634'; -- 修正设备[TMP00045634]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044792'; -- 修正设备[TMP00044792]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045894'; -- 修正设备[TMP00045894]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046350'; -- 修正设备[TMP00046350]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045987'; -- 修正设备[TMP00045987]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044900'; -- 修正设备[TMP00044900]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045461'; -- 修正设备[TMP00045461]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045592'; -- 修正设备[TMP00045592]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045933'; -- 修正设备[TMP00045933]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046425'; -- 修正设备[TMP00046425]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045978'; -- 修正设备[TMP00045978]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045029'; -- 修正设备[TMP00045029]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045939'; -- 修正设备[TMP00045939]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045947'; -- 修正设备[TMP00045947]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045316'; -- 修正设备[TMP00045316]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046327'; -- 修正设备[TMP00046327]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045541'; -- 修正设备[TMP00045541]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044920'; -- 修正设备[TMP00044920]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045353'; -- 修正设备[TMP00045353]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045334'; -- 修正设备[TMP00045334]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045560'; -- 修正设备[TMP00045560]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045028'; -- 修正设备[TMP00045028]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045765'; -- 修正设备[TMP00045765]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046498'; -- 修正设备[TMP00046498]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045313'; -- 修正设备[TMP00045313]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045378'; -- 修正设备[TMP00045378]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045299'; -- 修正设备[TMP00045299]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044069'; -- 修正设备[TMP00044069]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044360'; -- 修正设备[TMP00044360]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044140'; -- 修正设备[TMP00044140]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045076'; -- 修正设备[TMP00045076]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046310'; -- 修正设备[TMP00046310]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046130'; -- 修正设备[TMP00046130]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043915'; -- 修正设备[TMP00043915]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045956'; -- 修正设备[TMP00045956]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044296'; -- 修正设备[TMP00044296]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045373'; -- 修正设备[TMP00045373]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044562'; -- 修正设备[TMP00044562]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045735'; -- 修正设备[TMP00045735]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045319'; -- 修正设备[TMP00045319]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045349'; -- 修正设备[TMP00045349]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045398'; -- 修正设备[TMP00045398]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045645'; -- 修正设备[TMP00045645]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044294'; -- 修正设备[TMP00044294]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045780'; -- 修正设备[TMP00045780]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043906'; -- 修正设备[TMP00043906]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045855'; -- 修正设备[TMP00045855]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043919'; -- 修正设备[TMP00043919]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045783'; -- 修正设备[TMP00045783]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044869'; -- 修正设备[TMP00044869]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045362'; -- 修正设备[TMP00045362]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046003'; -- 修正设备[TMP00046003]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045849'; -- 修正设备[TMP00045849]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045511'; -- 修正设备[TMP00045511]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00043892'; -- 修正设备[TMP00043892]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044529'; -- 修正设备[TMP00044529]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045710'; -- 修正设备[TMP00045710]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044249'; -- 修正设备[TMP00044249]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044373'; -- 修正设备[TMP00044373]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045408'; -- 修正设备[TMP00045408]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045328'; -- 修正设备[TMP00045328]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046495'; -- 修正设备[TMP00046495]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045486'; -- 修正设备[TMP00045486]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044939'; -- 修正设备[TMP00044939]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00044518'; -- 修正设备[TMP00044518]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00046325'; -- 修正设备[TMP00046325]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045525'; -- 修正设备[TMP00045525]的电压逻辑属性为 1010
UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='1010' WHERE EQUIP_ID='TMP00045534'; -- 修正设备[TMP00045534]的电压逻辑属性为 1010
>>>>>>> origin/main


-- 2. 逆向回滚SQL脚本
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 无
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚动作：删除SVG中补画的图元与标注。
-- 回滚：Q49禁止DELETE且PWEQUIPINFO无状态列，需人工核对后删除该INSERT行。
-- 回滚：Q49禁止DELETE且PWEQUIPINFO无状态列，需人工核对后删除该INSERT行。
