<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_1" targetNamespace="http://bpmn.io/schema/bpmn" exporter="bpmn-js (https://demo.bpmn.io)" exporterVersion="18.3.1">
  <bpmn:collaboration id="Collaboration_0vl6jjh">
    <bpmn:participant id="Participant_0e3bw5k" name="CSV and Excel Processing Workflow" processRef="Process_1" />
  </bpmn:collaboration>
  <bpmn:process id="Process_1" isExecutable="false">
    <bpmn:laneSet id="LaneSet_0s9mzlg">
      <bpmn:lane id="Lane_01h9jrt" name="Output Generation">
        <bpmn:flowNodeRef>Event_0vrbcwd</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_19xbvtx</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0f7acn9</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_1bpyvt5</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_0xqcuyl" name="Data Processing">
        <bpmn:flowNodeRef>Activity_11l4dhn</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0b89ww8</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_17rjo3l</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0ujx8br</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_1fztye5</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_1c0s8ig</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_1smmzhd</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_00g1ddr</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_0qrypcl" name="Input Preparation">
        <bpmn:flowNodeRef>StartEvent_1</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_1xf6q01</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_131wh5c</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_1xtxsau</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    <bpmn:startEvent id="StartEvent_1" name="Start Process">
      <bpmn:outgoing>Flow_08yxcip</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Activity_1xf6q01" name="Load CSV file with store names">
      <bpmn:incoming>Flow_08yxcip</bpmn:incoming>
      <bpmn:outgoing>Flow_1v8ytfi</bpmn:outgoing>
      <bpmn:dataOutputAssociation id="DataOutputAssociation_1pzqq9g">
        <bpmn:targetRef>DataObjectReference_1aqjwkg</bpmn:targetRef>
      </bpmn:dataOutputAssociation>
    </bpmn:task>
    <bpmn:task id="Activity_131wh5c" name="Load XLSX file and access PRE ALLOCATION sheet">
      <bpmn:incoming>Flow_1v8ytfi</bpmn:incoming>
      <bpmn:outgoing>Flow_0pv1tfw</bpmn:outgoing>
      <bpmn:dataOutputAssociation id="DataOutputAssociation_00l0ugm">
        <bpmn:targetRef>DataObjectReference_0x7rpbz</bpmn:targetRef>
      </bpmn:dataOutputAssociation>
    </bpmn:task>
    <bpmn:task id="Activity_11l4dhn" name="Read next store name from CSV">
      <bpmn:incoming>Flow_1k2cvej</bpmn:incoming>
      <bpmn:outgoing>Flow_1r1iyhi</bpmn:outgoing>
      <bpmn:property id="Property_1obx1h9" name="__targetRef_placeholder" />
      <bpmn:dataInputAssociation id="DataInputAssociation_0rzp0jp">
        <bpmn:sourceRef>DataObjectReference_1aqjwkg</bpmn:sourceRef>
        <bpmn:targetRef>Property_1obx1h9</bpmn:targetRef>
      </bpmn:dataInputAssociation>
    </bpmn:task>
    <bpmn:task id="Activity_0b89ww8" name="Locate matching store column in XLSX">
      <bpmn:incoming>Flow_1r1iyhi</bpmn:incoming>
      <bpmn:outgoing>Flow_16wyzs5</bpmn:outgoing>
      <bpmn:property id="Property_0u9g5vc" name="__targetRef_placeholder" />
      <bpmn:dataInputAssociation id="DataInputAssociation_1r3bfoe">
        <bpmn:sourceRef>DataObjectReference_0x7rpbz</bpmn:sourceRef>
        <bpmn:targetRef>Property_0u9g5vc</bpmn:targetRef>
      </bpmn:dataInputAssociation>
    </bpmn:task>
    <bpmn:task id="Activity_17rjo3l" name="Select store column (quantities) + EANCode and SEASON columns">
      <bpmn:incoming>Flow_16wyzs5</bpmn:incoming>
      <bpmn:outgoing>Flow_14v8bst</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_0ujx8br" name="Complete processing all stores">
      <bpmn:incoming>Flow_08yvs3l</bpmn:incoming>
      <bpmn:outgoing>Flow_0qdhhh3</bpmn:outgoing>
    </bpmn:task>
    <bpmn:dataObjectReference id="DataObjectReference_0x7rpbz" name="Main XLSX File with PRE ALLOCATION sheet" dataObjectRef="DataObject_1t12pmn" />
    <bpmn:dataObject id="DataObject_1t12pmn" />
    <bpmn:endEvent id="Event_0vrbcwd" name="Process Completed">
      <bpmn:incoming>Flow_0qdhhh3</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:task id="Activity_1fztye5" name="Create new dataframe with selected columns">
      <bpmn:incoming>Flow_14v8bst</bpmn:incoming>
      <bpmn:outgoing>Flow_1u4s3pc</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_1c0s8ig" name="For each SEASON, filter dataframe to only rows with that SEASON">
      <bpmn:incoming>Flow_1u4s3pc</bpmn:incoming>
      <bpmn:outgoing>Flow_0bhpkjl</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_08yxcip" sourceRef="StartEvent_1" targetRef="Activity_1xf6q01" />
    <bpmn:sequenceFlow id="Flow_1v8ytfi" sourceRef="Activity_1xf6q01" targetRef="Activity_131wh5c" />
    <bpmn:sequenceFlow id="Flow_0pv1tfw" sourceRef="Activity_131wh5c" targetRef="Gateway_1xtxsau" />
    <bpmn:sequenceFlow id="Flow_1p71fkm" name="Yes" sourceRef="Gateway_00g1ddr" targetRef="Gateway_1xtxsau" />
    <bpmn:sequenceFlow id="Flow_1k2cvej" sourceRef="Gateway_1xtxsau" targetRef="Activity_11l4dhn" />
    <bpmn:sequenceFlow id="Flow_1r1iyhi" sourceRef="Activity_11l4dhn" targetRef="Activity_0b89ww8" />
    <bpmn:sequenceFlow id="Flow_16wyzs5" sourceRef="Activity_0b89ww8" targetRef="Activity_17rjo3l" />
    <bpmn:sequenceFlow id="Flow_14v8bst" sourceRef="Activity_17rjo3l" targetRef="Activity_1fztye5" />
    <bpmn:sequenceFlow id="Flow_08yvs3l" name="No" sourceRef="Gateway_00g1ddr" targetRef="Activity_0ujx8br" />
    <bpmn:sequenceFlow id="Flow_0qdhhh3" sourceRef="Activity_0ujx8br" targetRef="Event_0vrbcwd" />
    <bpmn:sequenceFlow id="Flow_1u4s3pc" sourceRef="Activity_1fztye5" targetRef="Activity_1c0s8ig" />
    <bpmn:sequenceFlow id="Flow_0fzdbkq" name="No" sourceRef="Gateway_19xbvtx" targetRef="Activity_1c0s8ig" />
    <bpmn:sequenceFlow id="Flow_0bhpkjl" sourceRef="Activity_1c0s8ig" targetRef="Activity_1smmzhd" />
    <bpmn:sequenceFlow id="Flow_0uzvsmv" sourceRef="Activity_1smmzhd" targetRef="Activity_0f7acn9" />
    <bpmn:sequenceFlow id="Flow_197j8oh" sourceRef="Activity_0f7acn9" targetRef="Gateway_19xbvtx" />
    <bpmn:sequenceFlow id="Flow_0t0ylj3" name="Yes" sourceRef="Gateway_19xbvtx" targetRef="Activity_1bpyvt5" />
    <bpmn:sequenceFlow id="Flow_0qsqnks" sourceRef="Activity_1bpyvt5" targetRef="Gateway_00g1ddr" />
    <bpmn:exclusiveGateway id="Gateway_19xbvtx" name="All SEASONs processed?">
      <bpmn:incoming>Flow_197j8oh</bpmn:incoming>
      <bpmn:outgoing>Flow_0t0ylj3</bpmn:outgoing>
      <bpmn:outgoing>Flow_0fzdbkq</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:task id="Activity_1smmzhd" name="Create sheet in new XLSX file for current SEASON">
      <bpmn:incoming>Flow_0bhpkjl</bpmn:incoming>
      <bpmn:outgoing>Flow_0uzvsmv</bpmn:outgoing>
    </bpmn:task>
    <bpmn:dataStoreReference id="DataStoreReference_0wgqowk" name="Store-SEASON TXT files with repeated EANCodes" />
    <bpmn:task id="Activity_0f7acn9" name="Generate TXT file with repeated EANCode values based on quantities">
      <bpmn:incoming>Flow_0uzvsmv</bpmn:incoming>
      <bpmn:outgoing>Flow_197j8oh</bpmn:outgoing>
      <bpmn:dataOutputAssociation id="DataOutputAssociation_0t2uf6r">
        <bpmn:targetRef>DataStoreReference_0wgqowk</bpmn:targetRef>
      </bpmn:dataOutputAssociation>
    </bpmn:task>
    <bpmn:task id="Activity_1bpyvt5" name="Save XLSX file with multiple sheets for each SEASON">
      <bpmn:incoming>Flow_0t0ylj3</bpmn:incoming>
      <bpmn:outgoing>Flow_0qsqnks</bpmn:outgoing>
      <bpmn:dataOutputAssociation id="DataOutputAssociation_09r0xrc">
        <bpmn:targetRef>DataStoreReference_0dn0hy2</bpmn:targetRef>
      </bpmn:dataOutputAssociation>
    </bpmn:task>
    <bpmn:dataStoreReference id="DataStoreReference_0dn0hy2" name="Store-specific XLSX files with SEASON sheets" />
    <bpmn:exclusiveGateway id="Gateway_00g1ddr" name="More stores?">
      <bpmn:incoming>Flow_0qsqnks</bpmn:incoming>
      <bpmn:outgoing>Flow_1p71fkm</bpmn:outgoing>
      <bpmn:outgoing>Flow_08yvs3l</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:exclusiveGateway id="Gateway_1xtxsau" name="Start Processing Loop">
      <bpmn:incoming>Flow_0pv1tfw</bpmn:incoming>
      <bpmn:incoming>Flow_1p71fkm</bpmn:incoming>
      <bpmn:outgoing>Flow_1k2cvej</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:dataObjectReference id="DataObjectReference_1aqjwkg" name="Store Names CSV" dataObjectRef="DataObject_03b4hiv" />
    <bpmn:dataObject id="DataObject_03b4hiv" />
  </bpmn:process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_0vl6jjh">
      <bpmndi:BPMNShape id="Participant_0e3bw5k_di" bpmnElement="Participant_0e3bw5k" isHorizontal="true">
        <dc:Bounds x="160" y="85" width="2000" height="885" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Lane_01h9jrt_di" bpmnElement="Lane_01h9jrt" isHorizontal="true">
        <dc:Bounds x="190" y="720" width="1970" height="250" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Lane_0xqcuyl_di" bpmnElement="Lane_0xqcuyl" isHorizontal="true">
        <dc:Bounds x="190" y="370" width="1970" height="350" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Lane_0qrypcl_di" bpmnElement="Lane_0qrypcl" isHorizontal="true">
        <dc:Bounds x="190" y="85" width="1970" height="285" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1">
        <dc:Bounds x="232" y="242" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="217" y="285" width="67" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1xf6q01_di" bpmnElement="Activity_1xf6q01">
        <dc:Bounds x="320" y="220" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_131wh5c_di" bpmnElement="Activity_131wh5c">
        <dc:Bounds x="480" y="220" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_11l4dhn_di" bpmnElement="Activity_11l4dhn">
        <dc:Bounds x="790" y="400" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0b89ww8_di" bpmnElement="Activity_0b89ww8">
        <dc:Bounds x="930" y="400" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_17rjo3l_di" bpmnElement="Activity_17rjo3l">
        <dc:Bounds x="1080" y="400" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0ujx8br_di" bpmnElement="Activity_0ujx8br">
        <dc:Bounds x="1900" y="530" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="DataObjectReference_0x7rpbz_di" bpmnElement="DataObjectReference_0x7rpbz">
        <dc:Bounds x="959" y="165" width="36" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="932" y="103" width="76" height="53" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Event_0vrbcwd_di" bpmnElement="Event_0vrbcwd">
        <dc:Bounds x="2072" y="802" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="2064" y="845" width="54" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1fztye5_di" bpmnElement="Activity_1fztye5">
        <dc:Bounds x="1220" y="400" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1c0s8ig_di" bpmnElement="Activity_1c0s8ig">
        <dc:Bounds x="1360" y="400" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_19xbvtx_di" bpmnElement="Gateway_19xbvtx" isMarkerVisible="true">
        <dc:Bounds x="1545" y="775" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1476" y="746" width="67" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1smmzhd_di" bpmnElement="Activity_1smmzhd">
        <dc:Bounds x="1360" y="560" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="DataStoreReference_0wgqowk_di" bpmnElement="DataStoreReference_0wgqowk">
        <dc:Bounds x="1385" y="885" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1463" y="893" width="76" height="53" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0f7acn9_di" bpmnElement="Activity_0f7acn9">
        <dc:Bounds x="1360" y="760" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1bpyvt5_di" bpmnElement="Activity_1bpyvt5">
        <dc:Bounds x="1720" y="760" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="DataStoreReference_0dn0hy2_di" bpmnElement="DataStoreReference_0dn0hy2">
        <dc:Bounds x="1745" y="885" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1814" y="893" width="82" height="40" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_00g1ddr_di" bpmnElement="Gateway_00g1ddr" isMarkerVisible="true">
        <dc:Bounds x="1745" y="545" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1696.5" y="533" width="65" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_1xtxsau_di" bpmnElement="Gateway_1xtxsau" isMarkerVisible="true">
        <dc:Bounds x="675" y="235" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="660" y="205" width="81" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="DataObjectReference_1aqjwkg_di" bpmnElement="DataObjectReference_1aqjwkg">
        <dc:Bounds x="819" y="125" width="36" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="805" y="95" width="65" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNEdge id="Flow_08yxcip_di" bpmnElement="Flow_08yxcip">
        <di:waypoint x="268" y="260" />
        <di:waypoint x="320" y="260" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1v8ytfi_di" bpmnElement="Flow_1v8ytfi">
        <di:waypoint x="420" y="260" />
        <di:waypoint x="480" y="260" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0pv1tfw_di" bpmnElement="Flow_0pv1tfw">
        <di:waypoint x="580" y="260" />
        <di:waypoint x="675" y="260" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1p71fkm_di" bpmnElement="Flow_1p71fkm">
        <di:waypoint x="1770" y="545" />
        <di:waypoint x="1770" y="260" />
        <di:waypoint x="725" y="260" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1781" y="523" width="18" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1k2cvej_di" bpmnElement="Flow_1k2cvej">
        <di:waypoint x="700" y="285" />
        <di:waypoint x="700" y="440" />
        <di:waypoint x="790" y="440" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1r1iyhi_di" bpmnElement="Flow_1r1iyhi">
        <di:waypoint x="890" y="440" />
        <di:waypoint x="930" y="440" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_16wyzs5_di" bpmnElement="Flow_16wyzs5">
        <di:waypoint x="1030" y="440" />
        <di:waypoint x="1080" y="440" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_14v8bst_di" bpmnElement="Flow_14v8bst">
        <di:waypoint x="1180" y="440" />
        <di:waypoint x="1220" y="440" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_08yvs3l_di" bpmnElement="Flow_08yvs3l">
        <di:waypoint x="1795" y="570" />
        <di:waypoint x="1900" y="570" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1793" y="583" width="15" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0qdhhh3_di" bpmnElement="Flow_0qdhhh3">
        <di:waypoint x="2000" y="570" />
        <di:waypoint x="2090" y="570" />
        <di:waypoint x="2090" y="802" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1u4s3pc_di" bpmnElement="Flow_1u4s3pc">
        <di:waypoint x="1320" y="440" />
        <di:waypoint x="1360" y="440" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0fzdbkq_di" bpmnElement="Flow_0fzdbkq">
        <di:waypoint x="1570" y="775" />
        <di:waypoint x="1570" y="440" />
        <di:waypoint x="1460" y="440" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1582" y="751" width="15" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0bhpkjl_di" bpmnElement="Flow_0bhpkjl">
        <di:waypoint x="1410" y="480" />
        <di:waypoint x="1410" y="560" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0uzvsmv_di" bpmnElement="Flow_0uzvsmv">
        <di:waypoint x="1410" y="640" />
        <di:waypoint x="1410" y="760" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_197j8oh_di" bpmnElement="Flow_197j8oh">
        <di:waypoint x="1460" y="800" />
        <di:waypoint x="1545" y="800" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0t0ylj3_di" bpmnElement="Flow_0t0ylj3">
        <di:waypoint x="1595" y="800" />
        <di:waypoint x="1720" y="800" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1592" y="813" width="18" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0qsqnks_di" bpmnElement="Flow_0qsqnks">
        <di:waypoint x="1770" y="760" />
        <di:waypoint x="1770" y="595" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="DataOutputAssociation_1pzqq9g_di" bpmnElement="DataOutputAssociation_1pzqq9g">
        <di:waypoint x="380" y="220" />
        <di:waypoint x="380" y="150" />
        <di:waypoint x="819" y="150" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="DataOutputAssociation_00l0ugm_di" bpmnElement="DataOutputAssociation_00l0ugm">
        <di:waypoint x="530" y="220" />
        <di:waypoint x="530" y="190" />
        <di:waypoint x="959" y="190" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="DataInputAssociation_0rzp0jp_di" bpmnElement="DataInputAssociation_0rzp0jp">
        <di:waypoint x="838" y="175" />
        <di:waypoint x="838" y="400" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="DataInputAssociation_1r3bfoe_di" bpmnElement="DataInputAssociation_1r3bfoe">
        <di:waypoint x="978" y="215" />
        <di:waypoint x="978" y="400" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="DataOutputAssociation_0t2uf6r_di" bpmnElement="DataOutputAssociation_0t2uf6r">
        <di:waypoint x="1410" y="840" />
        <di:waypoint x="1410" y="885" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="DataOutputAssociation_09r0xrc_di" bpmnElement="DataOutputAssociation_09r0xrc">
        <di:waypoint x="1770" y="840" />
        <di:waypoint x="1770" y="885" />
      </bpmndi:BPMNEdge>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
