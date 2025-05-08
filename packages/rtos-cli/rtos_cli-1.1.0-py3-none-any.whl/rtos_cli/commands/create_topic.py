# rtos_cli/commands/create_topic.py
"""
@file create_topic.py
@brief Command to create a new FreeRTOS topic for a task, enabling publish/subscribe communication between tasks
@version 1.4.0
@date 2025-05-08
@license MIT
"""

import os
from rtos_cli.utils import file_utils, readme_updater, doxygen

def run(task_name, topic_name, direction, data_type, rate):
    print(f"🔧 Creating topic '{topic_name}' for task '{task_name}' ({direction})...")

    if direction not in ["pub", "sub"]:
        print(f"❌ Invalid direction: {direction}. Must be 'pub' or 'sub'.")
        return

    topic_var_name = f"{topic_name}_queue"
    func_name = f"{'publish' if direction == 'pub' else 'subscribe'}_{topic_name}"
    set_func = f"set_{task_name}"

    base_path = os.getcwd()
    include_path = os.path.join(base_path, "include")
    src_path = os.path.join(base_path, "src")

    project_config_path = os.path.join(include_path, "project_config.h")
    task_header_path = os.path.join(include_path, f"{task_name}.h")
    task_source_path = os.path.join(src_path, f"{task_name}.cpp")
    main_cpp_path = os.path.join(src_path, "main.cpp")

    # Handle publication
    if direction == "pub":
        if file_utils.contains_line(project_config_path, topic_var_name):
            print(f"⚠️ Topic '{topic_name}' already declared. Aborting.")
            return

        queue_decl = f"extern QueueHandle_t {topic_var_name};\n"
        queue_def = f"QueueHandle_t {topic_var_name};\n"

        file_utils.insert_in_file(project_config_path, queue_decl, "// -- TOPIC QUEUE DECLARATIONS --")
        file_utils.insert_in_file(main_cpp_path, queue_def, "// -- TOPIC QUEUE DEFINITIONS --")

        func_decl = f"void {func_name}({data_type} data);\n"
        func_impl = f"""
void {func_name}({data_type} data) {{
    xQueueSend({topic_var_name}, &data, portMAX_DELAY);
    Serial.print("[{func_name}] Published: ");
    Serial.println(data);
}}
"""

        doxygen.add_function_description(
            header_path=task_header_path,
            function_name=func_name,
            brief=f"Publish to topic '{topic_name}'",
            params=[("data", data_type)],
            returns="void"
        )

        file_utils.insert_in_file(task_header_path, func_decl, "// -- TASK FUNCTION DECLARATIONS --")

        queue_creation = f"""
if ({topic_var_name} == NULL) {{
    {topic_var_name} = xQueueCreate(10, sizeof({data_type}));
}}"""
        file_utils.insert_in_file(task_source_path, queue_creation, "// -- TASK INIT EXTENSIONS --")

    # Handle subscription
    else:
        if not file_utils.contains_line(project_config_path, topic_var_name):
            print(f"❌ Cannot subscribe: queue '{topic_var_name}' not found.")
            return

        func_decl = f"void {func_name}();\n"
        func_impl = f"""
void {func_name}() {{
    {data_type} data;
    if (xQueueReceive({topic_var_name}, &data, pdMS_TO_TICKS({rate}))) {{
        {set_func}(data);  // Optional: implement this in task file
        Serial.print("[{func_name}] Received: ");
        Serial.println(data);
    }}
}}
"""

        doxygen.add_function_description(
            header_path=task_header_path,
            function_name=func_name,
            brief=f"Subscribe to topic '{topic_name}'",
            params=[],
            returns="void"
        )

        file_utils.insert_in_file(task_header_path, func_decl, "// -- TOPIC FUNCTION DECLARATIONS --")

    # Insert implementations
    file_utils.insert_in_file(task_source_path, func_impl, "// -- TOPIC FUNCTION DEFINITIONS --")

    # For publication, ensure function is called in loop (with dummy data)
    if direction == "pub":
        file_utils.insert_in_file(
            task_source_path,
            f"    {func_name}({data_type}(0)); // TODO: (0) Replace with actual data",
            "// -- TASK LOOP EXTENSIONS --"
        )

    # For subscription, ensure function is called in loop
    if direction == "sub":
        file_utils.insert_in_file(task_source_path, f"    {func_name}();", "// -- TASK LOOP EXTENSIONS --")

    # Update README
    readme_updater.append_section(
        "## Tópicos",
        f"- `{topic_name}` ({direction}) añadido a `{task_name}` (tipo: `{data_type}`, frecuencia: `{rate}`ms)\n"
    )

    print(f"✅ Topic '{topic_name}' ({direction}) created for task '{task_name}'.")
