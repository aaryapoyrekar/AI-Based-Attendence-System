import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database import db


class DatabaseFallbackTests(unittest.TestCase):
    def test_get_all_students_returns_empty_when_supabase_unavailable(self):
        with patch.object(db, "supabase", None):
            self.assertEqual(db.get_all_students(), [])

    def test_check_teacher_exists_returns_false_when_supabase_unavailable(self):
        with patch.object(db, "supabase", None):
            self.assertFalse(db.check_teacher_exists("teacher"))


if __name__ == "__main__":
    unittest.main()
