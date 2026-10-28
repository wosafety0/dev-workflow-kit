import json
import unittest
from pathlib import Path

from scripts.harness_config import (
    ALLOWED_COMMAND_IDS,
    HarnessConfigError,
    validate_harness_config,
)


class HarnessConfigValidationTests(unittest.TestCase):
    def valid_config(self):
        return {
            "schema_version": 1,
            "project": "example-project",
            "commands": ["python-unittest", "semantic-review"],
        }

    def test_checked_in_example_config_is_valid(self):
        example = Path(__file__).resolve().parents[1] / "examples" / "harness-config.json"
        config = json.loads(example.read_text(encoding="utf-8"))
        self.assertEqual(validate_harness_config(config)["commands"], ["python-unittest"])

    def test_accepts_known_task_ids_offline(self):
        config = self.valid_config()
        self.assertEqual(validate_harness_config(config), config)

    def test_rejects_non_object(self):
        with self.assertRaisesRegex(HarnessConfigError, "JSON object"):
            validate_harness_config([])

    def test_rejects_missing_or_unknown_keys(self):
        config = self.valid_config()
        del config["project"]
        with self.assertRaisesRegex(HarnessConfigError, "exactly"):
            validate_harness_config(config)
        config = self.valid_config()
        config["extra"] = "value"
        with self.assertRaisesRegex(HarnessConfigError, "exactly"):
            validate_harness_config(config)

    def test_rejects_unknown_schema_version_and_boolean(self):
        for version in (2, True, "1"):
            config = self.valid_config()
            config["schema_version"] = version
            with self.subTest(version=version), self.assertRaisesRegex(
                HarnessConfigError, "Unsupported schema_version"
            ):
                validate_harness_config(config)

    def test_rejects_invalid_project_name(self):
        for name in ("", " ", " example ", None):
            config = self.valid_config()
            config["project"] = name
            with self.subTest(name=name), self.assertRaises(HarnessConfigError):
                validate_harness_config(config)

    def test_rejects_missing_or_empty_allowlist(self):
        for commands in ([], None, ""):
            config = self.valid_config()
            config["commands"] = commands
            with self.subTest(commands=commands), self.assertRaisesRegex(
                HarnessConfigError, "non-empty list"
            ):
                validate_harness_config(config)

    def test_rejects_unknown_task_ids_and_command_text(self):
        for command in ("custom-task", "python -c", "../script.py", "/bin/sh", "echo"):
            config = self.valid_config()
            config["commands"] = [command]
            with self.subTest(command=command), self.assertRaisesRegex(
                HarnessConfigError, "unknown command ID"
            ):
                validate_harness_config(config)

    def test_rejects_non_string_or_empty_task_ids(self):
        for commands in ([None], [1], [""], [True]):
            config = self.valid_config()
            config["commands"] = commands
            with self.subTest(commands=commands), self.assertRaises(HarnessConfigError):
                validate_harness_config(config)

    def test_rejects_duplicate_task_ids(self):
        config = self.valid_config()
        config["commands"] = ["python-unittest", "python-unittest"]
        with self.assertRaisesRegex(HarnessConfigError, "duplicate"):
            validate_harness_config(config)

    def test_allowlist_is_explicit_and_closed(self):
        self.assertEqual(ALLOWED_COMMAND_IDS, {"python-unittest", "semantic-review"})
        config = self.valid_config()
        config["commands"].append("arbitrary")
        with self.assertRaisesRegex(HarnessConfigError, "unknown command ID"):
            validate_harness_config(config)

    def test_validation_does_not_mutate_input(self):
        config = self.valid_config()
        original = list(config["commands"])
        result = validate_harness_config(config)
        result["commands"].append("changed")
        self.assertEqual(config["commands"], original)


if __name__ == "__main__":
    unittest.main()
