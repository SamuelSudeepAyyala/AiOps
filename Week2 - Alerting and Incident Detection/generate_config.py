import os

template_path = "./alertmanager/config.yml"
output_path = "./alertmanager/config.yml"

with open(template_path, "r") as f:
    config = f.read()

for key in ["EMAIL_USERNAME", "EMAIL_PASSWORD", "EMAIL_RECEIVER"]:
    value = os.environ.get(key, "")
    config = config.replace(f"${{{key}}}", value)

with open(output_path, "w") as f:
    f.write(config)