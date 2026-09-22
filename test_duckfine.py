import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_initializes_member_id_and_owed_total(self):
        fine = DuckFine("member-42")

        self.assertEqual(fine.member_id, "member-42")
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_rejects_negative_days_late(self):
        fine = DuckFine("member-42")

        with self.assertRaisesRegex(ValueError, "days_late must not be negative"):
            fine.charge(-1)

    def test_charge_ignores_the_grace_period(self):
        fine = DuckFine("member-42")

        fee = fine.charge(2)

        self.assertEqual(fee, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_applies_daily_fee_for_chargeable_days(self):
        fine = DuckFine("member-42")

        fee = fine.charge(5)

        self.assertEqual(fee, 1.5)
        self.assertEqual(fine.total_owed, 1.5)

    def test_charge_doubles_fee_when_deluxe_is_true(self):
        fine = DuckFine("member-42")

        fee = fine.charge(5, deluxe=True)

        self.assertEqual(fee, 3.0)
        self.assertEqual(fine.total_owed, 3.0)

    def test_charge_is_capped_at_max_fee(self):
        fine = DuckFine("member-42")

        fee = fine.charge(20, deluxe=True)

        self.assertEqual(fee, 5.0)
        self.assertEqual(fine.total_owed, 5.0)


if __name__ == "__main__":
    unittest.main()
