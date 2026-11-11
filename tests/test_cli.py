import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

from hexa.cli import parse


class CliTest(unittest.TestCase):
    def test_defaults_start_at_the_menu(self):
        settings, skip_menu, nation, seed = parse([])

        self.assertEqual(settings, {"mode": "campaign", "start": "sea", "goal": "survive", "map": "europe"})
        self.assertFalse(skip_menu)
        self.assertIsNone(nation)
        self.assertIsNone(seed)

    def test_each_explicit_mode_skips_the_menu(self):
        for mode in ("campaign", "conquest", "colony"):
            with self.subTest(mode=mode):
                settings, skip_menu, _, _ = parse(["--mode", mode])

                self.assertEqual(settings["mode"], mode)
                self.assertTrue(skip_menu)

    def test_map_start_and_goal_choices(self):
        for option, choices in (
            ("map", ("europe", "random")),
            ("start", ("sea", "land")),
            ("goal", ("survive", "independence", "endless")),
        ):
            for choice in choices:
                with self.subTest(option=option, choice=choice):
                    settings, skip_menu, _, _ = parse([f"--{option}", choice])

                    self.assertEqual(settings[option], choice)
                    self.assertFalse(skip_menu)

    def test_invalid_choice_exits_with_code_two(self):
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as error:
            parse(["--mode", "unknown"])

        self.assertEqual(error.exception.code, 2)

    def test_seed_is_an_integer(self):
        _, _, _, seed = parse(["--seed", "42"])

        self.assertIsInstance(seed, int)
        self.assertEqual(seed, 42)

    def test_nation_passes_through_unchanged(self):
        _, _, nation, _ = parse(["--nation", "por"])

        self.assertEqual(nation, "por")

    def test_importing_cli_does_not_import_pygame(self):
        code = (
            "import sys\n"
            "import hexa.cli\n"
            "if 'pygame' in sys.modules:\n"
            "    sys.exit('pygame was imported')\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
