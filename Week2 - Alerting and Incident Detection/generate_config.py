import os

template_path = "Week2 - Alerting and Incident Detection/alertmanager/config.yml"
output_path = "Week2 - Alerting and Incident Detection/alertmanager/config.yml"

with open(template_path, "r") as f:
    config = f.read()

for key in ["EMAIL_USERNAME", "EMAIL_PASSWORD", "EMAIL_RECEIVER"]:
    value = os.environ.get(key, "")
    config = config.replace(f"${{{key}}}", value)

with open(output_path, "w") as f:
    f.write(config)
