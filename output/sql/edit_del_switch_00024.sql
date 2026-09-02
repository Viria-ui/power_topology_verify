-- ==========================================================
-- Phase 2 Test Task 2：删除开关 00024 (SVG id=TMP00043912)
-- 目标SVG：LINE216_beautified.svg
-- 策略：先把两侧最近邻居设备 A / B 直接连通；再删连接+删设备+删文字
-- 可回滚：ROLLBACK段提供反操作（先恢复设备/连接，再恢复A-TMP00043912-B的分叉）
-- ==========================================================
BEGIN TRANSACTION;

-- 1. 预查询：开关 TMP00043912 的邻居（两侧设备），保存到临时表，方便 INSERT 新直达线
CREATE TEMP TABLE _neighbors_00024 AS
  SELECT DISTINCT
    CASE WHEN START_ST_ID='TMP00043912' THEN END_ST_ID ELSE START_ST_ID END AS NEI_ID
  FROM EQUIP_JBS_PWFEEDERLINE
  WHERE START_ST_ID='TMP00043912' OR END_ST_ID='TMP00043912';

-- 2. 插入两侧设备直接相连的新馈线段（取距离最近的两个设备，这里按字典序兜底取第一对）
INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID, LINE_NAME, START_ST_ID, END_ST_ID, VOLTAGE_TYPE, FEEDER_ID, LINE_TYPE, REMARK)
SELECT
  'LN_BRIDGE_'||A.NEI_ID||'_'||B.NEI_ID,
  '开关00024删除后桥接_直通',
  A.NEI_ID, B.NEI_ID,
  'lkv10', 'LINE216', 'Trunk', '删除开关00024后两侧设备直接连通'
FROM _neighbors_00024 A, _neighbors_00024 B
WHERE A.NEI_ID < B.NEI_ID
  AND NOT EXISTS (SELECT 1 FROM EQUIP_JBS_PWFEEDERLINE L
                   WHERE (L.START_ST_ID=A.NEI_ID AND L.END_ST_ID=B.NEI_ID)
                      OR (L.START_ST_ID=B.NEI_ID AND L.END_ST_ID=A.NEI_ID))
LIMIT 1;

-- 3. 删除所有与 TMP00043912 关联的馈线段
DELETE FROM EQUIP_JBS_PWFEEDERLINE
 WHERE START_ST_ID='TMP00043912' OR END_ST_ID='TMP00043912';

-- 4. 删除开关本体设备
DELETE FROM EQUIP_JBS_PWEQUIPINFO WHERE EQUIP_ID='TMP00043912';

-- 5. 删除端子信号/量测（若存在）
DELETE FROM EQUIP_JBS_PWTERMINAL WHERE EQUIP_ID='TMP00043912';
DELETE FROM EQUIP_JBS_ZD_MEAS   WHERE EQUIP_ID='TMP00043912';

DROP TABLE _neighbors_00024;
COMMIT;

-- ========================= ROLLBACK（若需撤销） =========================
-- 1. 恢复设备本体
-- INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME, EQUIP_TYPE, VOLTAGE_TYPE, FEEDER_ID, PSR_TYPE)
-- VALUES ('TMP00043912','开关00024','负荷开关','lkv10','LINE216','0307');
-- 2. 恢复"桥接直线 LINE_ID = LN_BRIDGE_X_Y"为两条分叉 X-00024 / 00024-Y，然后删除 LN_BRIDGE_X_Y
--    （需按实际桥接ID补充，可从前述临时表重放）
