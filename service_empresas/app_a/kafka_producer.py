import os
import json
import threading
from confluent_kafka import Producer


KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_EMPRESA = "empresa_creada"

producer_config = {
    "bootstrap.servers": KAFKA_BROKER,
    "socket.timeout.ms": 2000,
    "queue.buffering.max.ms": 100,
    "enable.idempotence": False,  # evita bloqueos por confirmaciones
}

producer = Producer(producer_config)


def delivery_report(err, msg):
    """Callback opcional para logs"""
    if err is not None:
        print(f"[Kafka] Error al enviar mensaje: {err}")
    else:
        print(f"[Kafka] Mensaje entregado a {msg.topic()} [{msg.partition()}]")


def publish_empresa_creada_event(empresa):
    """
    Publica un evento cuando se crea una empresa, de manera asíncrona.
    Si Kafka no está disponible, se registra el error, pero no se bloquea la API.
    """
    def _send():
        try:
            data = {
                "id": empresa.id,
                "razon_social": empresa.razon_social,
                "nit": empresa.nit,
            }
            value = json.dumps(data).encode("utf-8")
            producer.produce(
                topic=TOPIC_EMPRESA,
                value=value,
                callback=delivery_report
            )
            producer.poll(0)
            producer.flush(1)  # espera 1 segundo como máximo
        except Exception as e:
            print(f"[Kafka] Error inesperado publicando evento empresa_creada: {e}")

    # Lanza en hilo separado (no bloquea Django)
    threading.Thread(target=_send, daemon=True).start()
