from confluent_kafka import Consumer
import threading, json, os, time

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

empresa_cache = set()


def load_empresas_from_kafka():
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'service_proyectos_empresa_cache',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(["empresa_creada"])

    print("[Kafka] Escuchando empresas_creadas...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"[Kafka] Error: {msg.error()}")
            continue

        try:
            event = json.loads(msg.value().decode('utf-8'))
            empresa_id = event.get("id")
            if empresa_id:
                empresa_cache.add(empresa_id)
                print(f"[Kafka] Empresa registrada en cache: {empresa_id}")
        except Exception as e:
            print(f"[Kafka] Error procesando mensaje: {e}")


def start_empresa_cache_listener():
    t = threading.Thread(target=load_empresas_from_kafka, daemon=True)
    t.start()
