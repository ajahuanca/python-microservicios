import os
import json
import threading
from confluent_kafka import Consumer, KafkaError


KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_EMPRESA = "empresa_creada"

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'proyectos_service_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)


def handle_empresa_event(mensaje):
    data = json.loads(mensaje)
    print(f"[Kafka] Recibido empresa_creada => {data}")
    # from .models import EmpresaLocal
    # EmpresaLocal.objects.update_or_create(
    #     id=data['id'],
    #     defaults={'nombre': data['nombre'], 'ruc': data['ruc']}
    # )


def consume_loop():
    consumer.subscribe([TOPIC_EMPRESA])
    print(f"[Kafka] Escuchando topic {TOPIC_EMPRESA} ...")
    while True:
        mensaje = consumer.poll(1.0)
        if mensaje is None:
            continue
        if mensaje.error():
            if mensaje.error().code() != KafkaError._PARTITION_EOF:
                print(f"[Kafka ERROR] {mensaje.error()}")
            continue
        handle_empresa_event(mensaje.value())


def start_consumer():
    t = threading.Thread(target=consume_loop, daemon=True)
    t.start()
