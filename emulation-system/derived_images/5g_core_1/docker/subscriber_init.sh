#!/bin/bash
MONGODB_DB="open5gs"
IMSI="001010123456780"
KEY="00112233445566778899aabbccddeeff"
OPC="63BFA50EE6523365FF14C1F45F88737D"
AMF="8000"
SQN=10
AMBR_DL_VALUE=1
AMBR_UL_VALUE=1
AMBR_UNIT=3
QCI_INDEX=9
ARP_PRIORITY=8
SST_VALUE=1
PROFILE_TITLE="srsUe"

SUBSCRIBER_DOC="{
    imsi: '${IMSI}',
    schema_version: 1,
    ambr: { downlink: { value: ${AMBR_DL_VALUE}, unit: ${AMBR_UNIT} }, uplink: { value: ${AMBR_UL_VALUE}, unit: ${AMBR_UNIT} } },
    imeisv: '3534900698733153',
    access_restriction_data: 32,
    subscriber_status: 0,
    operator_determined_barring: 0,
    network_access_mode: 0,
    subscribed_rau_tau_timer: 12,
    security: {
      k: '${KEY}',
      amf: '${AMF}',
      op: null,
      opc: '${OPC}',
      sqn: NumberLong('${SQN}')
    },
    slice: [
      {
        sst: ${SST_VALUE},
        default_indicator: true,
        session: [
          {
            qos: {
              arp: { priority_level: ${ARP_PRIORITY}, pre_emption_capability: 1, pre_emption_vulnerability: 1 },
              index: ${QCI_INDEX}
            },
            ambr: { downlink: { value: ${AMBR_DL_VALUE}, unit: ${AMBR_UNIT} }, uplink: { value: ${AMBR_UL_VALUE}, unit: ${AMBR_UNIT} } },
            name: 'internet',
            type: 3,
            pcc_rule: []
          }
        ]
      }
    ],
    msisdn: [], mme_host: [], mme_realm: [], purge_flag: [], __v: 0
}"

PROFILE_DOC="{
    ambr: { downlink: { value: ${AMBR_DL_VALUE}, unit: ${AMBR_UNIT} }, uplink: { value: ${AMBR_UL_VALUE}, unit: ${AMBR_UNIT} } },
    schema_version: 1,
    title: '${PROFILE_TITLE}',
    security: {
      k: '${KEY}',
      amf: '${AMF}',
      op: null,
      opc: '${OPC}'
    },
    slice: [
      {
        sst: ${SST_VALUE},
        default_indicator: true,
        session: [
          {
            qos: {
              arp: { priority_level: ${ARP_PRIORITY}, pre_emption_capability: 1, pre_emption_vulnerability: 1 },
              index: ${QCI_INDEX}
            },
            ambr: { downlink: { value: ${AMBR_DL_VALUE}, unit: ${AMBR_UNIT} }, uplink: { value: ${AMBR_UL_VALUE}, unit: ${AMBR_UNIT} } },
            name: 'internet',
            type: 3,
            pcc_rule: []
          }
        ]
      }
    ],
    msisdn: [], imeisv: [], __v: 0
}"

mongosh "${MONGODB_DB}" --eval "db.subscribers.insertOne(${SUBSCRIBER_DOC})"
mongosh "${MONGODB_DB}" --eval "db.profiles.insertOne(${PROFILE_DOC})"