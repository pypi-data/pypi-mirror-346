# RTOS CLI - Ayuda de Comandos

Este documento describe el uso de cada comando disponible en `rtos_cli.py`, la herramienta CLI para automatizar proyectos PlatformIO + FreeRTOS personalizados para el ESP32.

---

## Comandos Disponibles

### `create_project <project_name>`

Crea una estructura completa de proyecto PlatformIO + FreeRTOS para ESP32.

* Utiliza la placa `esp32-eddie-w.json`.
* Estructura carpetas, `platformio.ini`, `README.md`, y archivos base.

**Ejemplo:**

```bash
python rtos_cli.py create_project MiProyecto
```

---

### `create_task <task_name>`

Crea una tarea de FreeRTOS con archivos `.cpp` y `.h`, y la integra al proyecto.

**Ejemplo:**

```bash
python rtos_cli.py create_task sensor_reader
```

---

### `create_global_var <var_name> <var_type> <sync_type>`

Declara una variable global sincronizada con mutex o semáforo.

* `sync_type` puede ser: `mutex` o `semaphore`.

**Ejemplo:**

```bash
python rtos_cli.py create_global_var contador int mutex
```

---

### `create_queue <queue_name> <item_type> <length>`

Declara una cola global y la integra al archivo `project_config.h`.

**Ejemplo:**

```bash
python rtos_cli.py create_queue cola_mensajes int 20
```

---

### `create_timer <timer_name> <period_ms> <mode>`

Crea un temporizador de FreeRTOS (único o periódico).

* `mode` puede ser: `oneshot` o `periodic`.

**Ejemplo:**

```bash
python rtos_cli.py create_timer timer_led 1000 periodic
```

---

### `create_event_group <group_name>`

Crea un grupo de eventos FreeRTOS y lo registra globalmente.

**Ejemplo:**

```bash
python rtos_cli.py create_event_group grupo_eventos
```

---

### `create_mutex <mutex_name>`

Crea un mutex global de FreeRTOS.

**Ejemplo:**

```bash
python rtos_cli.py create_mutex mtx_sensor
```

---

### `create_semaphore <semaphore_name>`

Crea un semáforo binario global de FreeRTOS.

**Ejemplo:**

```bash
python rtos_cli.py create_semaphore sem_ready
```

---

### `create_module <module_name>`

Crea un módulo genérico C++ con archivo `.cpp` y `.h` más integración de cabecera y actualización del README.

**Ejemplo:**

```bash
python rtos_cli.py create_module comunicacion_lora
```

---

## Notas Generales

* Todos los cambios se integran automáticamente al proyecto existente.
* Se actualiza `README.md`, `platformio.ini` y `project_config.h` si aplica.
* Todas las funciones incluyen documentación tipo Doxygen.

---

Para obtener ayuda directamente desde CLI:

```bash
python rtos_cli.py --help
```

---

### `create_topic <task_name> <topic_name> <direction> <type> <rate>`

Crea un tópico de comunicación entre tareas tipo Publisher/Subscriber basado en colas de FreeRTOS.

* `direction`: puede ser `pub` (publicador) o `sub` (suscriptor).
* `type`: tipo de dato del tópico (e.g., `float`, `int`, etc).
* `rate`: intervalo de operación del tópico en milisegundos (usado como guía para la frecuencia de uso).

Este comando inserta automáticamente:

- Declaración de la cola asociada en `project_config.h`.
- Funciones `publish_<topic>()` y/o `subscribe_<topic>()` en `.cpp` y `.h` de la tarea correspondiente.
- Llamadas básicas de prueba al publicar y/o suscribir dentro del bucle `loop` de la tarea.
- Comentarios tipo Doxygen en cada función creada.
- Entrada en `README.md` del proyecto de destino.

**Ejemplos:**

```bash
python rtos_cli.py create_topic sensor_1 temperatura pub float 500
python rtos_cli.py create_topic actuador_1 temperatura sub float 500
```

---
