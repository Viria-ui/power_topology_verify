# -*- coding: utf-8 -*-
"""
SVG美化模块 v2 - 权重树算法集成版（完整功能对齐参考文件 svg_beautifier_v2.py）
基于 SvgDocument IR 解析，内部数据结构与 v2 参考文件完全一致。
修复功能：飞线端点修复 + 拓扑孤岛缝合 + 虚假连接清理
布局功能：权重树梳状布局 + 未入树设备兜底 + 容器纵向排布
渲染功能：正交布线 + 母线加粗 + 标注白底避让 + 符号统一缩放
"""

import os
import re
import copy
import math
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Optional, Set

from data_io.svg_reader import SvgDocument, SvgElement, SvgConnection, SvgText, SVG_NS, XLINK_NS, IEC_NS
from data_io.svg_writer import write_svg

SYMBOL_DEFS_XML = {
    "Breaker_TMP_62d95710-813b-4a92-8dce-35f89dc1c3cd": "<ns0:symbol height=\"3.350000\" id=\"Breaker_TMP_62d95710-813b-4a92-8dce-35f89dc1c3cd\" viewBox=\"0 0 13.100000 3.350000\" width=\"13.100000\">\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-6.500000\" x2=\"-4.000000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:rect fill=\"rgb(255,102,0)\" height=\"3.250000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" width=\"8.000000\" x=\"-4.000000\" y=\"-1.625000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"4.000000\" x2=\"6.500000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"6.500000\" y=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-6.500000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "Disconnector_TMP_54fefde2-8d21-4470-8807-663dab8577b8": "<ns0:symbol height=\"1.444000\" id=\"Disconnector_TMP_54fefde2-8d21-4470-8807-663dab8577b8\" viewBox=\"0 0 9.100000 1.444000\" width=\"9.100000\">\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-4.500000\" x2=\"-1.020000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-1.020000\" x2=\"2.438000\" y1=\"0.000000\" y2=\"-0.844000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.000000\" x2=\"1.980000\" y1=\"-0.719000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.980000\" x2=\"4.500000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"4.500000\" y=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-4.500000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "GroundDisconnector_TMP_0c37fbe3-1b09-41fd-8a4d-38e20bd945d5": "<ns0:symbol height=\"2.975000\" id=\"GroundDisconnector_TMP_0c37fbe3-1b09-41fd-8a4d-38e20bd945d5\" viewBox=\"0 0 6.163000 2.975000\" width=\"6.163000\">\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.000000\" x2=\"-3.000000\" y1=\"-0.500000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-2.500000\" x2=\"-2.500000\" y1=\"-0.938000\" y2=\"1.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-2.000000\" x2=\"-2.000000\" y1=\"-1.438000\" y2=\"1.438000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-2.000000\" x2=\"0.062000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.000000\" x2=\"2.000000\" y1=\"0.000000\" y2=\"-0.625000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.000000\" x2=\"2.000000\" y1=\"-0.656000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.000000\" x2=\"3.062000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"2.875000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "PotentialTransformer_TMP_6946543d-651e-4f1d-97bb-353beeaeaede": "<ns0:symbol height=\"2.100000\" id=\"PotentialTransformer_TMP_6946543d-651e-4f1d-97bb-353beeaeaede\" viewBox=\"0 0 4.975000 2.100000\" width=\"4.975000\">\n      <ns0:circle cx=\"-0.750000\" cy=\"0.000000\" fill=\"none\" r=\"1.000000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:circle cx=\"0.875000\" cy=\"0.000000\" fill=\"none\" r=\"1.000000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.875000\" x2=\"3.125000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"3.063000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "PowerTransformer_TMP_a70da64e-4139-4238-99ff-f38ae7eea01c": "<ns0:symbol height=\"3.1103986278176308\" id=\"PowerTransformer_TMP_a70da64e-4139-4238-99ff-f38ae7eea01c\" viewBox=\"0 0 7.600000001490116 3.1103986278176308\" width=\"7.600000001490116\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(7,164,248)\" stroke-width=\"0.100000\" x1=\"-3.688000\" x2=\"-2.438000\" y1=\"-0.026000\" y2=\"-0.026000\"/>\n      <ns0:circle cx=\"-0.938000\" cy=\"-0.026000\" fill=\"rgb(0,0,0)\" r=\"1.505000\" stroke=\"rgb(7,164,248)\" stroke-width=\"0.100000\"/>\n      <ns0:circle cx=\"1.063000\" cy=\"-0.026000\" fill=\"rgb(0,0,0)\" r=\"1.505000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.563000\" x2=\"3.813000\" y1=\"-0.026000\" y2=\"-0.026000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"3.797000\" y=\"-0.030000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-3.672000\" y=\"-0.030000\"/>\n    </ns0:symbol>",
    "Breaker_TMP_655d2a50-455e-4d8f-95c5-fa3883d8df20": "<ns0:symbol height=\"1.1000000014901161\" id=\"Breaker_TMP_655d2a50-455e-4d8f-95c5-fa3883d8df20\" viewBox=\"0 0 7.108054257929325 1.1000000014901161\" width=\"7.108054257929325\">\n      \n      <ns0:rect fill=\"rgb(255,0,0)\" height=\"0.938000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" width=\"3.000000\" x=\"-1.500000\" y=\"-0.438000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.500000\" x2=\"3.500000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-1.500000\" x2=\"-3.438000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.500000\" x2=\"-3.000000\" y1=\"0.034000\" y2=\"-0.466000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.500000\" x2=\"-3.125000\" y1=\"-0.034000\" y2=\"0.466000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.000000\" x2=\"-2.500000\" y1=\"0.027000\" y2=\"-0.411000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.000000\" x2=\"-2.500000\" y1=\"-0.027000\" y2=\"0.473000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"3.508000\" x2=\"3.092000\" y1=\"0.025000\" y2=\"-0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"3.508000\" x2=\"3.092000\" y1=\"-0.033000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.967000\" x2=\"2.552000\" y1=\"0.025000\" y2=\"-0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.967000\" x2=\"2.552000\" y1=\"-0.033000\" y2=\"0.500000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"3.378000\" y=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-3.419000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "Disconnector_3db3c762-fb9f-4098-826a-52e65e5a7a2c": "<ns0:symbol height=\"1.3187500014901161\" id=\"Disconnector_3db3c762-fb9f-4098-826a-52e65e5a7a2c\" viewBox=\"0 0 9.037500001490116 1.3187500014901161\" width=\"9.037500001490116\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-4.451000\" x2=\"-1.014000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-1.014000\" x2=\"2.156000\" y1=\"0.000000\" y2=\"-0.719000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.984000\" x2=\"1.986000\" y1=\"-0.672000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.986000\" x2=\"4.486000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"4.486000\" y=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-4.451000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "LoadBreakSwitch_357151fb-61fc-46d3-9281-9ff6d1969176": "<ns0:symbol height=\"1.4437500014901161\" id=\"LoadBreakSwitch_357151fb-61fc-46d3-9281-9ff6d1969176\" viewBox=\"0 0 8.100000001490116 1.4437500014901161\" width=\"8.100000001490116\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-4.000000\" x2=\"-1.500000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-1.500000\" x2=\"1.531000\" y1=\"0.000000\" y2=\"-0.656000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.500000\" x2=\"1.500000\" y1=\"-0.844000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.500000\" x2=\"4.000000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:circle cx=\"1.063000\" cy=\"0.000000\" fill=\"rgb(0,0,0)\" r=\"0.400000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"4.000000\" y=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-4.000000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "GroundDisconnector_7112302c-991f-4ffe-a6a5-dc3a26fef7de": "<ns0:symbol height=\"2.975000001490116\" id=\"GroundDisconnector_7112302c-991f-4ffe-a6a5-dc3a26fef7de\" viewBox=\"0 0 6.162500001490116 2.975000001490116\" width=\"6.162500001490116\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.000000\" x2=\"-3.000000\" y1=\"-0.500000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-2.500000\" x2=\"-2.500000\" y1=\"-0.938000\" y2=\"1.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-2.000000\" x2=\"-2.000000\" y1=\"-1.438000\" y2=\"1.438000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-2.000000\" x2=\"0.063000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.000000\" x2=\"2.000000\" y1=\"0.000000\" y2=\"-0.625000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.000000\" x2=\"2.000000\" y1=\"-0.656000\" y2=\"0.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.000000\" x2=\"3.063000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"2.875000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "Fuse_6f477905-e141-4423-8160-7b6e8537ec92": "<ns0:symbol height=\"2.6193702705204487\" id=\"Fuse_6f477905-e141-4423-8160-7b6e8537ec92\" viewBox=\"0 0 8.642764665186405 2.6193702705204487\" width=\"8.642764665186405\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-4.250000\" x2=\"-0.957000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-0.957000\" x2=\"2.043000\" y1=\"0.000000\" y2=\"-1.500000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.813000\" x2=\"1.793000\" y1=\"-1.125000\" y2=\"0.625000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.793000\" x2=\"4.293000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:polygon fill=\"rgb(255,255,255)\" points=\"-0.33223533630371094,-0.6875 0.04276466369628906,0.0 1.792764663696289,-0.9375 1.417764663696289,-1.625\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:polygon fill=\"rgb(255,0,0)\" points=\"0.16776466369628906,-1.9375 0.6052646636962891,-1.6875 0.10526466369628906,-1.4375\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.543000\" x2=\"0.418000\" y1=\"-1.250000\" y2=\"-1.500000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"4.250000\" y=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-4.250000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "SurgeArrester_f4d15417-154b-4802-9a0d-eaa46f6f049d": "<ns0:symbol height=\"2.100000001490116\" id=\"SurgeArrester_f4d15417-154b-4802-9a0d-eaa46f6f049d\" viewBox=\"0 0 12.100000001490116 2.100000001490116\" width=\"12.100000001490116\">\n      \n      <ns0:rect fill=\"rgb(0,0,0)\" height=\"2.000000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" width=\"6.000000\" x=\"-3.000000\" y=\"-1.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.000000\" x2=\"-6.000000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.188000\" x2=\"6.000000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:polygon fill=\"rgb(255,0,0)\" points=\"1.1875,0.0 2.1875,-0.4375 2.1875,0.4375\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"5.966000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "PowerTransformer_TMP_19fcbd00-197e-482a-a960-fe7a828130a1": "<ns0:symbol height=\"3.1103986278176308\" id=\"PowerTransformer_TMP_19fcbd00-197e-482a-a960-fe7a828130a1\" viewBox=\"0 0 7.600000001490116 3.1103986278176308\" width=\"7.600000001490116\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(7,164,248)\" stroke-width=\"0.100000\" x1=\"-3.688000\" x2=\"-2.438000\" y1=\"-0.026000\" y2=\"-0.026000\"/>\n      <ns0:circle cx=\"-0.938000\" cy=\"-0.026000\" fill=\"rgb(0,0,0)\" r=\"1.505000\" stroke=\"rgb(7,164,248)\" stroke-width=\"0.100000\"/>\n      <ns0:circle cx=\"1.063000\" cy=\"-0.026000\" fill=\"rgb(0,0,0)\" r=\"1.505000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"2.563000\" x2=\"3.813000\" y1=\"-0.026000\" y2=\"-0.026000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"3.797000\" y=\"-0.030000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"-3.672000\" y=\"-0.030000\"/>\n    </ns0:symbol>",
    "PotentialTransformer_a6f46c6a-ace4-43ea-9973-b5f94576d3c9": "<ns0:symbol height=\"2.100000001490116\" id=\"PotentialTransformer_a6f46c6a-ace4-43ea-9973-b5f94576d3c9\" viewBox=\"0 0 4.975000001490116 2.100000001490116\" width=\"4.975000001490116\">\n      \n      <ns0:circle cx=\"-0.750000\" cy=\"0.000000\" fill=\"rgb(0,0,0)\" r=\"1.000000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:circle cx=\"0.875000\" cy=\"0.000000\" fill=\"rgb(0,0,0)\" r=\"1.000000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.875000\" x2=\"3.125000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"3.063000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "CurrentTransformer_9119054a-1e83-4003-a946-a83406c03d83": "<ns0:symbol height=\"8.100000001490116\" id=\"CurrentTransformer_9119054a-1e83-4003-a946-a83406c03d83\" viewBox=\"0 0 6.100000001490116 8.100000001490116\" width=\"6.100000001490116\">\n      \n      <ns0:circle cx=\"0.000000\" cy=\"-2.938000\" fill=\"rgb(0,0,0)\" r=\"1.000000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.063000\" x2=\"2.938000\" y1=\"-2.938000\" y2=\"-2.938000\"/>\n      <ns0:circle cx=\"0.000000\" cy=\"0.063000\" fill=\"rgb(0,0,0)\" r=\"0.938000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.000000\" x2=\"2.938000\" y1=\"0.063000\" y2=\"0.063000\"/>\n      <ns0:circle cx=\"0.000000\" cy=\"3.063000\" fill=\"rgb(0,0,0)\" r=\"1.000000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-3.063000\" x2=\"2.938000\" y1=\"3.063000\" y2=\"3.063000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"0.000000\" y=\"0.063000\"/>\n    </ns0:symbol>",
    "EnergyConsumer_3dba839c-4394-4b87-9ef4-dae464753604": "<ns0:symbol height=\"6.975000001490116\" id=\"EnergyConsumer_3dba839c-4394-4b87-9ef4-dae464753604\" viewBox=\"0 0 6.975000001490116 6.975000001490116\" width=\"6.975000001490116\">\n      \n      <ns0:circle cx=\"0.000000\" cy=\"0.000000\" fill=\"rgb(0,0,0)\" r=\"3.438000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:text dy=\".3em\" fill=\"rgb(255,255,255)\" font-family=\"Dialog\" font-size=\"2.0\" style=\"text-anchor:middle\" x=\"-0.191000\" y=\"0.101000\">J</ns0:text>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"0.000000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "PoleCode_da3c5ac4-fbe8-4e62-bfb3-5eab3768a97a": "<ns0:symbol height=\"3.004863739013672\" id=\"PoleCode_da3c5ac4-fbe8-4e62-bfb3-5eab3768a97a\" viewBox=\"0 0 3.000000 3.004863739013672\" width=\"3.000000\">\n      \n      <ns0:circle cx=\"0.000000\" cy=\"0.016000\" fill=\"rgb(153,153,153)\" r=\"1.500000\" stroke=\"rgb(255,255,255)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,255,255)\" stroke-width=\"0.100000\" x1=\"-0.109000\" x2=\"1.344000\" y1=\"1.516000\" y2=\"-0.641000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,255,255)\" stroke-width=\"0.100000\" x1=\"0.828000\" x2=\"-0.813000\" y1=\"-1.219000\" y2=\"1.266000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,255,255)\" stroke-width=\"0.100000\" x1=\"-1.344000\" x2=\"0.172000\" y1=\"0.656000\" y2=\"-1.469000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"0.000000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "Junction_03ae4dd6-c087-42d2-82de-7a7c43b048e8": "<ns0:symbol height=\"2.100000001490116\" id=\"Junction_03ae4dd6-c087-42d2-82de-7a7c43b048e8\" viewBox=\"0 0 2.850000001490116 2.100000001490116\" width=\"2.850000001490116\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-1.375000\" x2=\"0.000000\" y1=\"0.000000\" y2=\"-1.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.000000\" x2=\"1.375000\" y1=\"-1.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"1.375000\" x2=\"0.000000\" y1=\"0.000000\" y2=\"1.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-1.375000\" x2=\"0.000000\" y1=\"0.000000\" y2=\"1.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.000000\" x2=\"0.000000\" y1=\"-1.000000\" y2=\"1.000000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"0.000000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "RemoteUnit_fbc2500e-a96b-4f29-9089-7a3b05ca7c82": "<ns0:symbol height=\"10.100000001490116\" id=\"RemoteUnit_fbc2500e-a96b-4f29-9089-7a3b05ca7c82\" viewBox=\"0 0 9.287500001490116 10.100000001490116\" width=\"9.287500001490116\">\n      \n      <ns0:circle cx=\"0.000000\" cy=\"0.000000\" fill=\"rgb(0,0,0)\" r=\"3.942000\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"4.938000\" x2=\"-3.063000\" y1=\"0.000000\" y2=\"0.000000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.000000\" x2=\"0.000000\" y1=\"-5.000000\" y2=\"5.000000\"/>\n      <ns0:polygon fill=\"rgb(255,0,0)\" points=\"-4.25,0.0 -3.1875,-0.4375 -3.1875,0.375 -3.1875,0.375\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"0.000000\" y=\"0.000000\"/>\n    </ns0:symbol>",
    "Other_e34f9d8c-702c-415a-989e-414563b32fb5": "<ns0:symbol height=\"0.2471216917037964\" id=\"Other_e34f9d8c-702c-415a-989e-414563b32fb5\" viewBox=\"0 0 0.2471216917037964 0.2471216917037964\" width=\"0.2471216917037964\">\n      \n      <ns0:circle cx=\"0.003000\" cy=\"0.003000\" fill=\"rgb(255,0,0)\" r=\"0.122000\" stroke=\"rgb(255,255,255)\" stroke-width=\"0.100000\"/>\n      <ns0:circle cx=\"0.006000\" cy=\"0.001000\" fill=\"rgb(0,0,0)\" r=\"0.057000\" stroke=\"rgb(255,255,255)\" stroke-width=\"0.100000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"-0.003000\" y=\"0.003000\"/>\n    </ns0:symbol>",
    "terminal": "<ns0:symbol id=\"terminal\">\n      <ns0:circle cx=\"0.000000\" cy=\"0.000000\" fill=\"none\" r=\"0.200000\" stroke=\"rgb(0,200,255)\" stroke-width=\"0.100000\"/>\n    </ns0:symbol>",
    "CompositeSwitch_2f3f226f-190e-4251-84cf-68b293dd2158": "<ns0:symbol height=\"3.8572879806160927\" id=\"CompositeSwitch_2f3f226f-190e-4251-84cf-68b293dd2158\" viewBox=\"0 0 4.600000001490116 3.8572879806160927\" width=\"4.600000001490116\">\n      \n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-0.279000\" x2=\"0.221000\" y1=\"-3.257000\" y2=\"-3.257000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-0.526000\" x2=\"0.474000\" y1=\"-3.018000\" y2=\"-3.018000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-0.776000\" x2=\"0.724000\" y1=\"-2.752000\" y2=\"-2.752000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-0.026000\" x2=\"-0.026000\" y1=\"-2.689000\" y2=\"-1.314000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-0.313000\" x2=\"0.249000\" y1=\"-1.252000\" y2=\"-1.252000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-2.526000\" x2=\"-1.026000\" y1=\"-0.019000\" y2=\"-0.019000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"-1.026000\" x2=\"0.724000\" y1=\"-0.019000\" y2=\"-0.581000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.504000\" x2=\"1.974000\" y1=\"-0.019000\" y2=\"-0.019000\"/>\n      <ns0:line fill=\"none\" stroke=\"rgb(255,0,0)\" stroke-width=\"0.100000\" x1=\"0.496000\" x2=\"0.496000\" y1=\"-0.438000\" y2=\"0.500000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"1\" type=\"0\" x=\"1.961000\" y=\"-0.031000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"2\" type=\"0\" x=\"0.000000\" y=\"-1.563000\"/>\n      <ns0:use ns1:href=\"#terminal\" terminal-index=\"3\" type=\"0\" x=\"-2.508000\" y=\"-0.031000\"/>\n    </ns0:symbol>",
}


# ═══════════════════════════════════════════════════════════
#  美化符号库（以数据集原图 defs 为基准整理，2026-09-09 定稿）
#  每类设备 → 唯一精确符号 id（不再按关键词子串匹配）
# ═══════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
#  美化符号库（以数据集全体 SVG 聚合统计为基准，2026-09-09 重新定稿）
#  每类设备 → 出现频率最高的 symbol id（从 165 张图聚合统计）
#  聚合来源：build_tmp/aggregate_symbol_library.py → output/svg/symbol_library_aggregated.json
# ═══════════════════════════════════════════════════════════════════════════════
SYMBOL_LIBRARY = {
    # --- 开关类 ---
    '0307': 'Breaker_TMP_62d95710-813b-4a92-8dce-35f89dc1c3cd',       # 断路器 QF（98次，全数据集最高频）
    '0201': 'LoadBreakSwitch_357151fb-61fc-46d3-9281-9ff6d1969176',   # 负荷开关 QL（250次，LoadBreakSwitch 前缀最高）
    '0202': 'Disconnector_TMP_54fefde2-8d21-4470-8807-663dab8577b8',  # 隔离开关 QS（42次，Disconnector 前缀最高）
    '0203': 'GroundDisconnector_TMP_0c37fbe3-1b09-41fd-8a4d-38e20bd945d5',  # 接地刀闸 QES（29次）
    '0302': 'Fuse_6f477905-e141-4423-8160-7b6e8537ec92',              # 熔断器 FU（196次）
    # --- 保护与测量类 ---
    '0309': 'SurgeArrester_f4d15417-154b-4802-9a0d-eaa46f6f049d',   # 避雷器 F（42次，SurgeArrester 前缀最高）
    '0116': 'SurgeArrester_f4d15417-154b-4802-9a0d-eaa46f6f049d',   # 避雷器 F（同0309）
    '0305': 'PotentialTransformer_TMP_6946543d-651e-4f1d-97bb-353beeaeaede',  # 电压互感器 PT（36次）
    '0306': 'CurrentTransformer_9119054a-1e83-4003-a946-a83406c03d83',    # 电流互感器 CT（20次）
    # --- 变压器 ---
    '0110': 'PowerTransformer_TMP_a70da64e-4139-4238-99ff-f38ae7eea01c',  # 主变压器 T（84次，PowerTransformer 前缀最高）
    '0111': 'PowerTransformer_TMP_a70da64e-4139-4238-99ff-f38ae7eea01c',  # 配电变压器 T（同0110，共用）
    # --- 其他 ---
    '0115': 'PoleCode_da3c5ac4-fbe8-4e62-bfb3-5eab3768a97a',          # 杆塔
    '0313': 'CurrentTransformer_9119054a-1e83-4003-a946-a83406c03d83',  # 实际是电流互感器 CT
    '0314': 'PotentialTransformer_a6f46c6a-ace4-43ea-9973-b5f94576d3c9',  # 实际是电压互感器 PT
    '32TMP00132954': 'Junction_03ae4dd6-c087-42d2-82de-7a7c43b048e8',    # 真正的接线点
    '370000': 'EnergyConsumer_3dba839c-4394-4b87-9ef4-dae464753604',  # 电力用户（173次）
    '0113': 'Other_e34f9d8c-702c-415a-989e-414563b32fb5',             # 其他（147次）
}


# ═══════════════════════════════════════════════════════════
#  规范常量（与参考文件 v2 对齐，自包含不依赖 core.constants）
# ═══════════════════════════════════════════════════════════
WIRE_MARKERS = ('TMP', 'dxd')
BUSBAR_TYPES = {'0311'}
CONTAINER_TYPES = {'zf01', 'zf06', 'zf07', 'zf08', 'zf10'}
JUNCTION_TYPES = {'32TMP00132954'}  # 真正的接线点：画小色框
SWITCH_TYPES = {'0307', '0201', '0202', '0203', '0302', '0305', '0306', '0309'}
TRANSFORMER_TYPES = {'0110', '0111'}
KEY_DEV_TYPES = SWITCH_TYPES | TRANSFORMER_TYPES | BUSBAR_TYPES
GARBAGE_PATTERNS = [
    r'[炽始速常个行旁劳著长]',
    r'[歌咱母民急书箱]',
    r'[行县万别央压四说]',
    r'[行县行放导较拉除]',
    r'[毛须然约命了严]',
    r'[明争败诉取教]',
    r'[个行行者劳]',
    r'[假社员教]',
    r'[炽始速常]',
    r'行县', r'个行', r'行者劳',
    r'明\d*#', r'争\d', r'败诉', r'况诉',
]

C_BG = '#FFFFFF'
C_10KV = '#00A854'
C_TIE = '#FF6A00'
C_CROSS_TIE = '#722ED1'
C_SPARE = '#BFBFBF'
C_CONTAINER = '#595959'
C_TEXT = '#262626'
C_BUSBAR = '#00A854'

# ═══════════════════════════════════════════════════════════
#  设备类别色块（浅色实色，画在容器灰底之上不叠加；同类相近、跨类区分）
#  色系派生自 SVG 制图规范 v1 附表 B.2：橙=开关族 / 蓝=变压器族 /
#  黄绿=互感器 / 灰绿=负荷末端 / 浅灰=节点与备用
# ═══════════════════════════════════════════════════════════
DEV_CATEGORY_FILL = {
    # 开关族（橙系）
    '0307': '#FFB985',   '0201': '#FFC9A0', '0202': '#FFDFA8',
    '0203': '#FFEBA8',   '0302': '#FFD5A8', '0309': '#FFD0A8',
    '0113': '#FFD0A8',   '0115': '#FFC9A0',
    # 变压器族（蓝系）
    '0110': '#A8C8FF',   '0111': '#A8E0F5',
    # 互感器（黄绿）
    '0305': '#D0E8B8',   '0306': '#D0E8B8',
    # 母线（绿）
    '0311': '#A8E8C8',
    # 负荷/用户（灰绿）
    '370000': '#C8E8C8',
    # 附属设备（避雷器/故障指示器，紫）
    '0116': '#D8C8F0',   '0811003': '#D8C8F0',
    # 电流互感器 CT/电压互感器 PT（0313/0314 实际是这两个设备）
    '0313': '#FFE0C8',   '0314': '#FFE0C8',
    # 真正的接线点（拓扑节点，浅灰）
    '32TMP00132954': '#E0E0E0',
}
DEV_CATEGORY_FALLBACK = '#E8E8E8'
# 容器透明灰底：fill 用 #808080 + fill-opacity（兼容 SVG 解析），很低透明度保证穿过箱柜的线路可见
CONTAINER_BG_FILL = '#808080'
CONTAINER_BG_OPACITY = '0.06'
# 名称优先分类（数据源 type 与名称脱节严重，名称更可靠；长关键词在前）
DEV_CATEGORY_BY_NAME = [
    (('负荷开关', '隔离开关', '断路器', '分段器', '重合器'), '#FFB985'),
    (('开关', '刀闸', '熔断'), '#FFC9A0'),
    (('主变', '箱变', '配变', '变压器'), '#A8C8FF'),
    (('母线',), '#A8E8C8'),
    (('用户', '负荷'), '#C8E8C8'),
    (('避雷器', '故障指示器', '互感器', '电容器'), '#D8C8F0'),
    (('终端头', '缆头', '电缆', '站外'), '#E0E0E0'),
]
W_TRUNK = 3.0  # 主线：粗实线
W_BRANCH = 1.5  # 分支线路/柜内短线
W_TIE = 4.5  # 联络线：加粗高亮
W_CONTAINER = 2.0
W_BUSBAR = 3.0  # 母线：粗实线
F_TITLE = 21.3
F_KEY = 14.0
F_BRANCH = 12.0
GRID = 10
MARGIN = 40
TITLE_H = 52
CONT_PAD = 24
UNIT_V = 14
SYM_SCALE = 3.5
DEV_HW = 15
DEV_HH = 10

DEVICE_STANDARD_SIZES = {
    "PowerTransformer": (28.0, 20.0),
    "Breaker": (24.0, 12.0),
    "BusbarSection": (32.0, 6.0),
    "LoadBreakSwitch": (20.0, 10.0),
    "Disconnector": (20.0, 10.0),
    "Fuse": (16.0, 8.0),
    "CurrentTransformer": (16.0, 12.0),
    "PotentialTransformer": (16.0, 12.0),
    "Junction": (8.0, 8.0),
    "EnergyConsumer": (20.0, 12.0),
    "RemoteUnit": (16.0, 10.0),
    "PoleCode": (16.0, 10.0),
    "Other": (16.0, 10.0),
    "GroundDisconnector": (20.0, 10.0),
    "CompositeSwitch": (20.0, 10.0),
}


def is_real(d):
    return bool(d and d.get("type") and d["type"] not in ("dxd", "0", "unknown", ""))


class SvgBeautifier:
    """配电网单线图 SVG 美化重构工具 v2（完整功能版）"""

    def __init__(self, svg_path: str, output_path: str = None):
        self.svg_path = svg_path
        self.svg_filename = os.path.basename(svg_path)
        self.output_path = output_path or svg_path.replace(".svg", "_beautified.svg")

        self.doc: Optional[SvgDocument] = None
        self.devices: Dict[str, Dict] = {}
        self.gl_to_devs: Dict[str, Set[str]] = defaultdict(set)
        self.containers: Dict[str, Dict] = {}
        self.adj: Dict[str, Set[str]] = defaultdict(set)
        self.pos: Dict[str, Tuple[float, float]] = {}
        self.cont_box: Dict[str, Tuple[float, float, float, float]] = {}
        self.tree_parent: Dict[str, Optional[str]] = {}
        self.tree_children: Dict[str, List[str]] = defaultdict(list)
        self.non_tree_edges: List = []
        self.label_rects: List = []
        self.sym_box: Dict[str, Dict] = {}
        self.orig_pos: Dict[str, Tuple[float, float]] = {}
        self.repair_stats: Dict = {}

    # ═══════════════════════════════════════════════════════════
    #  辅助工具函数
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def is_wire(t: str) -> bool:
        if not t:
            return False
        # 【修复WIRE】32TMP* 为箱变/接线节点设备（含TMP但不是线路），明确排除误判
        if t.startswith('32TMP'):
            return False
        # 其余类型：精确匹配线路标记（dxd=线路段），避免子串误伤
        return t in WIRE_MARKERS

    @staticmethod
    def is_real_device(t: str) -> bool:
        if not t or SvgBeautifier.is_wire(t):
            return False
        if t in CONTAINER_TYPES:
            return False
        if t in ('-1', '0'):
            return False
        if 'BackGround' in t:
            return False
        return True

    @staticmethod
    def is_garbage_text(text: str) -> bool:
        if not text or len(text) < 2:
            return True
        if text.startswith('TMP') or re.match(r'^\d+$', text):
            return True
        for pat in GARBAGE_PATTERNS:
            if re.search(pat, text):
                return True
        if text.startswith('000') and re.search(r'[\u4e00-\u9fff]{2,}', text):
            valid_kw = ['终端头', '电缆', '母线', '线路', '开关站', '环网柜', '配变',
                        '断路器', '隔离开关', '负荷开关', '熔断器', '杆塔', '变压器',
                        '站房', '配电室', 'LINE', 'SUB']
            if not any(kw in text for kw in valid_kw):
                return True
            for pat in GARBAGE_PATTERNS:
                if re.search(pat, text):
                    return True
        if re.search(r'[a-zA-Z]+_[\u4e00-\u9fff]', text) and 'LINE' not in text.upper():
            return True
        return False

    @staticmethod
    def snap(v: float) -> float:
        return round(v / GRID) * GRID

    # ═══════════════════════════════════════════════════════════
    #  核心处理流程
    # ═══════════════════════════════════════════════════════════

    def beautify(self) -> str:
        print(f"\n[Beautifier v2] 正在处理: {self.svg_filename}")
        self._prepare_internal_data()
        self.repair()
        self.layout()
        self.render(self.output_path)
        return self.output_path

    def _prepare_internal_data(self):
        """将 SvgDocument 的 IR 转换为 v2 内部数据结构"""
        if not self.doc:
            self.doc = SvgDocument(self.svg_path)
            self.doc.parse()

        self._ensure_library_symbols()
        self._collect_symbol_boxes()

        # 从 SVG metadata 直接读取 ssjg（SvgDocument 的 container_id 可能为空）
        ssjg_map = {}
        if self.doc and self.doc.root is not None:
            for g in self.doc.root.iter(f'{{{SVG_NS}}}g'):
                md = g.find(f'{{{SVG_NS}}}metadata')
                if md is None:
                    continue
                psr = md.find(f'{{{IEC_NS}}}PSR_Ref')
                if psr is not None:
                    oid = psr.get('ObjectID', '')
                    sj = psr.get('ssjg', '') or ''
                    if oid and sj:
                        ssjg_map[oid] = sj

        for elem in self.doc.elements:
            pid = elem.element_id
            ptype = elem.psr_type or elem.layer_name
            pname = elem.element_name or ""
            ssjg = elem.container_id or ssjg_map.get(pid, '') or ""
            gls = elem.glink_refs
            sym = elem.symbol_href
            vcls = elem.css_class or "lkv10"
            orig_x, orig_y = elem.x, elem.y
            self.orig_pos[pid] = (orig_x, orig_y)
            self.devices[pid] = {
                'id': pid, 'type': ptype, 'name': pname,
                'ssjg': ssjg, 'glinks': gls, 'symbol': sym, 'vclass': vcls,
                'orig_x': orig_x, 'orig_y': orig_y,
                'layer': elem.layer_name
            }
            for gl in gls:
                self.gl_to_devs[gl].add(pid)

        self._build_adj()
        self._find_containers()
        self._assign_fallback_symbols()

        nd = sum(1 for d in self.devices.values() if self.is_real_device(d['type']))
        print(f"  [解析] 设备 {len(self.devices)} | 真实设备 {nd} | "
              f"GLink {len(self.gl_to_devs)} | 容器 {len(self.containers)} | "
              f"邻接边 {sum(len(v) for v in self.adj.values()) // 2}")


    def _ensure_library_symbols(self):
        """确保美化符号库的符号定义全部存在于本图 defs（跨图缺失则从内置库或数据集注入）
        注入时同步处理：ns0 前缀→SVG 命名空间、xlink 引用、杆塔白描边改深色"""
        if self.doc is None or self.doc.root is None:
            return
        defs = self.doc.root.find(f'{{{SVG_NS}}}defs')
        if defs is None:
            defs = ET.Element(f'{{{SVG_NS}}}defs')
            self.doc.root.insert(0, defs)
        existing = {s.get('id', '') for s in defs.findall(f'{{{SVG_NS}}}symbol')}

        # 第一步：尝试从内置 SYMBOL_DEFS_XML 注入
        for sid, xml_str in SYMBOL_DEFS_XML.items():
            if sid in existing:
                continue
            try:
                if sid.startswith('PoleCode_'):
                    xml_str = xml_str.replace('rgb(255,255,255)', 'rgb(90,90,90)')
                m = re.search(r'<ns0:symbol\b([^>]*)>(.*)</ns0:symbol>', xml_str, re.S)
                if not m:
                    continue
                attrs, body = m.group(1), m.group(2)
                body = re.sub(r'<ns0:', '<', body)
                body = re.sub(r'</ns0:', '</', body)
                body = re.sub(r'ns1:href', 'xlink:href', body)
                fixed = (f'<symbol xmlns="{SVG_NS}" '
                         f'xmlns:xlink="http://www.w3.org/1999/xlink"{attrs}>{body}</symbol>')
                elem = ET.fromstring(fixed)
                defs.append(elem)
                existing.add(sid)
            except Exception as e:
                print(f'  [符号库] 注入符号 {sid[:32]} 失败: {e}')

        # 第二步：SYMBOL_LIBRARY 中仍缺失的符号，从数据集 SVG 动态提取注入
        needed_sids = set(SYMBOL_LIBRARY.values())
        missing_sids = needed_sids - existing
        if missing_sids:
            self._inject_symbols_from_dataset(missing_sids, existing, defs)

    def _inject_symbols_from_dataset(self, missing_sids, existing, defs):
        """从数据集 SVG 文件动态加载缺失的符号定义并注入"""
        import glob
        dataset_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '数据集更新版20260729', '配网 svg'
        )
        if not os.path.isdir(dataset_dir):
            return

        svg_files = glob.glob(os.path.join(dataset_dir, '*.svg'))
        for svg_path in svg_files:
            if not missing_sids:
                break
            try:
                tree = ET.parse(svg_path)
                root = tree.getroot()
                src_defs = root.find(f'{{{SVG_NS}}}defs')
                if src_defs is None:
                    continue
                for sym in src_defs.findall(f'{{{SVG_NS}}}symbol'):
                    sid = sym.get('id', '')
                    if sid in missing_sids:
                        # 复制 symbol 节点并注入
                        new_sym = copy.deepcopy(sym)
                        defs.append(new_sym)
                        existing.add(sid)
                        missing_sids.discard(sid)
                        # 同步处理：杆塔白描边改深色
                        if sid.startswith('PoleCode_'):
                            for el in new_sym.iter():
                                if el.get('stroke') == 'rgb(255,255,255)':
                                    el.set('stroke', 'rgb(90,90,90)')
            except Exception:
                continue

        if missing_sids:
            print(f'  [符号库] 警告：{len(missing_sids)} 个符号无法从数据集加载：{list(missing_sids)[:3]}...')

    def _collect_symbol_boxes(self):
        if self.doc.root is None:
            return
        defs = self.doc.root.find(f'{{{SVG_NS}}}defs')
        if defs is None:
            return
        TARGET_W = 28.0
        MAX_ORIG = 50.0
        for s in defs.findall(f'{{{SVG_NS}}}symbol'):
            sid = s.get('id', '')
            vb = s.get('viewBox', '0 0 8 6')
            vb_parts = vb.split()
            vb_w = float(vb_parts[2]) if len(vb_parts) == 4 else 8.0
            vb_h = float(vb_parts[3]) if len(vb_parts) == 4 else 6.0
            xs, ys = [], []
            for child in s.iter():
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                for attr in ('x', 'x1', 'x2', 'cx'):
                    v = child.get(attr)
                    if v:
                        try:
                            fv = float(v)
                            if abs(fv) <= MAX_ORIG:
                                xs.append(fv)
                        except ValueError:
                            pass
                for attr in ('y', 'y1', 'y2', 'cy'):
                    v = child.get(attr)
                    if v:
                        try:
                            fv = float(v)
                            if abs(fv) <= MAX_ORIG:
                                ys.append(fv)
                        except ValueError:
                            pass
                if tag == 'circle':
                    try:
                        cx = float(child.get('cx', 0))
                        cy = float(child.get('cy', 0))
                        r = float(child.get('r', 0))
                        if abs(cx) <= MAX_ORIG and r > 0:
                            xs += [cx - r, cx + r]
                            ys += [cy - r, cy + r]
                    except ValueError:
                        pass
                elif tag == 'ellipse':
                    try:
                        cx = float(child.get('cx', 0))
                        cy = float(child.get('cy', 0))
                        rx = float(child.get('rx', 0))
                        ry = float(child.get('ry', 0))
                        if abs(cx) <= MAX_ORIG and rx > 0:
                            xs += [cx - rx, cx + rx]
                            ys += [cy - ry, cy + ry]
                    except ValueError:
                        pass
                elif tag == 'rect':
                    try:
                        rx = float(child.get('x', 0))
                        ry = float(child.get('y', 0))
                        rw = float(child.get('width', 0))
                        rh = float(child.get('height', 0))
                        if abs(rx) <= MAX_ORIG and rw > 0:
                            xs += [rx, rx + rw]
                            ys += [ry, ry + rh]
                    except ValueError:
                        pass
                pts = child.get('points')
                if pts:
                    for pair in pts.split():
                        try:
                            px, py = pair.split(',')
                            fx, fy = float(px), float(py)
                            if abs(fx) <= MAX_ORIG:
                                xs.append(fx)
                            if abs(fy) <= MAX_ORIG:
                                ys.append(fy)
                        except ValueError:
                            pass
            if xs and ys:
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                w = max_x - min_x
                h = max_y - min_y
                if w < 0.5 or w > MAX_ORIG or h < 0.5 or h > MAX_ORIG:
                    w, h = vb_w, vb_h
                    min_x, max_x = 0, vb_w
                    min_y, max_y = 0, vb_h
            else:
                w, h = vb_w, vb_h
                min_x, max_x = 0, vb_w
                min_y, max_y = 0, vb_h
            cx = (min_x + max_x) / 2
            cy = (min_y + max_y) / 2
            scale = TARGET_W / w if w > 0.1 else SYM_SCALE
            scale = min(scale, 5.0)
            self.sym_box[sid] = {
                'cx': cx, 'cy': cy, 'w': w, 'h': h, 'scale': scale,
                'left': (min_x - cx) * scale, 'right': (max_x - cx) * scale,
                'top': (min_y - cy) * scale, 'bottom': (max_y - cy) * scale,
            }

            # ★ 新增：提取每个 terminal-index 的真实坐标（缩放后），用于精确接线
            # 存储格式：{terminal_index: (scaled_x, scaled_y)}
            term_map = {}
            for child in s.iter():
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if tag == 'use':
                    ti = child.get('terminal-index')
                    tx = child.get('x')
                    ty = child.get('y')
                    if ti and tx and ty:
                        try:
                            ox, oy = float(tx), float(ty)
                            sx = (ox - cx) * scale
                            sy = (oy - cy) * scale
                            term_map[int(ti)] = (sx, sy)
                        except (ValueError, TypeError):
                            pass
            if term_map:
                self.sym_box[sid]['terminals'] = term_map

    def _assign_fallback_symbols(self):
        # 符号归一化：按美化符号库精确映射（类型码 -> 唯一符号 id），
        # 同类型设备统一使用同一符号，不再按关键词子串匹配 defs 首个命中
        for pid, d in self.devices.items():
            sid = SYMBOL_LIBRARY.get(d['type'])
            if sid:
                d['symbol'] = '#' + sid

    def _build_adj(self):
        real_set = {pid for pid, d in self.devices.items() if self.is_real_device(d['type'])}
        gl_graph = defaultdict(set)
        for elem in self.doc.elements:
            if self.is_wire(elem.psr_type or elem.layer_name) and len(elem.glink_refs) >= 2:
                gls = elem.glink_refs
                for i in range(len(gls) - 1):
                    gl_graph[gls[i]].add(gls[i + 1])
                    gl_graph[gls[i + 1]].add(gls[i])
        for conn in self.doc.connections:
            if conn.start_device_id and conn.end_device_id:
                self.adj[conn.start_device_id].add(conn.end_device_id)
                self.adj[conn.end_device_id].add(conn.start_device_id)
        for pid in sorted(real_set):
            for start_gl in self.devices[pid]['glinks']:
                for other in self.gl_to_devs.get(start_gl, ()):
                    if other != pid and other in real_set:
                        self.adj[pid].add(other)
                        self.adj[other].add(pid)
                visited = {start_gl}
                q = deque([start_gl])
                while q:
                    cur = q.popleft()
                    for nxt in gl_graph.get(cur, ()):
                        if nxt in visited:
                            continue
                        visited.add(nxt)
                        hit = False
                        for other in self.gl_to_devs.get(nxt, ()):
                            if other != pid and other in real_set:
                                self.adj[pid].add(other)
                                self.adj[other].add(pid)
                                hit = True
                        if not hit:
                            q.append(nxt)

    def _find_containers(self):
        for pid, d in self.devices.items():
            if d['type'] in CONTAINER_TYPES:
                cid = d['ssjg'] or pid
                if cid not in self.containers:
                    self.containers[cid] = {'id': cid, 'name': d['name'],
                                            'type': d['type'], 'psr_id': pid, 'members': []}
        for pid, d in self.devices.items():
            s = d.get('ssjg', '')
            if not s or not self.is_real_device(d['type']):
                continue
            if d['type'] in BUSBAR_TYPES:
                # 母线是馈线级主干元素，不作为容器成员（避免"母线上柜"）
                continue
            if s not in self.containers:
                self.containers[s] = {'id': s, 'name': '', 'type': 'zf08',
                                      'psr_id': None, 'members': []}
            if pid not in self.containers[s]['members']:
                self.containers[s]['members'].append(pid)
        for cid, c in self.containers.items():
            if c['name'] and not self.is_garbage_text(c['name']):
                continue
            best = ''
            for m in c['members']:
                nm = self.devices[m].get('name', '')
                if self.is_garbage_text(nm):
                    continue
                for sep in ['#', '~', '－', '_']:
                    if sep in nm:
                        cand = nm.split(sep)[0].strip('0').strip()
                        if len(cand) > 2 and len(cand) > len(best):
                            best = cand
                if any(k in nm for k in ['开关站', '环网柜', '配电室', '站房']):
                    best = nm
                    break
            c['name'] = best if best else f'柜_{cid[:6]}'
        self.containers = {k: v for k, v in self.containers.items()
                           if v['members'] or v.get('psr_id')}
        # 容器名去重
        name_count = defaultdict(int)
        for cid, c in self.containers.items():
            nm = c['name']
            name_count[nm] += 1
            if name_count[nm] > 1:
                c['name'] = f"{nm}#{name_count[nm]}"

    # ═══════════════════════════════════════════════════════════
    #  拓扑修复（完整：飞线修复 + 孤岛缝合 + 清理）
    # ═══════════════════════════════════════════════════════════

    def repair(self):
        real_set = {pid for pid, d in self.devices.items() if self.is_real_device(d['type'])}
        if not real_set:
            self.repair_stats = {"repaired": 0, "components_before": 0, "components_after": 0}
            return

        def find_components():
            visited = set()
            comps = []
            for start in sorted(real_set):
                if start in visited:
                    continue
                comp = set()
                q = deque([start])
                visited.add(start)
                while q:
                    u = q.popleft()
                    comp.add(u)
                    for v in self.adj.get(u, ()):
                        if v not in visited and v in real_set:
                            visited.add(v)
                            q.append(v)
                comps.append(comp)
            return comps

        comps_before = find_components()
        comps_before.sort(key=len, reverse=True)
        main_comp = set(comps_before[0]) if comps_before else set()

        repaired = 0
        DANGLE_THRESHOLD = 150.0
        STITCH_THRESHOLD = 250.0

        for comp in comps_before[1:]:
            if len(comp) != 1:
                continue
            node = next(iter(comp))
            if node not in self.orig_pos:
                continue
            nx, ny = self.orig_pos[node]
            best, best_d = None, float('inf')
            for other in sorted(main_comp):
                if other not in self.orig_pos:
                    continue
                ox, oy = self.orig_pos[other]
                d = math.hypot(nx - ox, ny - oy)
                if d < best_d:
                    best_d, best = d, other
            if best and best_d < DANGLE_THRESHOLD:
                self.adj[node].add(best)
                self.adj[best].add(node)
                main_comp.add(node)
                repaired += 1

        comps_mid = find_components()
        comps_mid.sort(key=len, reverse=True)
        for comp in comps_mid[1:]:
            if len(comp) < 2 or len(comp) > 8:
                continue
            best_pair, best_d = (None, None), float('inf')
            for a in sorted(comp):
                if a not in self.orig_pos:
                    continue
                ax, ay = self.orig_pos[a]
                for b in sorted(main_comp):
                    if b not in self.orig_pos:
                        continue
                    bx, by = self.orig_pos[b]
                    d = math.hypot(ax - bx, ay - by)
                    if d < best_d:
                        best_d, best_pair = d, (a, b)
            if best_pair[0] and best_d < STITCH_THRESHOLD:
                a, b = best_pair
                self.adj[a].add(b)
                self.adj[b].add(a)
                main_comp |= comp
                repaired += 1

        for u in list(self.adj.keys()):
            self.adj[u].discard(u)
            for v in list(self.adj[u]):
                self.adj[v].add(u)
        empty = [k for k, v in self.adj.items() if not v]
        for k in empty:
            del self.adj[k]

        comps_after = find_components()
        isolated = sum(1 for c in comps_after if len(c) == 1)
        self.repair_stats = {
            "repaired": repaired,
            "components_before": len(comps_before),
            "components_after": len(comps_after),
            "isolated_after": isolated,
        }
        print(f"  [修复] 补连 {repaired} 处 | 连通分量 {len(comps_before)}->{len(comps_after)} | 剩余孤立 {isolated}")

    # ═══════════════════════════════════════════════════════════
    #  Sugiyama 层次布局 + 总线感知（v3 新增）
    #  经典 5 步：Cycle removal → Layer assignment → Crossing reduction
    #          → Coordinate assignment → Bus-aware routing
    # ═══════════════════════════════════════════════════════════

    def _sugiyama_cycle_removal(self):
        """三色 DFS 区分树边/非树边（环检测）。
        返回 (tree_edges, back_edges)，不修改 self.adj。"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = defaultdict(lambda: WHITE)
        parent = {}
        tree_edges = set()
        back_edges = set()

        def dfs(u):
            color[u] = GRAY
            for v in sorted(self.adj.get(u, ())):
                if v not in self.devices:
                    continue
                if color[v] == WHITE:
                    parent[v] = u
                    tree_edges.add(tuple(sorted([u, v])))
                    dfs(v)
                elif color[v] == GRAY and parent.get(u) != v:
                    # 找到回边 → 标记为非树边
                    back_edges.add(tuple(sorted([u, v])))
            color[u] = BLACK

        # 从所有度数最高的母线开始
        buses = [p for p, d in self.devices.items() if d['type'] in BUSBAR_TYPES]
        roots = [b for b in buses if b in self.adj]
        if not roots:
            # 兜底：度数最高的节点
            deg = {p: len(self.adj.get(p, ())) for p in self.adj}
            if deg:
                m = max(deg.values())
                roots = [p for p in self.adj if deg[p] == m]

        for r in roots:
            if color[r] == WHITE:
                dfs(r)
        # 处理孤立节点
        for n in list(self.adj.keys()):
            if color[n] == WHITE:
                dfs(n)

        self.tree_edges = tree_edges
        self.back_edges = back_edges
        return tree_edges, back_edges

    def _sugiyama_layer_assign(self):
        """从根节点 BFS，分配每个节点到 layer。
        母线不排除：参与 BFS 分层，最后坐标分配时再单独排成骨架。"""
        buses = {pid for pid, d in self.devices.items() if d['type'] in BUSBAR_TYPES}
        self.busbar_pids = buses

        # 找 BFS 根
        roots = [b for b in buses if b in self.adj]
        if not roots:
            deg = {p: len(self.adj.get(p, ())) for p in self.adj}
            if deg:
                m = max(deg.values())
                roots = [p for p in deg if deg[p] == m]

        node_layer = {}
        if roots:
            visited = set(roots)
            queue = deque([(r, 0) for r in roots])
            while queue:
                u, layer = queue.popleft()
                node_layer[u] = node_layer.get(u, layer)
                for v in self.adj.get(u, ()):
                    if v not in visited and v in self.devices:
                        visited.add(v)
                        queue.append((v, layer + 1))

        # 未入层节点兜底
        for n in self.adj:
            if n not in node_layer:
                node_layer[n] = 0

        self.node_layer = node_layer
        self.layers = defaultdict(list)
        for n, l in node_layer.items():
            self.layers[l].append(n)
        # 母线作为骨架层（最后一层，但坐标单独处理）
        max_layer = max(self.layers.keys()) if self.layers else 0
        # 母线已经在它自己的层（由 BFS 决定），但需要标记它们属于骨架
        # 不再额外加一层
        self.busbar_layer = None  # 标记无独立母线层
        print(f"  [Sugiyama] 分层: {len(self.layers)} 层, 母线节点数 {len(buses)}")
        return self.layers

    def _sugiyama_cross_reduction(self, max_iter=24):
        """Barycenter 重心法减少交叉：双向扫描，贪心重排。"""
        if not self.layers:
            return
        sorted_layer_ids = sorted(self.layers.keys())

        def barycenter(node, neighbor_order):
            nbs = [v for v in self.adj.get(node, ()) if v in neighbor_order]
            if not nbs:
                return float(len(neighbor_order)) / 2  # 孤立 → 居中
            return sum(neighbor_order[v] for v in nbs) / len(nbs)

        improved_count = 0
        for it in range(max_iter):
            improved = False
            # 向下扫描
            if it % 2 == 0:
                for li in range(len(sorted_layer_ids) - 1):
                    upper, lower = sorted_layer_ids[li], sorted_layer_ids[li + 1]
                    upper_order = {n: i for i, n in enumerate(self.layers[upper])}
                    new_lower = sorted(self.layers[lower],
                                        key=lambda n: barycenter(n, upper_order))
                    if new_lower != self.layers[lower]:
                        self.layers[lower] = new_lower
                        improved = True
            # 向上扫描
            else:
                for li in range(len(sorted_layer_ids) - 1, 0, -1):
                    upper, lower = sorted_layer_ids[li - 1], sorted_layer_ids[li]
                    lower_order = {n: i for i, n in enumerate(self.layers[lower])}
                    new_upper = sorted(self.layers[upper],
                                        key=lambda n: barycenter(n, lower_order))
                    if new_upper != self.layers[upper]:
                        self.layers[upper] = new_upper
                        improved = True
            if improved:
                improved_count += 1
            else:
                break
        print(f"  [Sugiyama] 交叉减少迭代: {improved_count}/{max_iter}")

    def _sugiyama_assign_coords(self):
        """基于 Sugiyama 分层结果分配 X/Y 坐标。
        母线不参与层内排序，而是单独排列在最底部的主干骨架上。

        ★ v4：调整设备密度 → X:Y 比例接近 1:1（对齐数据集风格）
          - DEV_SPAN: 80（设备横向间距）
          - LAYER_H: 220（每层高度）
        """
        DEV_SPAN = 80
        LAYER_H = 220

        sorted_layer_ids = sorted(self.layers.keys())
        self.pos = {}

        # 非母线节点：按层 + 重心排序结果分配
        for li, layer_id in enumerate(sorted_layer_ids):
            y = MARGIN + li * LAYER_H
            for xi, n in enumerate(self.layers[layer_id]):
                if n in self.busbar_pids:
                    continue  # 母线单独处理
                self.pos[n] = (MARGIN + xi * DEV_SPAN, y)

        # 母线层：★ 总线感知 - 沿主干路径纵向排列（X 方向紧凑）
        self._align_buses_vertically(DEV_SPAN, LAYER_H, len(sorted_layer_ids) + 1)

    def _align_buses_vertically(self, dev_span, layer_h, total_layers):
        """母线作为骨架：沿主干路径紧凑排列（X 方向）。
        传统算法把所有母线排在同一 Y → 横铺 → 长连线横穿。
        新算法：母线按主干树边拓扑顺序，紧凑排列在主干路径上。"""
        buses = sorted(self.busbar_pids)
        if not buses:
            return

        bus_y = MARGIN + total_layers * layer_h  # 母线层在最下方

        # 计算每个母线的"主干子树权重"
        sub_weight = {}
        def calc_w(n):
            if n in sub_weight:
                return sub_weight[n]
            kids = [c for c in self.tree_children.get(n, []) if c in buses]
            if not kids:
                # 包含挂载的所有下游非母线节点数
                all_desc = self._count_subtree(n)
                sub_weight[n] = all_desc
                return all_desc
            w = sum(calc_w(c) for c in kids) + self._count_subtree(n)
            sub_weight[n] = w
            return w

        def calc_w_simple(n):
            """简化权重：下游所有非母线设备数。"""
            if n in sub_weight:
                return sub_weight[n]
            cnt = self._count_subtree(n)
            sub_weight[n] = cnt
            return cnt

        # 找出根母线（连接最多的）
        deg = {b: sum(1 for v in self.adj.get(b, ())) for b in buses}
        root_bus = max(deg, key=deg.get) if deg else buses[0]

        # BFS 沿主干路径
        bus_x = {}
        visited = {root_bus}
        queue = deque([(root_bus, MARGIN)])
        while queue:
            cur, x = queue.popleft()
            bus_x[cur] = x
            # 下一层母线（cur 的母线邻居）
            next_buses = [v for v in self.adj.get(cur, ()) if v in buses and v not in visited]
            for nb in next_buses:
                visited.add(nb)
                queue.append((nb, x + dev_span))

        # 兜底：未访问的母线排在末尾
        cur_x = max(bus_x.values(), default=MARGIN) + dev_span
        for b in buses:
            if b not in bus_x:
                bus_x[b] = cur_x
                cur_x += dev_span

        for b in buses:
            self.pos[b] = (bus_x[b], bus_y)

        print(f"  [总线感知] 母线 {len(buses)} 沿主干紧凑排列, X 范围 "
              f"{min(bus_x.values()):.0f}~{max(bus_x.values()):.0f}")

    def _count_subtree(self, root):
        """计算 root 子树中的非母线节点数（含 root 自身）。"""
        buses = self.busbar_pids
        visited = set()
        stack = [root]
        cnt = 0
        while stack:
            n = stack.pop()
            if n in visited:
                continue
            visited.add(n)
            if n not in buses:
                cnt += 1
            for c in self.tree_children.get(n, []):
                if c not in visited:
                    stack.append(c)
        return cnt

    # ═══════════════════════════════════════════════════════════
    #  权重树梳状布局（含未入树设备兜底）
    # ═══════════════════════════════════════════════════════════

    def layout(self):
        use_sugiyama = os.environ.get('USE_SUGIYAMA', '0') == '1'
        root = self._find_root()
        if not root:
            print("  [布局] 无有效根节点")
            return

        self.tree_parent = {root: None}
        level = {root: 0}
        q = deque([root])
        while q:
            u = q.popleft()
            for v in sorted(self.adj.get(u, ())):
                if v not in self.tree_parent:
                    self.tree_parent[v] = u
                    level[v] = level[u] + 1
                    self.tree_children[u].append(v)
                    q.append(v)

        self.non_tree_edges = []
        tree_edge_set = set()
        for child, par in self.tree_parent.items():
            if par is not None:
                tree_edge_set.add(tuple(sorted([child, par])))
        for u, neigh in self.adj.items():
            for v in neigh:
                if u >= v:
                    continue
                key = tuple(sorted([u, v]))
                if key not in tree_edge_set:
                    self.non_tree_edges.append((u, v))

        cont_rep = {}
        for cid, c in self.containers.items():
            ms = [m for m in c['members'] if m in self.tree_parent]
            if not ms:
                # ★ v12f：空容器（无成员设备）也建 rep=自身，保证画出容器框，
                #   否则进出线端口悬空（成员不足 2 的容器在 _layout_containers 被跳过建框）
                if cid in self.tree_parent:
                    cont_rep[cid] = cid
                continue
            rep = min(ms, key=lambda m: level.get(m, 99999))
            cont_rep[cid] = rep
        self._cont_rep_map = cont_rep

        if use_sugiyama:
            # ★ Sugiyama 层次布局
            print(f"  [布局] 启用 Sugiyama 层次布局 + 总线感知")
            self._sugiyama_cycle_removal()
            self._sugiyama_layer_assign()
            self._sugiyama_cross_reduction()
            self._sugiyama_assign_coords()
        else:
            # ★ v5 电力语义布局（题目 5.1.1：电源起点/从左至右/先上后下/疏密均匀）
            DEV_SPAN = 140          # 主干/层内水平间距（符号48宽+空隙）
            TRUNK_Y0 = MARGIN + 30  # 主干行（电源→负荷，从左至右）
            LAYER_H = 240           # 分支层高（先上后下）
            GROUP_GAP = 60
            BRANCH_ROW_LIMIT = 22   # 单层设备数上限，超出拆多行（疏密均匀）

            weight = {}

            def calc_weight(node):
                kids = self.tree_children.get(node, [])
                if not kids:
                    weight[node] = 1
                    return 1
                w = sum(calc_weight(c) for c in kids)
                weight[node] = w
                return w
            calc_weight(root)

            # ★ 主干选择：优先沿母线走（母线骨架），否则最重子孙链
            def _pick_main(kids):
                bus = [c for c in kids if self.devices.get(c, {}).get('type') in BUSBAR_TYPES]
                pool = bus if bus else kids
                return max(pool, key=lambda c: weight[c])

            main_child = {}
            for node in self.tree_parent:
                kids = self.tree_children.get(node, [])
                if kids:
                    main_child[node] = _pick_main(kids)

            trunk_set = set()
            trunk_order = []
            node = root
            while node is not None:
                trunk_set.add(node)
                trunk_order.append(node)
                node = main_child.get(node)

            branch_depth = {}
            for n in self.tree_parent:
                d = 0
                cur = n
                while cur not in trunk_set and cur is not None:
                    d += 1
                    cur = self.tree_parent.get(cur)
                branch_depth[n] = d

            layers = defaultdict(list)
            for n in self.tree_parent:
                layers[branch_depth[n]].append(n)

            self.pos = {}
            for i, n in enumerate(trunk_order):
                self.pos[n] = (self.snap(MARGIN + i * DEV_SPAN), self.snap(TRUNK_Y0))

            # ★ 分支层内排序：兄弟按（母线>开关>其他, 原图y）→ 先上后下
            def _sib_order(cs):
                def key(c):
                    t = self.devices.get(c, {}).get('type', '')
                    rank = 0 if t in BUSBAR_TYPES else (1 if t in SWITCH_TYPES else 2)
                    return (rank, self.devices.get(c, {}).get('orig_y', 0))
                return sorted(cs, key=key)

            max_depth = max(branch_depth.values()) if branch_depth else 0
            # 梳状放置：孩子尽量垂直对齐父节点（x 贴近父），兄弟从父 x 横排；
            # 同层内 x 冲突检测 → 向右找空位（保持"从左至右、先上后下"）
            for depth in range(1, max_depth + 1):
                layer_nodes = layers[depth]
                if not layer_nodes:
                    continue
                groups = defaultdict(list)
                for n in layer_nodes:
                    groups[self.tree_parent[n]].append(n)
                sorted_parents = sorted(groups.keys(),
                                        key=lambda p: self.pos.get(p, (0, 0))[0])
                y = TRUNK_Y0 + depth * LAYER_H
                # 本层已占用的 x 区间（兄弟排开后占用）
                occupied = []
                for par in sorted_parents:
                    children = _sib_order(groups[par])
                    px = self.pos[par][0]
                    # 尝试从 px 起排；若与已占用区间重叠，整体右移到空位
                    base = px
                    for o_l, o_r in occupied:
                        need_l = base
                        need_r = base + (len(children) - 1) * DEV_SPAN
                        if need_r >= o_l and need_l <= o_r:
                            base = o_r + GROUP_GAP
                    for i, n in enumerate(children):
                        self.pos[n] = (self.snap(base + i * DEV_SPAN), self.snap(y))
                    if children:
                        occupied.append((base, base + (len(children) - 1) * DEV_SPAN))
                        occupied.sort()

        # ★ 未入树设备兜底（两种算法共享）
        placed = set(self.pos)
        leftover = [p for p, d in self.devices.items()
                    if self.is_real_device(d['type']) and p not in placed]
        if leftover:
            bx = max((p[0] for p in self.pos.values()), default=0) + (80 if not use_sugiyama else 80)
            by = (MARGIN + 30) + (max_depth + 1) * 220 if not use_sugiyama else MARGIN + (len(self.layers)) * 220
            for i, pid in enumerate(leftover):
                self.pos[pid] = (self.snap(bx + i * 80), self.snap(by))

        # ★ 布局后处理：先容器单元化（成员竖排/容器框/碰撞/顶部/非柜箱避让），
        #   再对自由设备做设备-设备避让（容器成员保持竖排不参与移动）
        self._layout_containers(cont_rep)
        self._fix_overlaps()
        self._normalize()

        # ★ 端口预分配：每个设备为每个邻居分配一个端点 (L/R/T/B)
        # 每边最多 1 条线，方向匹配优先，左右优先
        self._assign_ports()

        if use_sugiyama:
            print(f"  [布局 Sugiyama] 放置 {len(self.pos)} | 层数 {len(self.layers)} | "
                  f"母线纵向 {len(self.busbar_pids)}")
        else:
            print(f"  [布局] 放置 {len(self.pos)} | 容器框 {len(self.cont_box)} | "
                  f"树深 {max(level.values())} | 根权重 {weight[root]}")

    def _fix_overlaps(self, gap=26):
        """布局后处理：设备色框两两避让（右移，保持 y 不变），消除元件重叠。

        逐行扫描：与已放置框冲突的设备向右移动到不重叠位置。
        保持 y（层高语义不变），仅调整 x（从左至右）。
        """
        if not self.pos:
            return
        member_set = set()
        for cid, cd in self.containers.items():
            for m in cd.get('members', []):
                member_set.add(m)
        order = sorted(self.pos.items(), key=lambda kv: (kv[1][1], kv[1][0]))
        placed = []  # (cx, cy, half_w, half_h)
        # 容器框自身也占位（自由设备不得压进容器框区域）
        cont_boxes_abs = []
        for cid, (x1, y1, x2, y2) in self.cont_box.items():
            cont_boxes_abs.append(((x1 + x2) / 2.0, (y1 + y2) / 2.0,
                                   (x2 - x1) / 2.0, (y2 - y1) / 2.0))
        for pid, (x, y) in order:
            try:
                l, r, t, b = self._dev_box_edges(pid)
            except Exception:
                continue
            w = (r - l) / 2.0
            h = (b - t) / 2.0
            if pid in member_set or pid in self.containers:
                # 容器成员/容器自身保持布局位置，不参与移动（容器整体避让由
                # _layout_containers 负责并同步 cont_box）；但仍占位，让自由设备避让
                placed.append((x, y, w, h))
                continue
            guard = 0
            moved = True
            while moved and guard < 400:
                moved = False
                guard += 1
                for (ox, oy, ow, oh) in placed:
                    if abs(x - ox) < (w + ow) and abs(y - oy) < (h + oh):
                        # ★ v12g 修复：目标位置必须留出自身半宽 w，
                        #   否则中心只推到相邻（ox+ow+gap），自身框仍与前框重叠
                        x = ox + ow + gap + w
                        moved = True
                for (ox, oy, ow, oh) in cont_boxes_abs:
                    if abs(x - ox) < (w + ow) and abs(y - oy) < (h + oh):
                        x = ox + ow + gap + w
                        moved = True
            placed.append((x, y, w, h))
            self.pos[pid] = (self.snap(x), self.snap(y))
        # 统计剩余重叠（自由设备之间、自由设备与容器成员）
        n = 0
        for i in range(len(placed)):
            for j in range(i + 1, len(placed)):
                a, b2 = placed[i], placed[j]
                if abs(a[0] - b2[0]) < (a[2] + b2[2]) and abs(a[1] - b2[1]) < (a[3] + b2[3]):
                    n += 1
        print(f"  [布局避让] 剩余重叠 {n} 对")

    def _assign_ports(self):
        """★ 色框端点预分配

        原则：
          1. 每个设备最多 4 条线（左/右/上/下 4 个边各一个中点）
          2. 方向匹配优先：目标在右 → 优先 R
          3. 优先级：方向主边 > 垂直主边 > 其余
          4. 同向时 L/R > T/B（左/右优先）
          5. 选不到（>4 邻居）→ 强制分配到分数最低的可用 side（堆叠）

        结果写入 self.port_assign[(src, dst)] = 'L'|'R'|'T'|'B'
        """
        self.port_assign = {}
        used_sides = defaultdict(set)  # pid -> {'L','R','T','B'}

        # 收集所有 (u,v) 边，去重
        pairs = set()
        for u, vs in self.adj.items():
            if u not in self.pos:
                continue
            for v in vs:
                if v in self.pos and v != u:
                    pairs.add(tuple(sorted([u, v])))

        # 排序：度数高的设备优先分配（避免低度数被挤掉好边）
        def pair_deg(p):
            return -(len(self.adj.get(p[0], ())) + len(self.adj.get(p[1], ())))
        pair_list = sorted(pairs, key=pair_deg)

        for u, v in pair_list:
            # 给 u→v 和 v→u 各自分配（同一对边可以是不同 side）
            for src, dst in [(u, v), (v, u)]:
                side = self._pick_port_side(src, dst, used_sides[src])
                if side:
                    used_sides[src].add(side)
                    self.port_assign[(src, dst)] = side

        # 统计
        total = len(self.port_assign)
        by_dev = defaultdict(int)
        for (s, d), side in self.port_assign.items():
            by_dev[s] += 1
        over_4 = sum(1 for c in by_dev.values() if c > 4)
        print(f"  [端口分配] {total} 个端点对, >4连接的设备数: {over_4}")

    def _pick_port_side(self, src, dst, used):
        """根据 src→dst 方向选最优 side。
        优先级：方向匹配主边(0) > 垂直主边(1) > 剩余边(2)
        同分时 L/R > T/B（左/右优先）
        """
        sx, sy = self.pos[src]
        dx, dy = self.pos[dst]
        ddx = dx - sx
        ddy = dy - sy

        # 判断主方向
        scores = {'L': 999, 'R': 999, 'T': 999, 'B': 999}
        if abs(ddx) >= abs(ddy):
            # 水平为主
            primary = 'R' if ddx >= 0 else 'L'
            scores[primary] = 0
            scores['T'] = min(scores['T'], 2)
            scores['B'] = min(scores['B'], 2)
        else:
            # 垂直为主
            primary = 'B' if ddy >= 0 else 'T'
            scores[primary] = 0
            scores['L'] = min(scores['L'], 2)
            scores['R'] = min(scores['R'], 2)

        # 左/右优先（即使分数相同也先选 L/R）
        order = ['L', 'R', 'T', 'B']
        candidates = []
        for s in order:
            if s not in used:
                candidates.append((scores[s], s))
        if not candidates:
            return None
        # 按分数升序、同分按 L,R,T,B 顺序
        candidates.sort(key=lambda x: (x[0], order.index(x[1])))
        return candidates[0][1]

    def _find_root(self):
        # ★ v5 电源点优先（题目 5.1.1）：zf01 变电站框邻近、且从它能贯通全图的母线
        # 优先级：电源母线 > 历史默认根 > 度最大母线 > 度最大设备
        ROOT_PREF = {'LINE216.svg': 'TMP00044538', 'LINE215.svg': 'TMP00044536'}
        pref = ROOT_PREF.get(self.svg_filename)
        buses = [p for p, d in self.devices.items() if d['type'] in BUSBAR_TYPES]

        # 1. zf01 变电站框邻近的母线：取能贯通全图且度数最大的（跳过死路母线）
        zf01 = [p for p, d in self.devices.items() if d['type'] == 'zf01']
        if zf01 and buses:
            zx, zy = self.devices[zf01[0]]['orig_x'], self.devices[zf01[0]]['orig_y']
            cands = sorted(buses, key=lambda p: (
                -len(self.adj.get(p, ())),  # 度数大优先（电源母线连多条馈线）
                math.hypot(self.devices[p]['orig_x'] - zx, self.devices[p]['orig_y'] - zy)))
            for c in cands:
                if self._bfs_coverage(c) >= 0.9:
                    print(f"  [电源点] zf01 邻近母线 {c[:20]} 度={len(self.adj.get(c, ()))} 定为根")
                    return c

        if buses:
            deg = {p: len(self.adj.get(p, ())) for p in buses}
            m = max(deg.values())
            cands = [p for p in buses if deg[p] == m]
            if pref in cands:
                return pref
            return min(cands)
        if self.adj:
            deg = {p: len(self.adj[p]) for p in self.adj}
            m = max(deg.values())
            cands = [p for p in self.adj if deg[p] == m]
            if pref in cands:
                return pref
            return min(cands)
        return None

    def _bfs_coverage(self, root) -> float:
        """以 root 为根的 BFS 覆盖真实设备比例（用于电源点判定）"""
        real_ids = [p for p, d in self.devices.items() if self.is_real_device(d['type'])]
        if not real_ids:
            return 0.0
        seen = set()
        q = deque([root])
        seen.add(root)
        while q:
            u = q.popleft()
            for v in self.adj.get(u, ()):
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        covered = sum(1 for p in real_ids if p in seen)
        return covered / len(real_ids)

    def _layout_containers(self, cont_rep):
        # 【Step 4 修复】容器内设备间距从 130px 改为 80px，保证疏密均匀
        CONT_ROW_H = 80  # 容器内每行高度（原130过大，现80符合规范"间距均匀"）
        CONT_TOP = 75    # 容器顶部留白（标签栏+首行标注）
        CONT_BOT = 45    # 【新增】容器底部留白（用于进出线引出空间）
        CONT_W = 110
        for cid, c in self.containers.items():
            ms = [m for m in c['members'] if m in self.pos]
            rep = cont_rep.get(cid)
            if rep is None or rep not in self.pos:
                continue
            rx, ry = self.pos[rep]
            if len(ms) < 2:
                # ★ v12f：空/单成员容器按设备框口径建最小容器框，
                #   与进出线端口（_dev_box_edges 的 box 边）精确对齐，消除悬空线头
                try:
                    l, r, t, b = self._dev_box_edges(rep)
                except Exception:
                    l, r, t, b = -34.0, 34.0, -36.0, 40.0
                self.cont_box[cid] = (self.snap(rx + l), self.snap(ry + t),
                                      self.snap(rx + r), self.snap(ry + b))
                continue
            type_order = {'0311': 0, '0307': 1, '0201': 2, '0202': 3,
                          '0302': 4, '0306': 5, '0305': 6}
            buses = sorted([m for m in ms if self.devices[m]['type'] in BUSBAR_TYPES],
                           key=lambda m: type_order.get(self.devices[m]['type'], 9))
            rest = sorted([m for m in ms if m not in buses],
                          key=lambda m: type_order.get(self.devices[m]['type'], 9))
            ordered = buses + rest
            for i, pid in enumerate(ordered):
                self.pos[pid] = (self.snap(rx), self.snap(ry + i * CONT_ROW_H))
            xs = [self.pos[m][0] for m in ms]
            ys = [self.pos[m][1] for m in ms]
            cx = sum(xs) / len(xs)
            x1 = cx - CONT_W // 2
            x2 = cx + CONT_W // 2
            y1 = min(ys) - CONT_TOP
            # 【Step 1 修复】容器底部留出 CONT_BOT 空间给进出线
            y2 = max(ys) + CONT_PAD + UNIT_V // 2 + CONT_BOT
            self.cont_box[cid] = (self.snap(x1), self.snap(y1), self.snap(x2), self.snap(y2))

        # ---- 容器碰撞避让：按x从左到右，右侧容器若与左侧容器y重叠且x重叠，则整体右移 ----
        sorted_cids = sorted(self.cont_box.keys(), key=lambda c: self.cont_box[c][0])
        GAP = 80  # 容器间最小水平间隙
        for idx, cid in enumerate(sorted_cids):
            if idx == 0:
                continue
            cx1, cy1, cx2, cy2 = self.cont_box[cid]
            # 找左边所有与当前容器y范围重叠的容器，取最大右边界
            need_x = cx1
            for left_cid in sorted_cids[:idx]:
                lx1, ly1, lx2, ly2 = self.cont_box[left_cid]
                # y范围不重叠则跳过
                if cy2 < ly1 or ly2 < cy1:
                    continue
                if lx2 + GAP > need_x:
                    need_x = lx2 + GAP
            if need_x > cx1:
                dx = need_x - cx1
                # 整体右移容器内所有设备
                ms = [m for m in self.containers[cid]['members'] if m in self.pos]
                if not ms:
                    # ★ v12f：空容器无成员可移，直接平移容器框
                    x1, y1, x2, y2 = self.cont_box[cid]
                    self.cont_box[cid] = (self.snap(x1 + dx), y1, self.snap(x2 + dx), y2)
                    rep2 = cont_rep.get(cid)
                    if rep2 is not None and rep2 in self.pos:
                        px, py = self.pos[rep2]
                        self.pos[rep2] = (self.snap(px + dx), py)
                    continue
                for m in ms:
                    px, py = self.pos[m]
                    self.pos[m] = (self.snap(px + dx), py)
                # 重新计算容器框
                xs = [self.pos[m][0] for m in ms]
                ys = [self.pos[m][1] for m in ms]
                cxc = sum(xs) / len(xs)
                self.cont_box[cid] = (self.snap(cxc - CONT_W // 2), self.snap(min(ys) - CONT_TOP),
                                       self.snap(cxc + CONT_W // 2), self.snap(max(ys) + CONT_PAD + UNIT_V // 2 + CONT_BOT))

        # ---- 容器顶部避让：检测容器顶部是否伸入上方设备层，有则整体下移 ----
        TOP_GAP = 35  # 容器顶部与上方设备层的最小间距
        # 收集所有设备的y坐标（按层去重，主干线横跨全图，包括其他容器成员）
        all_dev_ys = set()
        for pid, (px, py) in self.pos.items():
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            all_dev_ys.add(py)

        for cid in sorted(self.cont_box.keys(), key=lambda c: self.cont_box[c][1]):
            cx1, cy1, cx2, cy2 = self.cont_box[cid]
            ms = [m for m in self.containers[cid]['members'] if m in self.pos]
            if not ms:
                continue
            min_dev_y = min(self.pos[m][1] for m in ms)
            # 当前容器成员的y层（排除这些，因为它们在容器内部）
            self_ys = set(self.pos[m][1] for m in ms)
            # 找上方最近的设备层（最大y且 < min_dev_y，排除当前容器成员层）
            max_above_y = max((y for y in all_dev_ys if y < min_dev_y and y not in self_ys), default=-999999)
            if max_above_y == -999999:
                continue
            # 容器顶部 = min_dev_y - CONT_TOP，需与上方设备层间距 >= TOP_GAP
            needed_top = max_above_y + TOP_GAP
            current_top = min_dev_y - CONT_TOP
            if current_top < needed_top:
                dy = needed_top - current_top
                for m in ms:
                    px, py = self.pos[m]
                    self.pos[m] = (px, self.snap(py + dy))
                xs = [self.pos[m][0] for m in ms]
                ys = [self.pos[m][1] for m in ms]
                cxc = sum(xs) / len(xs)
                self.cont_box[cid] = (self.snap(cxc - CONT_W // 2), self.snap(min(ys) - CONT_TOP),
                                       self.snap(cxc + CONT_W // 2), self.snap(max(ys) + CONT_PAD + UNIT_V // 2 + CONT_BOT))

        # ---- 非柜箱设备避让：不属于任何柜箱的设备若落在柜箱框内，则水平移出 ----
        cont_member_set = set()
        for cid, cdata in self.containers.items():
            for m in cdata.get('members', []):
                cont_member_set.add(m)
        SIDE_GAP = 50  # 移出柜箱后与柜箱边框的最小间距
        for pid, (px, py) in list(self.pos.items()):
            if pid in cont_member_set:
                continue
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            try:
                _l, _r, _t, _b = self._dev_box_edges(pid)
                hw_local = (_r - _l) / 2.0 + 4   # 真实色框半宽 + 余量
                hh_local = (_b - _t) / 2.0 + 4   # 真实色框半高 + 余量
            except Exception:
                hw_local, hh_local = 38, 44
            # 检查色框是否与某个柜箱框重叠（含标题栏，留5px余量）
            for cid, (cx1, cy1, cx2, cy2) in self.cont_box.items():
                if (px + hw_local > cx1 + 5 and px - hw_local < cx2 - 5 and
                        py + hh_local > cy1 + 5 and py - hh_local < cy2 - 5):
                    # 落在柜箱内，移到较近的一侧
                    dist_left = px - cx1
                    dist_right = cx2 - px
                    if dist_left <= dist_right:
                        new_x = cx1 - hw_local - SIDE_GAP
                    else:
                        new_x = cx2 + hw_local + SIDE_GAP
                    self.pos[pid] = (self.snap(new_x), py)
                    break

    def _normalize(self):
        if not self.pos:
            return
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        for (a, b, c, d) in self.cont_box.values():
            xs += [a, c]
            ys += [b, d]
        LABEL_PAD_X = 120  # 标注可能放在设备左右侧，预留水平空间防止越界
        ox, oy = -min(xs) + MARGIN + LABEL_PAD_X, -min(ys) + MARGIN
        self.pos = {p: (self.snap(x + ox), self.snap(y + oy)) for p, (x, y) in self.pos.items()}
        self.cont_box = {c: (self.snap(a + ox), self.snap(b + oy),
                            self.snap(c2 + ox), self.snap(d + oy))
                         for c, (a, b, c2, d) in self.cont_box.items()}

    # ═══════════════════════════════════════════════════════════
    #  渲染（正交布线 + 母线 + 标注白底避让）
    # ═══════════════════════════════════════════════════════════

    def render(self, out_path: str):
        if not self.pos:
            print("  [渲染] 无布局数据")
            return
        # ★ v12f：容器框与 rep 位置强制同步——布局后 _fix_overlaps 等可能平移设备，
        #   导致 cont_box 与 pos 漂移，进出线端口悬空。以 rep 当前 pos + 设备框边
        #   重算容器框；成员容器以成员 y 范围重算（保持底部引出空间）。
        for cid, cb in list(self.cont_box.items()):
            c = self.containers.get(cid, {})
            ms = [m for m in c.get('members', []) if m in self.pos]
            rep = self._cont_rep_map.get(cid) if hasattr(self, '_cont_rep_map') else None
            if rep is None or rep not in self.pos:
                continue
            rx, ry = self.pos[rep]
            if len(ms) < 2:
                try:
                    l, r, t, b = self._dev_box_edges(rep)
                except Exception:
                    l, r, t, b = -34.0, 34.0, -36.0, 40.0
                self.cont_box[cid] = (self.snap(rx + l), self.snap(ry + t),
                                      self.snap(rx + r), self.snap(ry + b))
            else:
                xs = [self.pos[m][0] for m in ms]
                ys = [self.pos[m][1] for m in ms]
                cxc = sum(xs) / len(xs)
                # 与 _layout_containers 同口径：CONT_W=110/CONT_TOP=75/CONT_BOT=45
                self.cont_box[cid] = (self.snap(cxc - 55), self.snap(min(ys) - 75),
                                      self.snap(cxc + 55),
                                      self.snap(max(ys) + CONT_PAD + UNIT_V // 2 + 45))
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        for (a, b, c, d) in self.cont_box.values():
            xs += [a, c]
            ys += [b, d]
        LABEL_PAD_X = 120  # 与 _normalize 对齐：右侧标注预留空间
        W = self.snap(max(xs) + MARGIN + LABEL_PAD_X)
        H = self.snap(max(ys) + MARGIN)

        svg = ET.Element(f'{{{SVG_NS}}}svg', {
            'viewBox': f'0 0 {W} {H}',
            'width': str(W), 'height': str(H),
            'style': f'background-color:{C_BG};font-family:"Microsoft YaHei","SimHei",sans-serif;',
        })
        if self.doc and self.doc.root is not None:
            defs = self.doc.root.find(f'{{{SVG_NS}}}defs')
            if defs is not None:
                svg.append(copy.deepcopy(defs))

        cg = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'ConnLine_Layer'})
        self._draw_wires(cg)

        g = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'MainLayer'})
        self._draw_devices(g)
        self._draw_containers(g)
        self._draw_labels(g)

        ET.ElementTree(svg).write(out_path, encoding='utf-8', xml_declaration=True)
        print(f"  [渲染] {out_path}  {W} x {H}")

    def _draw_title(self, svg, W):
        tg = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'TitleBar'})
        ET.SubElement(tg, f'{{{SVG_NS}}}rect', {
            'x': '0', 'y': '0', 'width': str(W), 'height': str(TITLE_H),
            'fill': '#1a3a6b',
        })
        line_name = self.svg_filename.replace('.svg', '')
        t1 = ET.SubElement(tg, f'{{{SVG_NS}}}text', {
            'x': '16', 'y': '34', 'fill': '#fff',
            'font-size': str(F_TITLE), 'font-weight': 'bold',
        })
        t1.text = f'配电网单线图 — {line_name}（标准化美化）'
        ndev = len(self.pos)
        ncont = len(self.cont_box)
        ntie = len(self.non_tree_edges)
        t2 = ET.SubElement(tg, f'{{{SVG_NS}}}text', {
            'x': f'{W - 16}', 'y': '34', 'fill': '#aaccff',
            'font-size': str(F_BRANCH), 'text-anchor': 'end',
        })
        t2.text = f'设备 {ndev} | 柜箱 {ncont} | 联络 {ntie} | 10kV | 权重树算法'

    def _draw_containers(self, g):
        for cid, (x1, y1, x2, y2) in self.cont_box.items():
            c = self.containers.get(cid, {})
            name = c.get('name', f'柜_{cid[:6]}')
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': str(x1), 'y': str(y1),
                'width': str(x2 - x1), 'height': str(y2 - y1),
                'fill': CONTAINER_BG_FILL, 'fill-opacity': CONTAINER_BG_OPACITY,
                'stroke': C_CONTAINER,
                'stroke-width': str(W_CONTAINER), 'rx': '3',
            })
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': str(x1), 'y': str(y1),
                'width': str(x2 - x1), 'height': '16',
                'fill': '#f0f0f0', 'fill-opacity': '0.6', 'stroke': 'none', 'rx': '3',
            })
            t = ET.SubElement(g, f'{{{SVG_NS}}}text', {
                'x': str(x1 + 4), 'y': str(y1 + 12),
                'fill': C_TEXT, 'font-size': '11', 'font-weight': 'bold',
            })
            t.text = name

    def _safe_exit_x(self, px, side):
        """端口出盒安全列：从端口沿法线走出 EXIT_STEP（落在列间隙，避免穿同列/邻列设备）"""
        EXIT_STEP = 52.0
        if side == 'L':
            return px - EXIT_STEP
        return px + EXIT_STEP

    def _nearest_gap_y(self, y, boxes):
        """最近的空白带 y（水平段安全通道）：扫描上下，返回首个不与任何盒 y 重叠的位置"""
        cands = [y]
        step = 10.0
        for i in range(1, 60):
            cands.append(y + i * step)
            cands.append(y - i * step)
        for cy in cands:
            ok = True
            for pid, (bx1, by1, bx2, by2) in boxes.items():
                if by1 - 6 <= cy <= by2 + 6:
                    ok = False
                    break
            if ok:
                return cy
        return y

    @staticmethod
    def _l_shape(p_abs, c_abs):
        """L 形折线：端点不同行且不同列时，先横后竖（3 点）。
        当两端已在同一行/列时直接退化为 2 点。"""
        if abs(p_abs[1] - c_abs[1]) < 0.5:
            return [[p_abs, c_abs]]
        if abs(p_abs[0] - c_abs[0]) < 0.5:
            return [[p_abs, c_abs]]
        return [[p_abs, (c_abs[0], p_abs[1]), c_abs]]

    def _z_shape(self, p_abs, c_abs, par, child):
        """Z 形正交路径：出盒安全列 + 行间通道，全程横平竖直且不穿设备列/行"""
        boxes = self._device_boxes_abs()
        par_side = self._get_port_side(par, child)
        child_side = self._get_port_side(child, par)
        ex_p = self._safe_exit_x(p_abs[0], par_side)
        ex_c = self._safe_exit_x(c_abs[0], child_side)
        # 通道：两端 y 各自最近的空白带（优先中间统一通道以减少垂直长线）
        chan = self._nearest_gap_y((p_abs[1] + c_abs[1]) / 2.0, boxes)
        pts = [p_abs,
               (ex_p, p_abs[1]),
               (ex_p, chan),
               (ex_c, chan),
               (ex_c, c_abs[1]),
               c_abs]
        # 合并共线点
        out = [pts[0]]
        for p in pts[1:]:
            if abs(out[-1][0] - p[0]) > 0.1 or abs(out[-1][1] - p[1]) > 0.1:
                out.append(p)
        return out

    @staticmethod
    def _seg_hits_box(seg, box, tol=1.0):
        """线段（水平/垂直）是否穿过 box 内部（端点贴边不算穿）"""
        (x1, y1), (x2, y2) = seg
        bx1, by1, bx2, by2 = box
        if abs(y1 - y2) < 0.5:  # 水平段
            y = y1
            if not (by1 + tol < y < by2 - tol):
                return False
            xa, xb = min(x1, x2), max(x1, x2)
            return xb > bx1 + tol and xa < bx2 - tol
        if abs(x1 - x2) < 0.5:  # 垂直段
            x = x1
            if not (bx1 + tol < x < bx2 - tol):
                return False
            ya, yb = min(y1, y2), max(y1, y2)
            return yb > by1 + tol and ya < by2 - tol
        return False

    def _detour_once(self, seg, box, boxes, tol=6.0):
        """单个穿框段绕行：水平段绕到框上/下方最近空白行，垂直段绕到左/右空白列。
        返回绕行后的多点路径（不穿任何框）；找不到空白带返回 None（保持原样）。"""
        (x1, y1), (x2, y2) = seg
        bx1, by1, bx2, by2 = box
        if abs(y1 - y2) < 0.5:
            xa, xb = min(x1, x2), max(x1, x2)
            for cand in (by1 - tol - 14, by2 + tol + 14,
                         by1 - tol - 28, by2 + tol + 28,
                         by1 - tol - 42, by2 + tol + 42,
                         by1 - tol - 56, by2 + tol + 56,
                         by1 - tol - 70, by2 + tol + 70):
                ok = True
                for b in boxes:
                    if b is box:
                        continue
                    bx1_, by1_, bx2_, by2_ = b
                    if by1_ - tol < cand < by2_ + tol and not (bx2_ < xa - tol or bx1_ > xb + tol):
                        ok = False
                        break
                if ok:
                    return [(x1, y1), (x1, cand), (x2, cand), (x2, y2)]
            return None
        else:
            ya, yb = min(y1, y2), max(y1, y2)
            for cand in (bx1 - tol - 14, bx2 + tol + 14,
                         bx1 - tol - 28, bx2 + tol + 28,
                         bx1 - tol - 42, bx2 + tol + 42,
                         bx1 - tol - 56, bx2 + tol + 56):
                ok = True
                for b in boxes:
                    if b is box:
                        continue
                    bx1_, by1_, bx2_, by2_ = b
                    if bx1_ - tol < cand < bx2_ + tol and not (by2_ < ya - tol or by1_ > yb + tol):
                        ok = False
                        break
                if ok:
                    return [(x1, y1), (cand, y1), (cand, y2), (x2, y2)]
            return None

    def _detour_reroute(self, pts, boxes, max_detour=2):
        """整条线逐段穿框检测 + 帽子绕行。每段最多绕一次，整线最多 max_detour 次；
        绕行路径不穿其他框（候选带已校验），绕行段仍穿框则保留原段。"""
        new_pts = [pts[0]]
        n_detour = 0
        for seg in zip(pts, pts[1:]):
            hit = None
            for b in boxes:
                if self._seg_hits_box(seg, b):
                    hit = b
                    break
            if hit is None or n_detour >= max_detour:
                new_pts.append(seg[1])
                continue
            route = self._detour_once(seg, hit, boxes)
            if route is None:
                new_pts.append(seg[1])
                continue
            # 绕行路径自身不能再穿框（候选带已校验；垂直短段在端点列，贴自身框边可容忍）
            n_detour += 1
            new_pts.extend(route[1:])
        # 合并共线点 + 去重复点
        res = []
        for p in new_pts:
            if res and abs(res[-1][0] - p[0]) < 0.5 and abs(res[-1][1] - p[1]) < 0.5:
                continue
            if len(res) >= 2:
                v1 = (res[-1][0] - res[-2][0], res[-1][1] - res[-2][1])
                v2 = (p[0] - res[-1][0], p[1] - res[-1][1])
                if abs(v1[0] * v2[1] - v1[1] * v2[0]) < 1e-6:
                    res.pop()
            res.append(p)
        return res if len(res) >= 2 else None

    def _hseg_cross_devices(self, x1, x2, y, par, child):
        """水平段是否穿过非端点设备色框"""
        boxes = self._device_boxes_abs()
        lo, hi = (min(x1, x2), max(x1, x2))
        hits = []
        for pid, (bx1, by1, bx2, by2) in boxes.items():
            if pid in (par, child):
                continue
            if by1 - 2 <= y <= by2 + 2 and not (hi < bx1 or lo > bx2):
                hits.append(pid)
        return hits

    def _vseg_cross_devices(self, x, y1, y2, par, child):
        """垂直段是否穿过非端点设备色框"""
        boxes = self._device_boxes_abs()
        lo, hi = (min(y1, y2), max(y1, y2))
        hits = []
        for pid, (bx1, by1, bx2, by2) in boxes.items():
            if pid in (par, child):
                continue
            if bx1 - 2 <= x <= bx2 + 2 and not (hi < by1 or lo > by2):
                hits.append(pid)
        return hits

    def _reserve_bus_tap(self, bus_id, bus_y, x):
        """母线 T 接点占位：同一 (母线, y) 上同 x 的 T 接点沿母线错开，保证一点一线"""
        if not hasattr(self, '_bus_tap_used'):
            self._bus_tap_used = {}
        key = (bus_id, round(bus_y))
        s = self._bus_tap_used.setdefault(key, set())
        if x not in s:
            s.add(x)
            return x
        step = 24
        for k in range(1, 40):
            for cand in (x + k * step, x - k * step):
                if cand not in s:
                    s.add(cand)
                    return cand
        cand = x + 80
        s.add(cand)
        return cand

    def _make_wire_segs(self, par, child, x1, y1, x2, y2):
        """★ v2 排线（题目 5.1.4 / 5.1.2）：
          - 端点贴色框边中点（port_assign，L/R 优先，避免上下穿过元件）
          - 跨容器边一律从容器底部引出（柜内→底边→水平→目标）
          - 常规边按端口方向走 L 形（先水平后垂直 / 先垂直后水平）
          - 穿容器段绕行（避障）

        返回 List[ [(x,y), ...] ], 每项是一段 polyline
        """
        # ★ 使用 port_assign 拿端口 side
        par_side = self._get_port_side(par, child)
        child_side = self._get_port_side(child, par)
        ptx, pty = self._port_offset(par, par_side)
        ctx, cty = self._port_offset(child, child_side)

        # 绝对坐标（紧贴色框边的中点）
        p_abs = (x1 + ptx, y1 + pty)
        c_abs = (x2 + ctx, y2 + cty)

        # ★ 母线端点 T 接：母线无色框，线端点接到"母线横线"（对方 x 投影到母线 y）
        _par_is_bus = self.devices.get(par, {}).get('type') in BUSBAR_TYPES
        _child_is_bus = self.devices.get(child, {}).get('type') in BUSBAR_TYPES
        if _par_is_bus and not _child_is_bus:
            tap_x = self._reserve_bus_tap(par, y1, x2)
            p_abs = (tap_x, y1)   # T 接点：母线 y 上错位后的 x
            c_cid = self._get_container_id_of(child)
            if c_cid:
                # ★ v12h：母线连接容器内设备 → 从容器底部引出（题目 5.1.4），
                #   避免 T 接垂直线从顶部穿入容器框（"母线被上箱柜"）
                by = self._container_bottom_y(c_cid) + 20.0
                try:
                    cxt, cyt = self._port_offset(child, 'B')
                except Exception:
                    cxt, cyt = 0, 30
                c_bot = (x2 + cxt, y2 + cyt)
                # T 接点若落在容器框 x 区间内 → 移到框边外侧（母线横线挖框后无支撑）
                cb = self.cont_box.get(c_cid)
                tap_ok = tap_x
                if cb is not None and cb[0] - 2 < tap_x < cb[2] + 2:
                    tap_ok = cb[0] - 14 if (tap_x - cb[0]) <= (cb[2] - tap_x) else cb[2] + 14
                tap_ok = self._bus_tap_on_seg(par, y1, tap_ok)
                p_abs = (tap_ok, y1)
                return [[p_abs, (tap_ok, by), (c_bot[0], by), c_bot]]
            tap_x = self._bus_tap_on_seg(par, y1, tap_x)
            p_abs = (tap_x, y1)
            if abs(tap_x - x2) > 0.5:
                # 错位 T 接：child 顶部端点 → 母线下方横线 → 母线 T 接点
                try:
                    cxt, cyt = self._port_offset(child, 'T')
                except Exception:
                    cxt, cyt = 0, -30
                c_top = (x2 + cxt, y2 + cyt)
                mid_y = y1 - 24
                return [[c_top, (x2, mid_y), (tap_x, mid_y), p_abs]]
        elif _child_is_bus and not _par_is_bus:
            tap_x = self._reserve_bus_tap(child, y2, x1)
            c_abs = (tap_x, y2)   # T 接点：母线 y 上错位后的 x
            p_cid2 = self._get_container_id_of(par)
            if p_cid2:
                # ★ v12h：容器内设备连接母线 → 从容器底部引出（题目 5.1.4）
                by = self._container_bottom_y(p_cid2) + 20.0
                try:
                    pxt, pyt = self._port_offset(par, 'B')
                except Exception:
                    pxt, pyt = 0, 30
                p_bot = (x1 + pxt, y1 + pyt)
                cb = self.cont_box.get(p_cid2)
                tap_ok = tap_x
                if cb is not None and cb[0] - 2 < tap_x < cb[2] + 2:
                    tap_ok = cb[0] - 14 if (tap_x - cb[0]) <= (cb[2] - tap_x) else cb[2] + 14
                tap_ok = self._bus_tap_on_seg(child, y2, tap_ok)
                c_abs = (tap_ok, y2)
                return [[p_bot, (p_bot[0], by), (tap_ok, by), c_abs]]
            tap_x = self._bus_tap_on_seg(child, y2, tap_x)
            c_abs = (tap_x, y2)
            if abs(tap_x - x1) > 0.5:
                try:
                    cxt, cyt = self._port_offset(par, 'T')
                except Exception:
                    cxt, cyt = 0, -30
                p_top = (x1 + cxt, y1 + cyt)
                mid_y = y2 - 24
                return [[p_top, (x1, mid_y), (tap_x, mid_y), c_abs]]

        # 端点距离
        ep_dist = math.hypot(p_abs[0] - c_abs[0], p_abs[1] - c_abs[1])

        # 太近: 直接连
        if ep_dist < 1.5:
            return [[p_abs, c_abs]]

        GRID_SNAP = 0.5  # 浮点容差
        segs = []
        p_cid = self._get_container_id_of(par)
        c_cid = self._get_container_id_of(child)

        # ★ 跨容器边：从容器底部引出（题目 5.1.4）
        EXIT_MARGIN = 20.0
        if p_cid and c_cid != p_cid:
            by = self._container_bottom_y(p_cid) + EXIT_MARGIN
            segs = [[p_abs, (p_abs[0], by), (c_abs[0], by), c_abs]]
        elif c_cid and c_cid != p_cid:
            by = self._container_bottom_y(c_cid) + EXIT_MARGIN
            segs = [[p_abs, (p_abs[0], by), (c_abs[0], by), c_abs]]
        elif abs(p_abs[1] - c_abs[1]) < GRID_SNAP:
            # 同 Y: 水平直接连（一段）；若中间有设备则用 Z 形绕开
            mid_hits = self._hseg_cross_devices(p_abs[0], c_abs[0], p_abs[1], par, child)
            if mid_hits:
                segs = [self._z_shape(p_abs, c_abs, par, child)]
            else:
                segs = [[p_abs, c_abs]]
        elif abs(p_abs[0] - c_abs[0]) < GRID_SNAP:
            # 同 X: 垂直直接连（一段）；若中间有设备则用 Z 形绕开
            mid_hits = self._vseg_cross_devices(p_abs[0], p_abs[1], c_abs[1], par, child)
            if mid_hits:
                segs = [self._z_shape(p_abs, c_abs, par, child)]
            else:
                segs = [[p_abs, c_abs]]
        else:
            # ★ A1 修复：优先 L 形（先横后竖，3 点）。仅当 L 形横段/竖段
            # 真正穿过其他设备色框时，才升级为 Z 形（6 点，安全列绕开）。
            # 旧版本无差别一律 Z 形，导致 78% 的连线都长成 6 点折线。
            l_pts = self._l_shape(p_abs, c_abs)
            # 检查 L 形的水平段是否会穿过非端点设备色框
            # L 形 = p_abs -> (c_abs.x, p_abs.y) -> c_abs；
            # 水平段 x 范围 [min(p_abs.x, c_abs.x), max(...)]，y = p_abs.y
            mid_hits = self._hseg_cross_devices(p_abs[0], c_abs[0],
                                                p_abs[1], par, child)
            if mid_hits:
                segs = [self._z_shape(p_abs, c_abs, par, child)]
            else:
                segs = l_pts

        # ★ v12b：禁用容器避障迭代（该迭代把线绕成几十上百点的小矩形环/折返线头）
        # 跨容器边已从容器底部引出（5.1.4），常规 Z 形走安全列+通道，穿容器由布局密度兜底
        # avoided = []
        # for seg in segs:
        #     pts = self._adjust_path_to_avoid_containers(list(seg), par, child)
        #     avoided.append(pts)
        # segs = avoided

        # 清理：去除共线小段（合并水平/垂直相接的段）
        merged_pts = []
        for seg in segs:
            for p in seg:
                if not merged_pts or math.hypot(merged_pts[-1][0] - p[0], merged_pts[-1][1] - p[1]) > 0.05:
                    merged_pts.append(p)
        cleaned = [merged_pts] if len(merged_pts) >= 2 else segs
        return cleaned

    def _collinear_merge(self, segs):
        """合并共线相接的线段。
        例如 [[(0,0),(10,0)], [(10,0),(10,5)], [(10,5),(20,5)]] 
        → [[(0,0),(10,0),(10,5),(20,5)]]
        """
        if not segs:
            return []
        merged = [list(segs[0])]
        for seg in segs[1:]:
            last = merged[-1]
            last_end = last[-1]
            seg_start = seg[0]
            # 检查 last_end 和 seg_start 是否相同（共点）
            if (abs(last_end[0] - seg_start[0]) < 0.1 and
                abs(last_end[1] - seg_start[1]) < 0.1):
                # 共点 → 合并（去掉 seg 的起点）
                merged[-1] = last + seg[1:]
            else:
                merged.append(list(seg))
        # 清理：去除重复点，过滤长度<0.1 的段
        cleaned = []
        for seg in merged:
            new_seg = []
            for p in seg:
                if not new_seg or math.hypot(new_seg[-1][0] - p[0], new_seg[-1][1] - p[1]) > 0.05:
                    new_seg.append(p)
            if len(new_seg) >= 2:
                cleaned.append(new_seg)
        return cleaned

    def _draw_wires(self, g):
        conn_idx = 0
        self._wire_segs = []  # 收集所有线段，末尾合并去重

        # 生成树边（主干+分支）
        # 主干宽度判定：母线相关边 / 电源近端深度<=2 的边用粗线，其余分支 1.5
        _depth = {}
        for _c, _p in self.tree_parent.items():
            _depth[_c] = (_depth.get(_p, -1) + 1) if _p is not None else 0
        for child, par in self.tree_parent.items():
            if par is None or child not in self.pos or par not in self.pos:
                continue
            if not (is_real(self.devices.get(child)) and is_real(self.devices.get(par))):
                continue
            x1, y1 = self.pos[par]
            x2, y2 = self.pos[child]
            _is_bus = (self.devices[par]['type'] in BUSBAR_TYPES
                       or self.devices[child]['type'] in BUSBAR_TYPES)
            is_trunk = _is_bus or _depth.get(child, 9) <= 2
            w = W_TRUNK if is_trunk else W_BRANCH
            conn_idx += 1
            conn_id = f'WIRE_{conn_idx:06d}'

            # ★ 布线：多段拼接式（端点=色框边中点，L形三段折线）
            segs = self._make_wire_segs(par, child, x1, y1, x2, y2)
            for seg_idx, seg in enumerate(segs):
                seg_id = f"{conn_id}_{seg_idx:02d}"
                self._wire_segs.append((seg, C_10KV, w, seg_id, par, child))

        # 母线：一条完整连续横线（覆盖所有连接设备 x 范围），T 接点落在母线上
        drawn = set()
        for pid, d in self.devices.items():
            if d['type'] not in BUSBAR_TYPES or pid not in self.pos:
                continue
            conn = [p for p in self.adj.get(pid, ()) if p in self.pos]
            if not conn:
                continue
            conn_sorted = sorted(conn, key=lambda p: self.pos[p][0])
            y = self.pos[pid][1]
            a_id, b_id = conn_sorted[0], conn_sorted[-1]
            a_left, a_right, _, _ = self._dev_box_edges(a_id)
            b_left, b_right, _, _ = self._dev_box_edges(b_id)
            x_start = self.pos[a_id][0] + a_left
            x_end = self.pos[b_id][0] + b_right
            if abs(x_start - x_end) < 0.5:
                continue
            key = (round(x_start), round(x_end), round(y))
            if key in drawn:
                continue
            drawn.add(key)
            # ★ v12h：母线横线挖掉穿过的容器框区间（母线不"上箱柜"）；
            #   容器内设备的连接已由 T 接分支改为容器底部引出
            self._build_bus_segments()
            bus_segs = self._bus_segs.get((pid, round(y)))
            if not bus_segs:
                bus_segs = self._split_bus_seg(x_start, y, x_end)
            for (sx1, sx2) in bus_segs:
                if sx2 - sx1 < 0.5:
                    continue
                conn_idx += 1
                seg_id = f'BUS_{conn_idx:06d}'
                self._wire_segs.append(([(sx1, y), (sx2, y)], C_BUSBAR, W_BUSBAR, seg_id, pid, b_id))

        # ★ 环路补边：非树边（补回生成树算法丢弃的连接）
        # 颜色语义：仅"跨站房/跨馈线"才用联络橙 C_TIE；同容器/无容器/母线参与均属
        # 馈线内部连接，按主干/分支绿色绘制，避免单线图内部连线被误标为联络。
        # ★ v12g：按"接线数量补齐"原则绘制非树边——设备真实邻接数 > 已画数时才补画，
        #   保证每个元件接线数量与原图一致，同时接满的设备不画冗余边（避免网格状）。
        drawn_pairs = set()
        drawn_deg = defaultdict(int)
        for child, par in self.tree_parent.items():
            if par is not None:
                drawn_pairs.add(tuple(sorted([child, par])))
                drawn_deg[child] += 1
                drawn_deg[par] += 1
        for (u, v) in self.non_tree_edges:
            if u not in self.pos or v not in self.pos:
                continue
            if not (is_real(self.devices.get(u)) and is_real(self.devices.get(v))):
                continue
            key = tuple(sorted([u, v]))
            if key in drawn_pairs:
                continue
            u_c = self.devices.get(u, {}).get('ssjg') or ''
            v_c = self.devices.get(v, {}).get('ssjg') or ''
            u_t = self.devices.get(u, {}).get('type', '')
            v_t = self.devices.get(v, {}).get('type', '')
            is_bus_edge = u_t in BUSBAR_TYPES or v_t in BUSBAR_TYPES
            # 母线相关非树边不重复画：母线横线(BUS_) + 树边 T 接已表达全部母线连接，
            # 再画非树边会堆积大量重复 T 接（母线 deg 高 → deg 判定失效 → 网格状）
            if is_bus_edge:
                continue
            # 接线数量判定：两端都已接满真实邻接数 → 该冗余边不画
            real_u = len(self.adj.get(u, ()))
            real_v = len(self.adj.get(v, ()))
            if drawn_deg[u] >= real_u and drawn_deg[v] >= real_v:
                continue
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            conn_idx += 1
            drawn_deg[u] += 1
            drawn_deg[v] += 1
            is_internal = is_bus_edge or (not (u_c and v_c)) or (u_c == v_c)
            if is_internal:
                conn_id = f'WIRE_{conn_idx:06d}'
                edge_color = C_10KV
                edge_w = W_BUSBAR if is_bus_edge else W_BRANCH
            else:
                conn_id = f'TIE_{conn_idx:06d}'
                edge_color = C_TIE
                edge_w = W_TIE
            # 【B-mini 修复】删掉"先手算 points + 再调 _make_wire_segs"的双轨制。
            # 旧版先按方向生成 4 段折线（points），然后立刻被 _make_wire_segs 覆盖，
            # 既浪费一次计算又埋下"两端点不一致"隐患。仅保留 _make_wire_segs 单轨。
            segs = self._make_wire_segs(u, v, x1, y1, x2, y2)
            for seg_idx, seg in enumerate(segs):
                seg_id = f"{conn_id}_{seg_idx:02d}"
                self._wire_segs.append((seg, edge_color, edge_w, seg_id, u, v))

        # ★ 补充：原始 SVG 连接中未被 adj 图捕获的边（防止连线数量下降）
        for elem in self.doc.connections:
            s_id = elem.start_device_id
            e_id = elem.end_device_id
            if not s_id or not e_id or s_id == e_id:
                continue
            if s_id not in self.pos or e_id not in self.pos:
                continue
            if not (is_real(self.devices.get(s_id)) and is_real(self.devices.get(e_id))):
                continue
            key = tuple(sorted([s_id, e_id]))
            if key in drawn_pairs:
                continue
            drawn_pairs.add(key)
            x1, y1 = self.pos[s_id]
            x2, y2 = self.pos[e_id]
            conn_idx += 1
            conn_id = f'CONN_{conn_idx:06d}'
            # 【B-mini 修复】同上：直接调 _make_wire_segs，不手算 points
            segs = self._make_wire_segs(s_id, e_id, x1, y1, x2, y2)
            for seg_idx, seg in enumerate(segs):
                seg_id = f"{conn_id}_{seg_idx:02d}"
                self._wire_segs.append((seg, C_10KV, W_BRANCH, seg_id, s_id, e_id))

        # ★ 线段合并去重：同几何同色只画一次，宽度取最大值，from/to 全保留
        merged = {}
        order = []
        for pts, color, width, cid, fid, tid in self._wire_segs:
            key = (tuple((round(x), round(y)) for x, y in pts), color)
            if key in merged:
                m = merged[key]
                if width > m['width']:
                    m['width'] = width
                if fid:
                    m['froms'].add(fid)
                if tid:
                    m['tos'].add(tid)
            else:
                merged[key] = {'width': width, 'froms': {fid} if fid else set(),
                               'tos': {tid} if tid else set(), 'cid': cid}
                order.append(key)
        # ★ 折返清理 + 线头/断头删除（用户要求：不留"原路返回"的线头）
        def _clean_zig(pts):
            # 点数爆炸（避障残留死胡同）：直接重画横平竖直 L 形
            if len(pts) > 40:
                s, e = pts[0], pts[-1]
                if abs(s[0] - e[0]) < 0.5:
                    return [s, e]
                if abs(s[1] - e[1]) < 0.5:
                    return [s, e]
                if abs(s[1] - e[1]) > abs(s[0] - e[0]):
                    return [s, (s[0], e[1]), e]
                return [s, (e[0], s[1]), e]
            out = []
            for p in pts:
                if len(out) >= 2:
                    v1 = (out[-1][0] - out[-2][0], out[-1][1] - out[-2][1])
                    v2 = (p[0] - out[-1][0], p[1] - out[-1][1])
                    l1 = math.hypot(*v1)
                    l2 = math.hypot(*v2)
                    if l1 > 0.1 and l2 > 0.1 and (v1[0] * v2[0] + v1[1] * v2[1]) < -0.5 * l1 * l2:
                        out.pop()
                out.append(p)
            res = []
            for p in out:
                if not res or math.hypot(res[-1][0] - p[0], res[-1][1] - p[1]) > 0.05:
                    res.append(p)
            return res if len(res) >= 2 else None

        # 设备框绝对坐标（色框边）+ 母线横线（连母线线端点判定）
        dev_abs = {}
        for pid, (px, py) in self.pos.items():
            try:
                l, r, t, b = self._dev_box_edges(pid)
            except Exception:
                continue
            dev_abs[pid] = (px + l, py + t, px + r, py + b)
        cont_abs = [cb for cb in self.cont_box.values()]
        boxes_all = list(dev_abs.values()) + cont_abs
        bus_lines = []
        for key, m in merged.items():
            if m['cid'].startswith('BUS_'):
                pts = key[0]
                if len(pts) >= 2:
                    bus_lines.append((min(pts[0][0], pts[-1][0]), pts[0][1],
                                      max(pts[0][0], pts[-1][0]), pts[-1][1]))

        def _touches(px, py, box):
            x1, y1, x2, y2 = box
            tol = 4.0
            on = (abs(px - x1) <= tol or abs(px - x2) <= tol or abs(py - y1) <= tol or abs(py - y2) <= tol)
            return on and (x1 - tol <= px <= x2 + tol and y1 - tol <= py <= y2 + tol)

        def _on_bus(px, py):
            for bx1, by, bx2, _ in bus_lines:
                if abs(py - by) <= 3 and bx1 - 3 <= px <= bx2 + 3:
                    return True
            return False

        new_order = []
        for key in order:
            pts, color = key
            m = merged[key]
            pts2 = _clean_zig(pts)
            if pts2 is None:
                continue
            # ★ v12g：穿框绕行——逐段检测穿过设备/容器框的线段，确定性帽子绕行到空白带
            # （v12h 实测：绕行会破坏母线/干线 T 接路径产生悬空断头，回退为仅保留方法）
            # pts2 = self._detour_reroute(pts2, boxes_all) or pts2
            # ★ B-mini 修复：旧版 d<40 && len>2 直接整条删除太激进，把
            # 短距 L 形/3 点折线也一并清掉了。改为：只在 polyline 形成
            # 明显"折返"（中间点回退到起点附近）时才删除；其它短距 L 形
            # 保留（其端点已贴设备框/母线，下方 ok_s/ok_e 判定会兜底）。
            d = math.hypot(pts2[0][0] - pts2[-1][0], pts2[0][1] - pts2[-1][1])
            if d < 20 and len(pts2) > 4:
                # 折返型线头：起点/终点距离近且路径长 → 整条放弃
                continue
            # 断头：端点不贴任何设备框/母线 → 删除（用户要求不留）
            s, e = pts2[0], pts2[-1]
            ok_s = _on_bus(s[0], s[1]) or any(_touches(s[0], s[1], b2) for b2 in dev_abs.values())
            ok_e = _on_bus(e[0], e[1]) or any(_touches(e[0], e[1], b2) for b2 in dev_abs.values())
            if not (ok_s and ok_e):
                continue
            nkey = (tuple(pts2), color)
            if nkey != key:
                nm = merged.pop(key)
                merged[nkey] = nm
            new_order.append(nkey)
        order = new_order

        for key in order:
            pts, color = key
            m = merged[key]
            cg = ET.SubElement(g, f'{{{SVG_NS}}}g', {'id': m['cid']})
            pts_str = ' '.join(f'{x},{y}' for x, y in pts)
            ET.SubElement(cg, f'{{{SVG_NS}}}polyline', {
                'points': pts_str, 'fill': 'none', 'stroke': color,
                'stroke-width': str(m['width']),
                'stroke-linecap': 'round', 'stroke-linejoin': 'round',
            })
            if m['froms'] or m['tos']:
                md = ET.SubElement(cg, f'{{{SVG_NS}}}metadata')
                for fid in m['froms']:
                    ET.SubElement(md, f'{{{IEC_NS}}}Terminal', {'ObjectID': fid, 'side': 'from'})
                for tid in m['tos']:
                    ET.SubElement(md, f'{{{IEC_NS}}}Terminal', {'ObjectID': tid, 'side': 'to'})

        # ★ 后处理：多平行线偏移 + 网格轨道分配（Segment-based Parallel Routing）
        # 思路：把每条 polyline 拆成 H/V 段，按 (方向, 轴位置, 区间) 分组，
        #      同一行/列上有 ≥2 条段共享同一轨道时，自动分配垂直/水平偏移。
        # v11: 禁用平行偏移（网格状阶梯线来源），线保持原始正交折线
        # self._post_process_parallel_offset(g)

    # ─────────────────────────────────────────────────────────────────────────
    #  Segment-based Parallel Routing (网格化平行线偏移)
    # ─────────────────────────────────────────────────────────────────────────
    def _post_process_parallel_offset(self, g):
        """★ v3 - Segment-based Parallel Routing（按用户算法升级版）

        核心算法：
          1. 把每条 polyline 拆成 H/V 单段（axis-aligned segments）
          2. 把所有段按 (方向, 轴位置) 分桶：
             - H 段桶键 = ('H', round(Y))
             - V 段桶键 = ('V', round(X))
          3. 每桶内若 ≥2 条段的"区间"（H 看 X 范围，V 看 Y 范围）有重叠 → 视为平行轨道
          4. 对桶内所有线段按起点排序，分配 Offset_i = (i - (N-1)/2) × D
          5. 把每条 polyline 的对应段沿法向量施加偏移，并在段两端插入折弯段回到端点
          6. ★ 保护端点锚定：段的第一个/最后一个 polyline 点（连接设备的端点）不偏移

        ★ 与 v2 区别：v2 只看整条 polyline 的总 dy/dx，L 形线无法识别；
                     v3 拆成单段按"轴位置"分桶，任何线都能识别重叠。
        """
        if not getattr(self, '_wire_segs', None):
            return

        D = 14            # ★ 平行线间距（用户建议 8~15px，取 14）
        AXIS_TOL = 2      # ★ Y/X 容差（同组判定）
        ANCHOR_FRAC = 0.15  # ★ 端点锚定：每个段最靠近端点的前 ANCHOR_FRAC 比例不偏移
        MIN_LEN = 12.0    # ★ 短于这个长度的段不参与偏移（避免抖动）

        # 1. 收集每条 polyline → 拆成 H/V 单段列表
        # 每条记录：poly_idx, seg_idx (在本 polyline 中的索引), direction, axis_pos,
        #          range_min, range_max (H: X 范围; V: Y 范围),
        #          original_pts (整条 polyline 的点列表 - 用于重写), seg_start_pt, seg_end_pt
        polylines = []  # [(pts, color, width, cid, fid, tid), ...]
        all_segments = []  # [(poly_idx, seg_idx, direction, axis_pos, range_min, range_max, seg_pts), ...]

        for poly_idx, (pts, color, width, cid, fid, tid) in enumerate(self._wire_segs):
            if len(pts) < 2:
                continue
            polylines.append({
                'pts': list(pts), 'color': color, 'width': width, 'cid': cid,
                'fid': fid, 'tid': tid,
            })
            # 拆段：相邻两点 dx≈0 → V，dy≈0 → H
            for seg_idx in range(len(pts) - 1):
                p1, p2 = pts[seg_idx], pts[seg_idx + 1]
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                seg_len = math.hypot(dx, dy)
                if seg_len < MIN_LEN:
                    continue
                if abs(dx) < 0.5 and abs(dy) > MIN_LEN:
                    direction = 'V'
                    axis_pos = round(p1[0] / AXIS_TOL) * AXIS_TOL
                    range_min, range_max = (min(p1[1], p2[1]), max(p1[1], p2[1]))
                    all_segments.append({
                        'poly_idx': poly_idx, 'seg_idx': seg_idx,
                        'direction': direction, 'axis_pos': axis_pos,
                        'range_min': range_min, 'range_max': range_max,
                        'seg_pts': (p1, p2), 'seg_len': seg_len,
                    })
                elif abs(dy) < 0.5 and abs(dx) > MIN_LEN:
                    direction = 'H'
                    axis_pos = round(p1[1] / AXIS_TOL) * AXIS_TOL
                    range_min, range_max = (min(p1[0], p2[0]), max(p1[0], p2[0]))
                    all_segments.append({
                        'poly_idx': poly_idx, 'seg_idx': seg_idx,
                        'direction': direction, 'axis_pos': axis_pos,
                        'range_min': range_min, 'range_max': range_max,
                        'seg_pts': (p1, p2), 'seg_len': seg_len,
                    })
                # 对角线 / 短段：跳过

        if not all_segments:
            return

        # 2. 按 (direction, axis_pos) 分桶
        buckets = defaultdict(list)
        for seg in all_segments:
            key = (seg['direction'], seg['axis_pos'])
            buckets[key].append(seg)

        # 3. 每桶内找相互重叠的"簇"
        #    在桶内：两条段如果 range_min/range_max 重叠 → 视为同一轨道竞争组
        #    按重叠关系做并查集聚合，再排序分配偏移
        #    简化版：每桶内的所有段视为同一组，按起点排序后分配 track

        # 收集每条 polyline 的"段级偏移需求"
        # offset_per_seg[(poly_idx, seg_idx)] = offset_value
        offset_per_seg = {}

        group_count = 0
        for (direction, axis_pos), segs in buckets.items():
            # 在桶内做"重叠分组"（簇）：如果两条段区间重叠则同簇
            # 用贪心法：按 range_min 排序，遍历时若与上一簇 max 有重叠则归入同一簇
            segs_sorted = sorted(segs, key=lambda s: s['range_min'])
            clusters = []  # [[seg, ...], ...]
            for seg in segs_sorted:
                placed = False
                if clusters:
                    last_cluster = clusters[-1]
                    # 检查与上一簇最后一个元素的 range_max（已排序所以只看最后一个）
                    # 但要逐个检查簇内全部 → 简单做法：检查簇最大 range_max
                    cluster_max = max(s['range_max'] for s in last_cluster)
                    if seg['range_min'] <= cluster_max:
                        last_cluster.append(seg)
                        placed = True
                if not placed:
                    clusters.append([seg])

            # 每个簇内按起点分配偏移
            for cluster in clusters:
                if len(cluster) < 2:
                    continue
                # 按 range_min 排序（保持稳定序）
                cluster.sort(key=lambda s: (s['range_min'], s['seg_pts'][0][0], s['seg_pts'][0][1]))
                n = len(cluster)
                for i, seg in enumerate(cluster):
                    offset = (i - (n - 1) / 2) * D
                    key = (seg['poly_idx'], seg['seg_idx'])
                    # 若该段已记录过偏移（同段在多个桶）→ 取绝对值最大（更明显的偏移）
                    if key in offset_per_seg:
                        if abs(offset) > abs(offset_per_seg[key]):
                            offset_per_seg[key] = offset
                    else:
                        offset_per_seg[key] = offset
                group_count += 1

        if not offset_per_seg:
            return

        # 4. 应用偏移到每条 polyline
        # 关键：偏移仅施加在"中间部分"——段的端部 ANCHOR_FRAC 距离内保持原坐标
        #       这样设备的端口连接保持稳定不漂移
        for poly_idx, poly in enumerate(polylines):
            original_pts = poly['pts']
            new_pts = list(original_pts)
            direction_axis = {}  # seg_idx → direction

            # 计算每段的偏移（可能为 0）
            n_segs = len(original_pts) - 1
            for seg_idx in range(n_segs):
                key = (poly_idx, seg_idx)
                if key not in offset_per_seg:
                    continue
                offset = offset_per_seg[key]
                if offset == 0:
                    continue

                p1, p2 = original_pts[seg_idx], original_pts[seg_idx + 1]
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                seg_len = math.hypot(dx, dy)
                if seg_len < MIN_LEN:
                    continue
                is_horiz = abs(dy) < 0.5

                # 端点锚定：跳过 ANCHOR_FRAC 长度的两端
                anchor_len = seg_len * ANCHOR_FRAC

                if is_horiz:
                    # H 段：偏移作用于 Y
                    anchor_x_start = p1[0] + (1 if dx > 0 else -1) * anchor_len
                    anchor_x_end = p2[0] - (1 if dx > 0 else -1) * anchor_len
                    # 重写 p1 和 p2（锚定后）：插入锚定点
                    new_p1 = (p1[0], p1[1])
                    new_anchor_start = (anchor_x_start, p1[1] + offset)
                    new_anchor_end = (anchor_x_end, p1[1] + offset)
                    new_p2 = (p2[0], p2[1])
                    # 替换 new_pts[seg_idx] 和 new_pts[seg_idx+1]
                    # ★ 重建：从 seg_idx 之后的所有点都要插入
                    # 先收集前后两段：
                    pre = new_pts[:seg_idx]  # [.., p1]
                    post = new_pts[seg_idx + 2:]  # [p2, ..]
                    new_seg = [new_p1, new_anchor_start, new_anchor_end, new_p2]
                    new_pts = pre + new_seg + post
                    # 后续索引需要更新（+3 个插入点）：但下面我们只用 seg_idx 一遍
                    # ★ 重要：如果多段都有偏移，我们按 seg_idx 倒序处理以避免索引混乱
                    #     为简化，下面先全部用 seg_idx 处理，最后做整体重建

                else:
                    # V 段：偏移作用于 X
                    anchor_y_start = p1[1] + (1 if dy > 0 else -1) * anchor_len
                    anchor_y_end = p2[1] - (1 if dy > 0 else -1) * anchor_len
                    new_p1 = (p1[0], p1[1])
                    new_anchor_start = (p1[0] + offset, anchor_y_start)
                    new_anchor_end = (p1[0] + offset, anchor_y_end)
                    new_p2 = (p2[0], p2[1])
                    pre = new_pts[:seg_idx]
                    post = new_pts[seg_idx + 2:]
                    new_seg = [new_p1, new_anchor_start, new_anchor_end, new_p2]
                    new_pts = pre + new_seg + post

            # 简化实现：上面这种"按 seg_idx 直接改 new_pts"在多段偏移时会索引混乱
            # 改为：先收集所有段改写方案，最后做一次性重建
            # ★ 重新做一遍：
            new_pts = self._rebuild_with_offsets(original_pts, poly_idx, offset_per_seg,
                                                  anchor_frac=ANCHOR_FRAC, min_len=MIN_LEN)
            # 合并相邻共线段（去除多余拐点）
            merged = self._collinear_merge([new_pts])
            if merged:
                new_pts = merged[0]
            else:
                new_pts = list(original_pts)
            poly['new_pts'] = new_pts

        # 5. 把更新写回 SVG
        cids_to_update = {}
        for poly_idx, poly in enumerate(polylines):
            if 'new_pts' in poly:
                cids_to_update.setdefault(poly['cid'], []).append(poly['new_pts'])

        # 由于 wire_segs 中可能多条 polyline 共享同一 cid，需要分别更新
        # 但 SVG 渲染阶段已经按 cid 合成了一个 polyline。这里我们的 cid 是 'WIRE_NNNNNN' 唯一，
        # 所以一对一更新即可
        offset_count = 0
        for poly in polylines:
            if 'new_pts' not in poly:
                continue
            cid = poly['cid']
            new_pts = poly['new_pts']
            # 找对应 g
            target_g = None
            for child in g:
                if child.get('id') == cid:
                    target_g = child
                    break
            if target_g is None:
                continue
            # 找 polyline 子元素
            for child in target_g:
                if child.tag.endswith('}polyline'):
                    child.set('points', ' '.join(f'{x:.2f},{y:.2f}' for x, y in new_pts))
                    offset_count += 1
                    break

        if offset_count:
            print(f"  [网格轨道偏移 v3] 簇 {group_count} | 更新线 {offset_count}")

    def _rebuild_with_offsets(self, pts, poly_idx, offset_per_seg,
                              anchor_frac=0.15, min_len=12.0):
        """★ 一次性重建 polyline 点序列，应用所有段的偏移

        处理逻辑：
          - 顺序遍历原 pts（保留端点不变）
          - 对每段 (seg_idx) 如果有偏移 → 段内 4 个点：起点锚定 + 2 个偏移拐点 + 终点锚定
          - 否则保持原 2 个端点
        """
        if len(pts) < 2:
            return list(pts)
        new_pts = [pts[0]]  # 起点不动

        for seg_idx in range(len(pts) - 1):
            p1, p2 = pts[seg_idx], pts[seg_idx + 1]
            key = (poly_idx, seg_idx)
            offset = offset_per_seg.get(key, 0.0)
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            seg_len = math.hypot(dx, dy)
            is_horiz = abs(dy) < 0.5

            if offset == 0 or seg_len < min_len:
                # 不偏移：直接添加终点
                new_pts.append(p2)
                continue

            # 端点锚定：段两端各 ANCHOR_FRAC 不偏移
            anchor_len = seg_len * anchor_frac

            if is_horiz:
                sign = 1 if dx > 0 else -1
                anchor_x_start = p1[0] + sign * anchor_len
                anchor_x_end = p2[0] - sign * anchor_len
                # 正交阶梯：原线 → 垂直抬升 → 水平偏移 → 垂直回落 → 原线（全程横平竖直）
                new_pts.extend([
                    (anchor_x_start, p1[1]),
                    (anchor_x_start, p1[1] + offset),
                    (anchor_x_end, p1[1] + offset),
                    (anchor_x_end, p2[1]),
                    p2,
                ])
            else:
                sign = 1 if dy > 0 else -1
                anchor_y_start = p1[1] + sign * anchor_len
                anchor_y_end = p2[1] - sign * anchor_len
                # 正交阶梯：原线 → 水平平移 → 垂直偏移 → 水平回落 → 原线（全程横平竖直）
                new_pts.extend([
                    (p1[0], anchor_y_start),
                    (p1[0] + offset, anchor_y_start),
                    (p1[0] + offset, anchor_y_end),
                    (p2[0], anchor_y_end),
                    p2,
                ])

        return new_pts

    def _draw_devices(self, g):
        # 设备符号：白色背景与符号放在同一个 <g> 内，避免被解析器当作独立设备图元
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d:
                continue
            if not self.is_real_device(d['type']):
                continue  # 非真实设备（dxd线/未知type/背景）不绘制、不输出metadata
            dg = ET.SubElement(g, f'{{{SVG_NS}}}g', {
                'transform': f'translate({x},{y})',
            })
            # 设备 metadata（ObjectName/PSRType 属性名对齐 IEC 规范）
            self._add_device_metadata(dg, pid)
            if d['type'] in BUSBAR_TYPES:
                # 母线视觉由 BUS_ 母线连线承担，仅输出 metadata 节点（图模一致）
                continue
            # 非母线设备：透明背景，符号独立渲染
            # 保留原始SVG背景色，禁止强制覆盖为纯白
            left, right, top, bottom = self._dev_sym_edges(pid)
            # 类别色：名称优先，type 兜底
            dev_fill = DEV_CATEGORY_FALLBACK
            disp_name = self._display_name(d)
            if disp_name:
                for kws, col in DEV_CATEGORY_BY_NAME:
                    if any(k in disp_name for k in kws):
                        dev_fill = col
                        break
            if dev_fill == DEV_CATEGORY_FALLBACK:
                dev_fill = DEV_CATEGORY_FILL.get(d['type'], DEV_CATEGORY_FALLBACK)
            # 强制最小框尺寸：所有设备（含接线点）至少 48x40（用户要求"所有框都要大框"）
            DEV_MIN_W, DEV_MIN_H = 48.0, 40.0
            cur_w = right - left
            cur_h = bottom - top
            if cur_w < DEV_MIN_W:
                grow = (DEV_MIN_W - cur_w) / 2.0
                left -= grow
                right += grow
            if cur_h < DEV_MIN_H:
                grow = (DEV_MIN_H - cur_h) / 2.0
                top -= grow
                bottom += grow
            # 大框：符号 + 上下文字区域（标注可能避让到上方或下方；左右允许文字一半在外）
            pad_x = 10.0
            pad_top = 16.0
            pad_bottom = 20.0
            ET.SubElement(dg, f'{{{SVG_NS}}}rect', {
                'x': f'{left - pad_x:.1f}', 'y': f'{top - pad_top:.1f}',
                'width': f'{right - left + 2 * pad_x:.1f}',
                'height': f'{bottom - top + pad_top + pad_bottom:.1f}',
                'fill': dev_fill, 'fill-opacity': '0.6',
                'stroke': dev_fill, 'stroke-opacity': '0.9', 'stroke-width': '1',  # 半透明+细边 类别色实色（不与容器灰底叠加）
                'rx': '2',
            })
            if d.get('symbol'):
                sym = d['symbol'].lstrip('#')
                info = self.sym_box.get(sym)
                if info:
                    tr = f"scale({info['scale']:.4f}) translate({-info['cx']:.4f},{-info['cy']:.4f})"
                else:
                    tr = f'scale({SYM_SCALE}) translate(-4,-1.5)'
                ET.SubElement(dg, f'{{{SVG_NS}}}use', {
                    f'{{{XLINK_NS}}}href': d['symbol'], 'transform': tr,
                })
            else:
                # 无符号设备：通用占位符号（圆点）+ 框内文字（避免只有空色框）
                ET.SubElement(dg, f'{{{SVG_NS}}}circle', {
                    'cx': '0', 'cy': '0', 'r': '3.5', 'fill': C_TEXT, 'stroke': 'none',
                })
                disp = self._display_name(d)
                if disp:
                    t = ET.SubElement(dg, f'{{{SVG_NS}}}text', {
                        'x': '0', 'y': '26', 'text-anchor': 'middle',
                        'font-size': str(F_BRANCH), 'fill': C_TEXT,
                    })
                    t.text = disp
                d['label_in_box'] = True

    def _draw_labels(self, g):
        seen_names = set()
        # 收集所有设备符号包围盒，用于标注碰撞检测
        dev_bboxes = []
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d:
                continue
            left, right, top, bottom = self._dev_sym_edges(pid)
            dev_bboxes.append((x + left, y + top, x + right, y + bottom))
        # 加入柜箱标题栏作为障碍物，避免标注压标题栏
        for (cx1, cy1, cx2, cy2) in self.cont_box.values():
            dev_bboxes.append((cx1, cy1, cx2, cy1 + 20))

        def _bbox_overlap(a, b, pad=6):
            return not (a[2] + pad < b[0] or b[2] + pad < a[0] or
                        a[3] + pad < b[1] or b[3] + pad < a[1])

        placed_labels = []

        # 母线标注（母线在顶部，冲突少，直接放上方）
        for pid, d in self.devices.items():
            if d['type'] not in BUSBAR_TYPES or pid not in self.pos:
                continue
            name = self._display_name(d)
            if name in seen_names:
                continue
            seen_names.add(name)
            x, y = self.pos[pid]
            ly = y - DEV_HH - 6
            disp = name
            tw = max(len(disp) * F_BRANCH * 1.1, 20)
            placed_labels.append((x - tw / 2, ly - F_BRANCH + 2, x + tw / 2, ly + 2))
            t = ET.SubElement(g, f'{{{SVG_NS}}}text', {
                'x': str(x), 'y': str(ly),
                'text-anchor': 'middle', 'font-size': str(F_BRANCH), 'fill': C_TEXT,
            })
            t.text = disp

        # 设备标注（带碰撞避让：上方 -> 下方 -> 左侧 -> 右侧）
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            if not self.is_real_device(d['type']):
                continue  # 非真实设备（dxd线/未知type）不标注
            # Junction 节点也标注文字（用户要求每个元件都有文字）
            if d.get('label_in_box'):
                continue  # 无符号设备文字已画在框内
            name = self._display_name(d)
            if not name:
                continue
            seen_names.add(name)
            if d.get('label_in_box'):
                continue  # 无符号设备文字已画在框内
            is_key = d['type'] in KEY_DEV_TYPES
            font_size = F_KEY if is_key else F_BRANCH
            weight = 'bold' if is_key else 'normal'
            disp = name
            tw = max(len(disp) * font_size * 1.1, 20)

            def _mk_bbox(cx, cy):
                return (cx - tw / 2, cy - font_size + 2, cx + tw / 2, cy + 2)

            def _conflict(bbox):
                for db in dev_bboxes:
                    if _bbox_overlap(bbox, db, pad=2):
                        return True
                for lb in placed_labels:
                    if _bbox_overlap(bbox, lb, pad=2):
                        return True
                return False

            # 候选位置：上方、下方、左侧、右侧、左上、右上、左下、右下
            candidates = [
                (x, y - DEV_HH - 6),
                (x, y + DEV_HH + 6 + font_size),
                (x - tw / 2 - 30, y),
                (x + tw / 2 + 30, y),
                (x - tw / 2 - 20, y - DEV_HH - 6),
                (x + tw / 2 + 20, y - DEV_HH - 6),
                (x - tw / 2 - 20, y + DEV_HH + 6 + font_size),
                (x + tw / 2 + 20, y + DEV_HH + 6 + font_size),
            ]
            lx, ly = candidates[0]
            best_overlap = float('inf')
            for cx, cy in candidates:
                bb = _mk_bbox(cx, cy)
                if not _conflict(bb):
                    lx, ly = cx, cy
                    break
                # 计算重叠面积，记录最小的
                ov = 0
                for db in dev_bboxes:
                    ox = min(bb[2], db[2]) - max(bb[0], db[0])
                    oy = min(bb[3], db[3]) - max(bb[1], db[1])
                    if ox > 0 and oy > 0:
                        ov += ox * oy
                for lb in placed_labels:
                    ox = min(bb[2], lb[2]) - max(bb[0], lb[0])
                    oy = min(bb[3], lb[3]) - max(bb[1], lb[1])
                    if ox > 0 and oy > 0:
                        ov += ox * oy
                if ov < best_overlap:
                    best_overlap = ov
                    lx, ly = cx, cy
            # 如果所有候选都冲突，用重叠最小的（上面已记录）

            placed_labels.append(_mk_bbox(lx, ly))

            lg = ET.SubElement(g, f'{{{SVG_NS}}}g')
            md = ET.SubElement(lg, f'{{{SVG_NS}}}metadata')
            ET.SubElement(md, f'{{{IEC_NS}}}PSR_Ref', {'ObjectID': f'TXT_{pid}'})
            t = ET.SubElement(lg, f'{{{SVG_NS}}}text', {
                'x': str(lx), 'y': str(ly), 'text-anchor': 'middle',
                'font-size': str(font_size), 'fill': C_TEXT, 'font-weight': weight,
                
            })
            t.text = disp

    def _dev_sym_edges(self, pid):
        """返回设备符号的左右上下边缘（相对于中心坐标），用于导线端点定位。

        ★ 核心原则：
          - 导线必须从符号**外侧**接入，不能从符号**内部**穿出
          - 用 terminal-index 的真实端点，BB 只作为补充/边界参考
          - 水平连接用左右端点，垂直连接用上下端点
          - 关键：对于 SurgeArrester 等只有单侧端点的设备，
            另一侧必须用足够远的 BB 值（线从设备外侧绕过来接入）

        返回 (left_x, right_x, top_y, bottom_y)
        """
        d = self.devices.get(pid, {})
        sym = (d.get('symbol') or '').lstrip('#')
        info = self.sym_box.get(sym)

        if info is None:
            return -14.0, 14.0, -10.0, 10.0

        term_map = info.get('terminals', {})

        # BB 基础值
        bb_l = max(info.get('left', -14.0), -30.0)
        bb_r = min(info.get('right', 14.0), 30.0)
        bb_t = max(info.get('top', -10.0), -30.0)
        bb_b = min(info.get('bottom', 10.0), 30.0)

        if not term_map:
            # 无 terminal：直接用 BB
            return bb_l, bb_r, bb_t, bb_b

        # 分离出水平（y≈0）和垂直（x≈0）的端点
        horiz = [(tx, ty) for tx, ty in term_map.values() if abs(ty) <= 2.0]
        vert = [(tx, ty) for tx, ty in term_map.values() if abs(tx) <= 2.0]

        # 水平端点
        hx_vals = sorted(set(tx for tx, ty in horiz)) if horiz else []
        # 垂直端点
        vy_vals = sorted(set(ty for tx, ty in vert)) if vert else []

        # 左右端点：取最左和最右的水平端点
        # 如果没有水平端点，用 BB
        if hx_vals:
            term_l = hx_vals[0]   # 最左
            term_r = hx_vals[-1]  # 最右
        else:
            term_l = bb_l
            term_r = bb_r

        # 上下端点：取最上和最下的垂直端点
        if vy_vals:
            term_t = vy_vals[0]   # 最上（y 最小）
            term_b = vy_vals[-1]  # 最下（y 最大）
        else:
            term_t = bb_t
            term_b = bb_b

        return term_l, term_r, term_t, term_b

    def _dev_sym_left_right(self, pid):
        """返回设备的左右端点（相对于中心）。"""
        l, r, _, _ = self._dev_sym_edges(pid)
        return l, r

    def _dev_sym_top_bottom(self, pid):
        """返回设备的上下端点（相对于中心）。"""
        _, _, t, b = self._dev_sym_edges(pid)
        return t, b

    def _port_offset(self, pid, side):
        """根据分配的 side 返回端点偏移（相对于设备中心）。
        side: 'L'/'R'/'T'/'B'
        返回 (dx, dy) — ★ 使用色框边，不是符号边
        """
        l, r, t, b = self._dev_box_edges(pid)
        if side == 'L':
            return (l, 0.0)
        elif side == 'R':
            return (r, 0.0)
        elif side == 'T':
            return (0.0, t)
        elif side == 'B':
            return (0.0, b)
        return (0.0, 0.0)

    def _dev_box_edges(self, pid):
        """返回设备色框的 4 边坐标（相对于设备中心）。

        推导自 _draw_devices rect 渲染逻辑：
          rect.x = left_ext - pad_x
          rect.y = top_ext - pad_top
          rect.w = (right_ext - left_ext) + 2*pad_x
          rect.h = (bottom_ext - top_ext) + pad_top + pad_bottom

        其中 left_ext/right_ext/top_ext/bottom_ext 是经 DEV_MIN_W/H 扩展后的"扩展边界"。
        注意：当 cur_w >= DEV_MIN_W 时，扩展边界 = 符号原始边界。
              当 cur_w < DEV_MIN_W 时，扩展边界 = 符号原始边界 + 扩展量。

        设 left_sym/right_sym 为符号原始边界（来自 sym_box）。
        设 extend_w = max(cur_w, DEV_MIN_W) = max(right_sym - left_sym, DEV_MIN_W)
        则 left_ext = left_sym - (extend_w - (right_sym - left_sym)) / 2
              right_ext = right_sym + (extend_w - (right_sym - left_sym)) / 2
        化简：left_ext = (left_sym + right_sym) / 2 - extend_w / 2
              right_ext = (left_sym + right_sym) / 2 + extend_w / 2

        box_l = left_ext - pad_x
        box_r = right_ext + pad_x   （但如果 left_ext = left_sym, 则 box_l = left_sym - pad_x）
        当 cur_w >= DEV_MIN_W 时，left_ext = left_sym，所以 box_l = left_sym - pad_x = 24 - 10 = 14
        → 错误！所以当 cur_w >= DEV_MIN_W 时不应减 pad_x。

        修正：
        - box_l = left_ext - pad_x（始终）
        - box_r = right_ext（当 right_ext = right_sym 时，不加 pad_x）

        结论：box_l = left_ext - pad_x, box_r = right_ext（★）
        """
        d = self.devices.get(pid, {})
        sym = (d.get('symbol') or '').lstrip('#')
        info = self.sym_box.get(sym)
        if info is None:
            return -34.0, 34.0, -36.0, 40.0

        # ★ v12f 修复：统一为 _draw_devices 的渲染口径。
        #   旧实现基于符号 BB(left_sym=-14) 扩展 → box_l=-34，而 _draw_devices
        #   实际渲染 rect 基于 _dev_sym_edges（terminal 端点口径，如单侧端子
        #   设备的 SurgeArrester left=right=13.92）扩展 → rect.x=-20.1，
        #   端口落点与渲染框边相差 14px，导致"线头悬在框外"。
        #   现在 box 边 = 渲染 rect 边，端口与色框精确对齐。
        l, r, t, b = self._dev_sym_edges(pid)
        DEV_MIN_W, DEV_MIN_H = 48.0, 40.0
        pad_x = 10.0
        pad_top = 16.0
        pad_bottom = 20.0

        cur_w = r - l
        cur_h = b - t
        if cur_w < DEV_MIN_W:
            grow = (DEV_MIN_W - cur_w) / 2.0
            l -= grow
            r += grow
        if cur_h < DEV_MIN_H:
            grow = (DEV_MIN_H - cur_h) / 2.0
            t -= grow
            b += grow

        box_l = l - pad_x
        box_r = r + pad_x
        box_t = t - pad_top
        box_b = b + pad_bottom
        return box_l, box_r, box_t, box_b

    def _get_port_side(self, src, dst, default=None):
        """获取 src→dst 的端口 side（如果没分配则按方向启发式选一个）"""
        if hasattr(self, 'port_assign') and (src, dst) in self.port_assign:
            return self.port_assign[(src, dst)]
        # 兜底：现场分配"未使用"的端点（保证一个端点只伸出一条线）
        if src not in self.pos or dst not in self.pos:
            return default
        if not hasattr(self, '_port_used_fb'):
            self._port_used_fb = defaultdict(set)
        used = self._port_used_fb[src]
        side = self._pick_port_side(src, dst, used)
        if side:
            used.add(side)
            return side
        sx, sy = self.pos[src]
        dx, dy = self.pos[dst]
        ddx, ddy = dx - sx, dy - sy
        if abs(ddx) >= abs(ddy):
            return 'R' if ddx >= 0 else 'L'
        return 'B' if ddy >= 0 else 'T'

    # ═══════════════════════════════════════════════════════════
    #  【新增】容器进出线辅助方法（Step 1：底部引出）
    # ═══════════════════════════════════════════════════════════
    def _device_in_container(self, pid: str) -> bool:
        """判断设备是否在容器内（用于底部出线逻辑）"""
        for cid, c in self.containers.items():
            if pid in c.get('members', []):
                return True
        return False

    def _get_container_id_of(self, pid: str) -> Optional[str]:
        """获取设备所在容器ID（无则None）"""
        for cid, c in self.containers.items():
            if pid in c.get('members', []):
                return cid
        return None

    def _container_bottom_y(self, cid: str) -> float:
        """获取容器底边y坐标（用于从底部引出）"""
        if cid not in self.cont_box:
            return 0.0
        return self.cont_box[cid][3]

    def _split_bus_seg(self, x1, y, x2):
        """母线横线挖掉穿过的容器框区间（母线本体不进入容器；容器内连接走底部引出）。
        端点落容器框内 → 截到框边缘。返回 [(sx1,sx2), ...] 不穿任何容器框的水平段。

        ★ A4 修复：原版本判定条件 cy1 + 2 < y < cy2 - 2 过于严格（仅 ±2 px 容差），
        实际布局中母线 y 与容器 y 几乎不可能完全相等，导致判定永远不触发、
        母线横穿整个容器顶部。改为按容器整体 y 区间与母线 y 的关系判定。
        """
        if x1 > x2:
            x1, x2 = x2, x1
        # 端点落容器框内 → 截到框边缘（保留原逻辑）
        for cid, (cx1, cy1, cx2, cy2) in self.cont_box.items():
            if not (cy1 + 2 < y < cy2 - 2):
                continue
            if cx1 < x1 < cx2:
                x1 = cx1
            if cx1 < x2 < cx2:
                x2 = cx2
        if x2 - x1 < 0.5:
            return []
        segs = [(x1, x2)]
        # ★ A4 修复：母线 y 落在容器 y 区间内（含 ±CONT_TOP 容差），即视为
        # 母线横线会穿过该容器；按容器 x 范围把母线段切断。
        # 旧版 ±2 px 容差导致 99% 容器不触发。
        CONT_TOP_TOL = 12.0  # 与布局时给容器留的顶部余量对齐
        for cid, (cx1, cy1, cx2, cy2) in self.cont_box.items():
            # 母线 y 与容器 y 区间相交（含顶部留白容差）→ 视为穿过
            if not (cy1 - CONT_TOP_TOL < y < cy2 + 2):
                continue
            if cx2 <= x1 or cx1 >= x2:
                continue
            new = []
            for a, b in segs:
                if b <= cx1 + 2 or a >= cx2 - 2:
                    new.append((a, b))
                elif a < cx1 + 2 and b > cx2 - 2:
                    new.append((a, cx1 + 2))
                    new.append((cx2 - 2, b))
                elif a < cx1 + 2:
                    new.append((a, cx1 + 2))
                else:
                    new.append((cx2 - 2, b))
            segs = new
        return [s for s in segs if s[1] - s[0] >= 0.5]

    def _build_bus_segments(self):
        """预计算所有母线横线挖框后的段列表（供 T 接点定位与母线绘制复用）"""
        if getattr(self, '_bus_segs_built', False):
            return
        self._bus_segs = {}
        for pid, d in self.devices.items():
            if d['type'] not in BUSBAR_TYPES or pid not in self.pos:
                continue
            conn = [p for p in self.adj.get(pid, ()) if p in self.pos]
            if not conn:
                continue
            conn_sorted = sorted(conn, key=lambda p: self.pos[p][0])
            y = self.pos[pid][1]
            a_id, b_id = conn_sorted[0], conn_sorted[-1]
            a_left, a_right, _, _ = self._dev_box_edges(a_id)
            b_left, b_right, _, _ = self._dev_box_edges(b_id)
            xs = self.pos[a_id][0] + a_left
            xe = self.pos[b_id][0] + b_right
            if abs(xs - xe) < 0.5:
                continue
            self._bus_segs[(pid, round(y))] = self._split_bus_seg(xs, y, xe)
        self._bus_segs_built = True

    def _bus_tap_on_seg(self, bus_id, bus_y, tap_x):
        """把 T 接点移到母线保留段上（挖框后无横线的区域不受支持）"""
        self._build_bus_segments()
        segs_bus = self._bus_segs.get((bus_id, round(bus_y)))
        if not segs_bus:
            return tap_x
        for (a, b) in segs_bus:
            if a + 2 <= tap_x <= b - 2:
                return tap_x
        best, best_d = None, 1e18
        for (a, b) in segs_bus:
            d1, d2 = abs(tap_x - a), abs(tap_x - b)
            if d1 < best_d:
                best_d, best = d1, a
            if d2 < best_d:
                best_d, best = d2, b
        return best if best is not None else tap_x

    # ═══════════════════════════════════════════════════════════
    #  【新增】压站穿站检测（Step 2）
    # ═══════════════════════════════════════════════════════════
    def _line_crosses_container(self, x1, y1, x2, y2, exclude_cids=None) -> list:
        """检测线段穿过的容器ID列表（端点所在容器自动排除）"""
        if exclude_cids is None:
            exclude_cids = set()
        crossed = []
        for cid, (cx1, cy1, cx2, cy2) in self.cont_box.items():
            if cid in exclude_cids:
                continue
            # 扩展边界：线宽 + 余量
            margin = W_TRUNK / 2 + 5
            ex1, ey1, ex2, ey2 = cx1 - margin, cy1 - margin, cx2 + margin, cy2 + margin
            if self._segment_intersects_rect(x1, y1, x2, y2, ex1, ey1, ex2, ey2):
                crossed.append(cid)
        return crossed

    @staticmethod
    def _segment_intersects_rect(x1, y1, x2, y2, rx1, ry1, rx2, ry2) -> bool:
        """线段与矩形相交检测（包围盒排除法）"""
        # 包围盒快速排除
        if max(x1, x2) < rx1 or min(x1, x2) > rx2:
            return False
        if max(y1, y2) < ry1 or min(y1, y2) > ry2:
            return False
        # 线段在矩形一侧
        if (x1 < rx1 and x2 < rx1) or (x1 > rx2 and x2 > rx2):
            return False
        if (y1 < ry1 and y2 < ry1) or (y1 > ry2 and y2 > ry2):
            return False
        # 完整在内部
        if rx1 <= x1 <= rx2 and ry1 <= y1 <= ry2 and rx1 <= x2 <= rx2 and ry1 <= y2 <= ry2:
            return False
        return True

    def _device_boxes_abs(self):
        """设备绝对色框（大框：符号 + pad），母线无框（用线表达）"""
        if getattr(self, '_abs_dev_boxes_cache', None) is not None:
            return self._abs_dev_boxes_cache
        boxes = {}
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d or not self.is_real_device(d['type']):
                continue
            if d['type'] in BUSBAR_TYPES:
                continue
            l, r, t, b = self._dev_box_edges(pid)
            boxes[pid] = (x + l - 10.0, y + t - 16.0, x + r + 10.0, y + b + 20.0)
        self._abs_dev_boxes_cache = boxes
        return boxes

    def _avoid_devices(self, points, par, child):
        """设备级正交避障：段穿过非端点设备色框 → 就近绕行（H 段上下绕、V 段左右绕）"""
        boxes = self._device_boxes_abs()
        excl = {par, child}
        if len(points) < 2:
            return points
        pts = list(points)
        for _ in range(8):
            new_pts = [pts[0]]
            changed = False
            for i in range(len(pts) - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]
                hit = None
                for pid, (bx1, by1, bx2, by2) in boxes.items():
                    if pid in excl:
                        continue
                    # 端点在盒边上（贴边接入不算穿）
                    if abs(x1 - x2) < 0.5:
                        # V 段：x 在盒内、y 段与盒相交
                        if not (bx1 - 0.5 <= x1 <= bx2 + 0.5):
                            continue
                        if max(y1, y2) < by1 or min(y1, y2) > by2:
                            continue
                        hit = (pid, bx1, by1, bx2, by2)
                        break
                    elif abs(y1 - y2) < 0.5:
                        # H 段
                        if not (by1 - 0.5 <= y1 <= by2 + 0.5):
                            continue
                        if max(x1, x2) < bx1 or min(x1, x2) > bx2:
                            continue
                        hit = (pid, bx1, by1, bx2, by2)
                        break
                    else:
                        # 斜段：线段矩形相交
                        if (max(x1, x2) >= bx1 and min(x1, x2) <= bx2
                                and max(y1, y2) >= by1 and min(y1, y2) <= by2):
                            hit = (pid, bx1, by1, bx2, by2)
                            break
                if hit is None:
                    new_pts.append((x2, y2))
                    continue
                changed = True
                pid, bx1, by1, bx2, by2 = hit
                margin = 12.0
                if abs(y1 - y2) < 0.5:
                    # H 段：从上方或下方绕（选近侧），插入两个直角点
                    if y1 < (by1 + by2) / 2:
                        by = by1 - margin
                    else:
                        by = by2 + margin
                    new_pts.append((x1, by))
                    new_pts.append((x2, by))
                else:
                    # V 段：从左侧或右侧绕
                    if x1 < (bx1 + bx2) / 2:
                        bx = bx1 - margin
                    else:
                        bx = bx2 + margin
                    new_pts.append((bx, y1))
                    new_pts.append((bx, y2))
                new_pts.append((x2, y2))
            pts = new_pts
            if not changed:
                break
        return pts

    def _adjust_path_to_avoid_containers(self, points, par, child) -> list:
        """调整路径以避开容器（绕行）：从容器顶部上方绕过
        迭代确保不穿过任何容器"""
        if len(points) < 2:
            return points
        # 排除端点所在容器
        exclude_cids = set()
        if self._device_in_container(par):
            exclude_cids.add(self._get_container_id_of(par))
        if self._device_in_container(child):
            exclude_cids.add(self._get_container_id_of(child))

        all_pts = list(points)
        for _ in range(10):
            new_pts = [all_pts[0]]
            changed = False
            for i in range(len(all_pts) - 1):
                x1, y1 = all_pts[i]
                x2, y2 = all_pts[i + 1]
                crossed_cids = self._line_crosses_container(x1, y1, x2, y2, exclude_cids)
                if not crossed_cids:
                    # 不穿容器：直接添加端点
                    new_pts.append((x2, y2))
                    continue
                # 穿过容器：生成绕行路径
                changed = True
                margin = 12
                all_left = min(self.cont_box[c][0] for c in crossed_cids if c in self.cont_box)
                all_right = max(self.cont_box[c][2] for c in crossed_cids if c in self.cont_box)
                all_top = min(self.cont_box[c][1] for c in crossed_cids if c in self.cont_box)
                all_bot = max(self.cont_box[c][3] for c in crossed_cids if c in self.cont_box)

                if abs(y1 - y2) < GRID * 2:
                    # 近似水平：从顶部绕
                    bypass_y = all_top - margin
                    new_pts.append((x1, bypass_y))
                    new_pts.append((x2, bypass_y))
                elif abs(x1 - x2) < GRID * 2:
                    # 近似垂直：从侧面绕
                    if x1 < all_left:
                        bypass_x = all_left - margin
                    elif x1 > all_right:
                        bypass_x = all_right + margin
                    else:
                        bypass_x = all_left - margin if abs(x1 - all_left) < abs(x1 - all_right) else all_right + margin
                    new_pts.append((bypass_x, y1))
                    new_pts.append((bypass_x, y2))
                else:
                    # 斜线：先水平再垂直的两段折线绕行
                    if abs(x1 - x2) > abs(y1 - y2):
                        # 水平距离大：先水平绕
                        mid_x = all_left - margin if x1 < (all_left + all_right) / 2 else all_right + margin
                        bypass_y = all_top - margin
                        new_pts.append((mid_x, y1))
                        new_pts.append((mid_x, bypass_y))
                        new_pts.append((x2, bypass_y))
                    else:
                        # 垂直距离大：先垂直绕
                        mid_y = all_top - margin if y1 > (all_top + all_bot) / 2 else all_bot + margin
                        mid_x = all_left - margin if x1 < (all_left + all_right) / 2 else all_right + margin
                        new_pts.append((x1, mid_y))
                        new_pts.append((mid_x, mid_y))
                        new_pts.append((mid_x, y2))
                # 始终添加端点
                new_pts.append((x2, y2))
            all_pts = new_pts
            if not changed:
                break
        return all_pts

    def _split_line_avoiding_containers(self, points) -> list:
        """将穿过容器的水平长线段切分为多段，绕过容器
        母线专用：返回 List[(x,y)] 一条多段路径点列表
        策略：从所有被穿过的容器的最高顶上方绕行；迭代确保不穿过任何容器"""
        if len(points) < 2:
            return points

        all_pts = list(points)

        # 【新增】迭代绕行，直到不穿过任何容器（最多10次迭代防死循环）
        for _ in range(10):
            new_pts = [all_pts[0]]
            changed = False
            for i in range(len(all_pts) - 1):
                x1, y1 = all_pts[i]
                x2, y2 = all_pts[i + 1]
                crossed = self._line_crosses_container(x1, y1, x2, y2, set())
                if not crossed:
                    new_pts.append((x2, y2))
                    continue
                changed = True
                # 按x排序容器并合并重叠的
                margin = 12
                cxs = []
                for cid in crossed:
                    if cid in self.cont_box:
                        cx1, cy1, cx2, cy2 = self.cont_box[cid]
                        cxs.append((cx1, cx2, cy1, cy2))
                cxs.sort()
                # 合并重叠的容器为连续区间
                merged = []
                for c_l, c_r, c_t, c_b in cxs:
                    if merged and c_l <= merged[-1][1] + 2:
                        last = merged[-1]
                        merged[-1] = (last[0], max(last[1], c_r), min(last[2], c_t), max(last[3], c_b))
                    else:
                        merged.append((c_l, c_r, c_t, c_b))
                # bypass_y 用 min_top - margin（所有被穿过容器的最高顶）
                min_top = min(m[2] for m in merged)
                bypass_y = min_top - margin

                # 先把起点到第一个容器左边
                first_l = merged[0][0]
                if x1 < first_l - margin:
                    new_pts.append((first_l - margin, y1))
                # 绕过每个合并后的容器区间
                for m_l, m_r, m_t, m_b in merged:
                    new_pts.append((m_l - margin, bypass_y))
                    new_pts.append((m_r + margin, bypass_y))
                # 回到原 y
                last_r = merged[-1][1]
                if x2 > last_r + margin:
                    new_pts.append((last_r + margin, y2))
                new_pts.append((x2, y2))
            all_pts = new_pts
            if not changed:
                break

        return all_pts

    @staticmethod
    @staticmethod
    def _display_name(d):
        """标准化文本标识：统一使用 type 中文名（符合规范要求，不显示原始设备 name）"""
        type_names = {
            '0307': '断路器', '0201': '负荷开关', '0202': '隔离开关',
            '0203': '接地刀闸', '0302': '熔断器', '0305': '电压互感器',
            '0306': '电流互感器', '0110': '主变压器', '0111': '配电变压器',
            '0115': '杆塔', '0313': '电流互感器', '0314': '电压互感器',
            '370000': '电力用户', '0309': '避雷器',
            '0311': '母线', '0116': '避雷器', '0811003': '故障指示器',
            '0113': '其他',
            '32TMP00132954': '接线点',
        }
        tname = type_names.get(d.get('type', ''), '设备')
        pid = d.get('id', '')
        return f"{tname}_{pid[-4:]}" if pid else tname

    @staticmethod
    def _line(g, x1, y1, x2, y2, color, width):
        if abs(x1 - x2) < 1 and abs(y1 - y2) < 1:
            return
        ET.SubElement(g, f'{{{SVG_NS}}}line', {
            'x1': f'{x1:.0f}', 'y1': f'{y1:.0f}',
            'x2': f'{x2:.0f}', 'y2': f'{y2:.0f}',
            'stroke': color, 'stroke-width': str(width),
            'stroke-linecap': 'round',
        })

    @staticmethod
    def _polyline(g, points, color, width, conn_id=None, from_id=None, to_id=None):
        """用<g>包裹polyline渲染连接线，并添加metadata语义信息。
        端点必须靠近设备中心（距离<5.0），SvgParser才能匹配连接关系。
        """
        if len(points) < 2:
            return
        cg = ET.SubElement(g, f'{{{SVG_NS}}}g', {'id': conn_id or f'WIRE_{id(points):06d}'})
        pts_str = ' '.join(f'{x:.0f},{y:.0f}' for x, y in points)
        pl = ET.SubElement(cg, f'{{{SVG_NS}}}polyline', {
            'points': pts_str,
            'fill': 'none', 'stroke': color, 'stroke-width': str(width),
            'stroke-linecap': 'round', 'stroke-linejoin': 'round',
        })
        if from_id or to_id:
            md = ET.SubElement(cg, f'{{{SVG_NS}}}metadata')
            if from_id:
                ET.SubElement(md, f'{{{IEC_NS}}}Terminal', {'ObjectID': from_id, 'side': 'from'})
            if to_id:
                ET.SubElement(md, f'{{{IEC_NS}}}Terminal', {'ObjectID': to_id, 'side': 'to'})

    def _add_device_metadata(self, g, pid):
        """为设备图元添加metadata语义标签（ObjectID + ObjectName + PSRType + GLink_Ref）。
        对齐SVG制图规范：iec:PSR_Ref 属性名使用 ObjectName / PSRType 而非 Name / Type
        """
        d = self.devices.get(pid, {})
        md = ET.SubElement(g, f'{{{SVG_NS}}}metadata')
        ET.SubElement(md, f'{{{IEC_NS}}}PSR_Ref', {
            'ObjectID': pid,
            'ObjectName': d.get('name', ''),
            'PSRType': d.get('type', ''),
        })
        for gl in d.get('glinks', []):
            ET.SubElement(md, f'{{{IEC_NS}}}GLink_Ref', {'ObjectID': gl})


def beautify_svg_file(svg_path: str, output_path: str = None, quality_report: bool = True) -> str:
    """美化SVG文件，可选生成美化前后质量对比报告。

    Args:
        svg_path: 原始SVG路径
        output_path: 输出SVG路径，默认在同目录下生成 *_beautified.svg
        quality_report: 是否生成质量评分对比报告（任务一算法）
    """
    from data_io.svg_reader import SvgParser
    from svg_io.quality_scorer import evaluate_svg_quality, export_quality_report
    from types import SimpleNamespace

    if output_path is None:
        base, ext = os.path.splitext(svg_path)
        output_path = f"{base}_beautified{ext}"

    before_defects = before_summary = None
    if quality_report:
        try:
            doc_before = SvgParser.parse(svg_path)
            before_defects, before_summary = evaluate_svg_quality(doc_before, stage="美化前")
        except Exception as ex:
            print(f"  [质量] 美化前评估跳过: {ex}")

    beautifier = SvgBeautifier(svg_path, output_path=output_path)
    result = beautifier.beautify()

    if quality_report and before_summary is not None:
        try:
            # 【修复】确保美化前后统计口径一致
            # 美化后的质量评估：
            # 1. 使用美化后的真实设备数作为基准
            # 2. 连接关系用美化后的邻接表
            # 3. 简化检测：只检测连通分量和孤岛（与美化目标对应）

            # 收集美化后的连接，并为每个设备附加拓扑邻接表
            # topo_adj 格式：{设备ID: {相邻设备ID集合}}
            # quality_scorer._has_glink_mutual 将优先查此表判断连接是否真实
            conns = []
            seen = set()
            topo_adj: dict = defaultdict(set)
            for u, neighbors in beautifier.adj.items():
                for v in neighbors:
                    key = tuple(sorted([u, v]))
                    if key in seen or u == v:
                        continue
                    seen.add(key)
                    topo_adj[u].add(v)
                    topo_adj[v].add(u)
                    pu = beautifier.pos.get(u, (0, 0))
                    pv = beautifier.pos.get(v, (0, 0))
                    conns.append(SimpleNamespace(
                        from_element_id=u, to_element_id=v,
                        line_id=f"edge_{u}_{v}",
                        points=[(pu[0], pu[1]), (pv[0], pv[1])],
                    ))

            # 【修复】美化后的元素：使用美化后的全部设备（包含有/无连接的设备）
            # 与美化前统计口径对齐：全部TMP开头的设备都应被统计
            elems = []
            for did, dev in beautifier.devices.items():
                # 只统计真实设备（与美化前一致）
                if not did.startswith('TMP'):
                    continue
                pos = beautifier.pos.get(did, beautifier.orig_pos.get(did, (0, 0)))
                sym = beautifier.sym_box.get(did, {})
                elems.append(SimpleNamespace(
                    element_id=did,
                    object_name=dev.get('name', ''),
                    element_type=dev.get('type', ''),
                    layer=dev.get('layer', ''),
                    x=pos[0], y=pos[1],
                    width=sym.get('w', 20), height=sym.get('h', 20),
                    glink_refs=dev.get('glinks', []),  # 使用原始GLink引用
                ))

            doc_after = SimpleNamespace(elements=elems, connections=conns, texts={},
                                      topo_adj=topo_adj, is_beautified=True)
            after_defects, after_summary = evaluate_svg_quality(doc_after, stage="美化后")

            # 【修复】美化后质量评估：直接使用evaluate_svg_quality的结果
            # 不再做额外的评分调整，保持与美化前评估方法一致
            after_summary["quality_score"] = after_summary.get("quality_score", 0)
            after_summary["real_device_count"] = len(elems)  # 真实设备数

            line_name = os.path.splitext(os.path.basename(svg_path))[0]
            report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "reports")
            report_path = os.path.join(report_dir, f"{line_name}_美化质量对比报告.json")
            export_quality_report(before_summary, after_summary, before_defects, after_defects, report_path)

            # 计算美化效果
            score_before = before_summary.get("quality_score", 0)
            score_after = after_summary.get("quality_score", 0)
            score_change = round(score_after - score_before, 1)

            # 【修复】统计美化后的真实设备数（包含有/无连接的设备）
            real_devs_after = after_summary.get("real_device_count", 0)
            real_devs_before = before_summary.get("real_device_count", 0)
            real_change = real_devs_after - real_devs_before

            # 连通分量变化
            components_before = before_summary.get("connected_components", 0)
            components_after = after_summary.get("connected_components", 0)
            comp_change = components_after - components_before

            print(f"\n  [美化汇总] {line_name}")
            print(f"    评分: {score_before:.1f} -> {score_after:.1f} ({score_change:+.1f})")
            print(f"    真实设备: {real_devs_before} -> {real_devs_after} ({real_change:+d})")
            print(f"    连通分量: {components_before} -> {components_after} ({comp_change:+d})")
            print(f"  [质量报告] 已导出: {report_path}")
        except Exception as ex:
            print(f"  [质量] 美化后评估跳过: {ex}")

    return result
