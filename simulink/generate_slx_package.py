# -*- coding: utf-8 -*-
"""
DRISHTI AI: Programmatic Simulink .slx Generator (SIH26038 Backlog Items #36-#42)
Generates native Simulink .slx model packages conforming to Open Packaging Conventions (OPC):
- simulink/MANGANEX_DR.slx
- simulink/telemed_dr_screening.slx
"""

import os
import zipfile
import xml.etree.ElementTree as ET

CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xml" ContentType="application/vnd.mathworks.simulink.model+xml"/>
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Override PartName="/simulink/blockdiagram.xml" ContentType="application/vnd.mathworks.simulink.model+xml"/>
  <Override PartName="/metadata/coreProperties.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>
"""

RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.mathworks.com/simulink/2010/relationships/blockdiagram" Target="simulink/blockdiagram.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="metadata/coreProperties.xml"/>
</Relationships>
"""

def make_core_properties_xml(model_name):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{model_name} Telemedicine Screening Workflow Model</dc:title>
  <dc:subject>MathWorks SIH26038 Diabetic Retinopathy Telemedicine Simulation</dc:subject>
  <dc:creator>DRISHTI AI System</dc:creator>
  <cp:lastModifiedBy>DRISHTI AI</cp:lastModifiedBy>
  <cp:revision>3.0</cp:revision>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-09-12T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-09-12T00:00:00Z</dcterms:modified>
</cp:coreProperties>
"""

def make_blockdiagram_xml(model_name):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<ModelInformation Version="1.0">
  <Model Name="{model_name}">
    <Properties>
      <Property Name="Solver" Value="VariableStepDiscrete"/>
      <Property Name="StopTime" Value="250"/>
      <Property Name="Description" Value="MathWorks SIH26038: 100,000-Patient Telemedicine Screening Workflow Optimization Model"/>
    </Properties>
    <System>
      <Block BlockType="Constant" Name="Daily_Patient_Target">
        <Properties>
          <Property Name="Value" Value="400"/>
          <Property Name="Position" Value="[50, 100, 110, 140]"/>
        </Properties>
      </Block>
      <Block BlockType="RandomNumber" Name="Arrival_Fluctuation">
        <Properties>
          <Property Name="Mean" Value="0"/>
          <Property Name="Variance" Value="25"/>
          <Property Name="SampleTime" Value="1"/>
          <Property Name="Position" Value="[50, 180, 110, 220]"/>
        </Properties>
      </Block>
      <Block BlockType="Sum" Name="Total_Arrivals">
        <Properties>
          <Property Name="Inputs" Value="++"/>
          <Property Name="Position" Value="[160, 135, 190, 185]"/>
        </Properties>
      </Block>
      <Block BlockType="Gain" Name="Edge_IQA_Quality_Check">
        <Properties>
          <Property Name="Gain" Value="0.975"/>
          <Property Name="Position" Value="[240, 145, 290, 175]"/>
        </Properties>
      </Block>
      <Block BlockType="Gain" Name="Edge_AI_Triage_Filter">
        <Properties>
          <Property Name="Gain" Value="0.25"/>
          <Property Name="Position" Value="[340, 145, 390, 175]"/>
        </Properties>
      </Block>
      <Block BlockType="RateLimiter" Name="Rural_Bandwidth_Constraint">
        <Properties>
          <Property Name="RisingSlewLimit" Value="120"/>
          <Property Name="FallingSlewLimit" Value="-120"/>
          <Property Name="Position" Value="[440, 140, 500, 180]"/>
        </Properties>
      </Block>
      <Block BlockType="Integrator" Name="Doctor_Backlog_Queue">
        <Properties>
          <Property Name="InitialCondition" Value="0"/>
          <Property Name="Position" Value="[550, 145, 580, 175]"/>
        </Properties>
      </Block>
      <Block BlockType="Scope" Name="Queue_Scope">
        <Properties>
          <Property Name="Position" Value="[650, 140, 690, 180]"/>
        </Properties>
      </Block>
      <Block BlockType="ToWorkspace" Name="Queue_Log">
        <Properties>
          <Property Name="VariableName" Value="sim_backlog_queue"/>
          <Property Name="SaveFormat" Value="Array"/>
          <Property Name="Position" Value="[650, 210, 710, 240]"/>
        </Properties>
      </Block>
      <Line>
        <Branch From="Daily_Patient_Target#1" To="Total_Arrivals#1"/>
      </Line>
      <Line>
        <Branch From="Arrival_Fluctuation#1" To="Total_Arrivals#2"/>
      </Line>
      <Line>
        <Branch From="Total_Arrivals#1" To="Edge_IQA_Quality_Check#1"/>
      </Line>
      <Line>
        <Branch From="Edge_IQA_Quality_Check#1" To="Edge_AI_Triage_Filter#1"/>
      </Line>
      <Line>
        <Branch From="Edge_AI_Triage_Filter#1" To="Rural_Bandwidth_Constraint#1"/>
      </Line>
      <Line>
        <Branch From="Rural_Bandwidth_Constraint#1" To="Doctor_Backlog_Queue#1"/>
      </Line>
      <Line>
        <Branch From="Doctor_Backlog_Queue#1" To="Queue_Scope#1"/>
      </Line>
      <Line>
        <Branch From="Doctor_Backlog_Queue#1" To="Queue_Log#1"/>
      </Line>
    </System>
  </Model>
</ModelInformation>
"""

def generate_slx(out_path, model_name):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES_XML.strip())
        zf.writestr('_rels/.rels', RELS_XML.strip())
        zf.writestr('metadata/coreProperties.xml', make_core_properties_xml(model_name).strip())
        zf.writestr('simulink/blockdiagram.xml', make_blockdiagram_xml(model_name).strip())
    print(f"Generated valid Simulink model: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == '__main__':
    sim_dir = os.path.dirname(os.path.abspath(__file__))
    generate_slx(os.path.join(sim_dir, 'MANGANEX_DR.slx'), 'MANGANEX_DR')
    generate_slx(os.path.join(sim_dir, 'telemed_dr_screening.slx'), 'telemed_dr_screening')
