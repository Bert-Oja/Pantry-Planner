import os
import inquirer


def prompt_openai_model():
    models = [
        "gpt-4-1106-preview",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-3.5-turbo-16k",
    ]  # List of models
    return inquirer.prompt(
        [
            inquirer.List(
                "model",
                message="Choose your OpenAI model",
                default="gpt-4-1106-preview",
                choices=models,
            )
        ]
    )["model"]


def write_env_file(config):
    with open(".env", "w") as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")


def main():
    # Check if .env file exists
    env_exists = os.path.isfile(".env")

    if env_exists:
        use_existing = inquirer.prompt(
            [
                inquirer.Confirm(
                    "use_existing",
                    message="An existing .env file was found. Do you want to use it?",
                )
            ]
        )["use_existing"]

        if use_existing:
            print("Using existing .env file.")
            return

    # Prompt for OpenAI API Key
    openai_api_key = inquirer.prompt(
        [
            inquirer.Text(
                "openai_api_key",
                message="Enter your OpenAI API key",
                validate=lambda _, x: x.strip() != "",
            )
        ]
    )["openai_api_key"]

    # Prompt for OpenAI Model
    openai_model = prompt_openai_model()

    # Prompt for other configurations
    ourgroceries_username = inquirer.prompt(
        [
            inquirer.Text(
                "ourgroceries_username",
                message="Enter your OurGroceries username",
                validate=lambda _, x: x.strip() != "",
            )
        ]
    )["ourgroceries_username"]

    ourgroceries_password = inquirer.prompt(
        [
            inquirer.Password(
                "ourgroceries_password", message="Enter your OurGroceries password"
            )
        ]
    )["ourgroceries_password"]

    simplenote_username = inquirer.prompt(
        [
            inquirer.Text(
                "simplenote_username",
                message="Enter your Simplenote username",
                validate=lambda _, x: x.strip() != "",
            )
        ]
    )["simplenote_username"]

    simplenote_password = inquirer.prompt(
        [
            inquirer.Password(
                "simplenote_password", message="Enter your Simplenote password"
            )
        ]
    )["simplenote_password"]

    # Write to .env file
    config = {
        "OPENAI_API_KEY": openai_api_key,
        "OPENAI_MODEL": openai_model,
        "OURGROCERIES_USERNAME": ourgroceries_username,
        "OURGROCERIES_PASSWORD": ourgroceries_password,
        "SIMPLENOTE_USERNAME": simplenote_username,
        "SIMPLENOTE_PASSWORD": simplenote_password,
    }
    write_env_file(config)

    print("Configuration complete. .env file created.")


if __name__ == "__main__":
    main()
