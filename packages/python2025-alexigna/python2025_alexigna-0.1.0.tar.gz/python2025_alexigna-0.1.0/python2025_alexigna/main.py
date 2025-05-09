import yaml


def dict_to_yaml(src: dict) -> str:
    return yaml.safe_dump(src)


if __name__ == "__main__":
    data = {
        "key1": "value1",
        "key2": {
            "sub-key1": "value",
            "sub-key2": "value",
        },
    }
    print(dict_to_yaml(data))
