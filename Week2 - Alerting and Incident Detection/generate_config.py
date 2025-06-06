import os

print("Current working directory:", os.getcwd())

template_path = "./alertmanager/config.yml"
output_path = "./alertmanager/config.yml"

with open(template_path, "r") as f:
    config = f.read()

for key in ["EMAIL_USERNAME", "EMAIL_PASSWORD", "EMAIL_RECEIVER"]:
    value = os.environ.get(key, "")
    print(f"Replacing ${key} with {value}")
    config = config.replace(f"${{{key}}}", value)

with open(output_path, "w") as f:
    print("Writing into the output file")
    f.write(config)
