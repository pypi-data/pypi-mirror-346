# Pipeline Configuration Documentation

This document describes the configuration options available for the Kafka to ClickHouse pipeline.

## Overview

The pipeline configuration is a JSON object that defines how data flows from Kafka topics to ClickHouse tables. It consists of three main components:

1. Source Configuration (Kafka)
2. Sink Configuration (ClickHouse)
3. Join Configuration (Optional)

## Root Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pipeline_id` | string | Yes | Unique identifier for the pipeline. Must be non-empty. |
| `source` | object | Yes | Configuration for the Kafka source. See [Source Configuration](#source-configuration). |
| `sink` | object | Yes | Configuration for the ClickHouse sink. See [Sink Configuration](#sink-configuration). |
| `join` | object | No | Configuration for joining multiple Kafka topics. See [Join Configuration](#join-configuration). |

## Source Configuration

The source configuration defines how to connect to and consume from Kafka topics.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | "kafka" is the only supported source |
| `provider` | string | No | Kafka provider, e.g. "aiven" |
| `topics` | array | Yes | List of Kafka topics to consume from. See [Topic Configuration](#topic-configuration). |
| `connection_params` | object | Yes | Kafka connection parameters. See [Connection Parameters](#connection-parameters). |

### Connection Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `brokers` | array | Yes | List of Kafka broker addresses (e.g., ["localhost:9092"]). |
| `protocol` | string | Yes | Security protocol for Kafka connection (e.g., "SASL_SSL"). |
| `mechanism` | string | Yes | Authentication mechanism (e.g., "SCRAM-SHA-256"). |
| `username` | string | Yes | Username for Kafka authentication. |
| `password` | string | Yes | Password for Kafka authentication. |
| `root_ca` | string | No | Cert. file for Kafka authentication. |

### Topic Configuration

Each topic in the `topics` array has the following configuration:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Name of the Kafka topic. |
| `consumer_group_initial_offset` | string | Yes | Initial offset for the consumer group ("earliest" or "newest"). |
| `schema` | object | Yes | Event schema definition. See [Schema Configuration](#schema-configuration). |
| `deduplication` | object | Yes | Deduplication settings. See [Deduplication Configuration](#deduplication-configuration). |

### Schema Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Schema type (Currently only "json" is supported). |
| `fields` | array | Yes | List of field definitions. See [Field Configuration](#field-configuration). |

### Field Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Field name. |
| `type` | string | Yes | Field type (e.g., "String", "Integer"). |

### Deduplication Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | boolean | Yes | Whether deduplication is enabled. |
| `id_field` | string | Yes | Field name used for message deduplication. |
| `id_field_type` | string | Yes | Type of the ID field (e.g., "string"). |
| `time_window` | string | Yes | Time window for deduplication (e.g., "1h" for one hour). |

## Sink Configuration

The sink configuration defines how to connect to and write to ClickHouse.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be "clickhouse". |
| `host` | string | Yes | ClickHouse server hostname. |
| `port` | integer | Yes | ClickHouse server port. |
| `database` | string | Yes | ClickHouse database name. |
| `username` | string | Yes | ClickHouse username. |
| `password` | string | Yes | ClickHouse password. |
| `table` | string | Yes | Target table name. |
| `secure` | boolean | No | Whether to use secure connection. Defaults to false. |
| `max_batch_size` | integer | No | Maximum number of records to batch before writing. Defaults to 1000. |
| `max_delay_time` | string | No | Maximum delay time before the messages are flushed into the sink. Defaults to "10m". |
| `table_mapping` | array | Yes | List of field to column mappings. See [Table Mapping Configuration](#table-mapping-configuration). |

### Table Mapping Configuration

Each mapping in the `table_mapping` array has the following configuration:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | Yes | Name of the source topic. |
| `field_name` | string | Yes | Source field name. |
| `column_name` | string | Yes | Target column name. |
| `column_type` | string | Yes | Target column type. |

## Join Configuration

The join configuration defines how to join data from multiple Kafka topics.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | boolean | Yes | Whether joining is enabled. |
| `type` | string | Yes | Join type (e.g., "temporal"). |
| `sources` | array | Yes | List of sources to join. See [Join Source Configuration](#join-source-configuration). |

### Join Source Configuration

Each source in the `sources` array has the following configuration:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | Yes | Name of the Kafka topic to join. |
| `join_key` | string | Yes | Field name used for joining records. |
| `time_window` | string | Yes | Time window for joining records (e.g., "1h" for one hour). |
| `orientation` | string | Yes | Join orientation ("left" or "right"). |

## Example Configuration

```json
{
  "pipeline_id": "kafka-to-clickhouse-pipeline",
  "source": {
    "type": "kafka",
    "provider": "aiven",
    "connection_params": {
      "brokers": [
        "kafka-broker-0:9092",
        "kafka-broker-1:9092"
      ],
      "protocol": "SASL_SSL",
      "mechanism": "SCRAM-SHA-256",
      "username": "<user>",
      "password": "<password>",
      "root_ca": "<base64 encoded ca>"
    },
    "topics": [
      {
        "consumer_group_initial_offset": "earliest",
        "name": "user_logins",
        "schema": {
          "type": "json",
          "fields": [
            {
              "name": "session_id",
              "type": "string"
            },
            {
              "name": "user_id",
              "type": "string"
            },
            {
              "name": "timestamp",
              "type": "datetime"
            }
          ]
        },
        "deduplication": {
          "enabled": true,
          "id_field": "session_id",
          "id_field_type": "string",
          "time_window": "12h"
        }
      },
      {
        "consumer_group_initial_offset": "earliest",
        "name": "orders",
        "schema": {
          "type": "json",
          "fields": [
            {
              "name": "user_id",
              "type": "string"
            },
            {
              "name": "order_id",
              "type": "string"
            },
            {
              "name": "timestamp",
              "type": "datetime"
            }
          ]
        },
        "deduplication": {
          "enabled": true,
          "id_field": "order_id",
          "id_field_type": "string",
          "time_window": "12h"
        }
      }
    ]
  },
  "join": {
    "enabled": false,
    "type": "temporal",
    "sources": [
      {
        "source_id": "user_logins",
        "join_key": "user_id",
        "time_window": "1h",
        "orientation": "left"
      },
      {
        "source_id": "orders",
        "join_key": "user_id",
        "time_window": "1h",
        "orientation": "right"
      }
    ]
  },
  "sink": {
    "type": "clickhouse",
    "provider": "aiven",
    "host": "<host>",
    "port": "12753",
    "database": "default",
    "username": "<user>",
    "password": "<password>",
    "secure": true,
    "max_batch_size": 1,
    "max_delay_time": "10m",
    "table": "user_orders",
    "table_mapping": [
      {
        "source_id": "user_logins",
        "field_name": "session_id",
        "column_name": "session_id",
        "column_type": "UUID"
      },
      {
        "source_id": "user_logins",
        "field_name": "user_id",
        "column_name": "user_id",
        "column_type": "UUID"
      },
      {
        "source_id": "orders",
        "field_name": "order_id",
        "column_name": "order_id",
        "column_type": "UUID"
      },
      {
        "source_id": "user_logins",
        "field_name": "timestamp",
        "column_name": "login_at",
        "column_type": "DataTime"
      },
      {
        "source_id": "orders",
        "field_name": "timestamp",
        "column_name": "order_placed_at",
        "column_type": "DateTime"
      }
    ]
  }
}
```
