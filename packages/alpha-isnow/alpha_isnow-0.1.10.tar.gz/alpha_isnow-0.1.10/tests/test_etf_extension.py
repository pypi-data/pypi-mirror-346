import unittest
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import pytest

from alpha.datasets import AssetType, load_daily, list_available_months

# Try to import external library, make test optional if not available
try:
    import pwb_toolbox.datasets as pwb_ds

    PWB_AVAILABLE = True
except ImportError:
    PWB_AVAILABLE = False

# Load environment variables for API access
load_dotenv()


class TestETFExtension(unittest.TestCase):
    """Test suite for ETF extension functionality"""

    @pytest.mark.skipif(not PWB_AVAILABLE, reason="pwb_toolbox not installed")
    def test_etf_extension_consistency(self):
        """Test that our ETF extension matches the external library's implementation"""
        symbols = ["SPY", "IEF", "GLD"]

        print("Loading PWB dataset...")
        df_pwb = pwb_ds.load_dataset("ETFs-Daily-Price", symbols, extend=True)

        print("Loading Alpha dataset...")
        df_alpha = load_daily(asset_type=AssetType.ETFs, symbols=symbols, extend=True)

        if "date" in df_pwb.columns and not isinstance(df_pwb.index, pd.DatetimeIndex):
            df_pwb["date"] = pd.to_datetime(df_pwb["date"])
            df_pwb = df_pwb.set_index("date")

        if "date" in df_alpha.columns and not isinstance(
            df_alpha.index, pd.DatetimeIndex
        ):
            df_alpha["date"] = pd.to_datetime(df_alpha["date"])
            df_alpha = df_alpha.set_index("date")

        common_cols = set(df_pwb.columns).intersection(set(df_alpha.columns))
        if "symbol" in common_cols:
            common_cols.remove("symbol")

        for symbol in symbols:
            print(f"Testing symbol: {symbol}")

            pwb_symbol_data = df_pwb[df_pwb["symbol"] == symbol].sort_index()
            alpha_symbol_data = df_alpha[df_alpha["symbol"] == symbol].sort_index()

            self.assertEqual(
                len(pwb_symbol_data),
                len(alpha_symbol_data),
                f"Date count mismatch for {symbol}",
            )

            common_dates = pwb_symbol_data.index.intersection(alpha_symbol_data.index)
            self.assertGreater(
                len(common_dates), 0, f"No common dates found for {symbol}"
            )

            sample_dates = [
                common_dates[0],
                common_dates[len(common_dates) // 2],
                common_dates[-1],
            ]

            for date in sample_dates:
                pwb_row = pwb_symbol_data.loc[date]
                alpha_row = alpha_symbol_data.loc[date]

                for col in common_cols:
                    pwb_val = pwb_row[col]
                    alpha_val = alpha_row[col]

                    if pd.isna(pwb_val) or pd.isna(alpha_val):
                        continue

                    self.assertTrue(
                        np.isclose(pwb_val, alpha_val, rtol=1e-5, atol=1e-8),
                        f"Value mismatch for {symbol} on {date} in column {col}: "
                        f"PWB={pwb_val}, Alpha={alpha_val}",
                    )

    def test_etf_extension_internal_consistency(self):
        """Test internal consistency of ETF extension with different parameters"""
        symbols = ["SPY", "IEF", "GLD"]

        df_full = load_daily(asset_type=AssetType.ETFs, symbols=symbols, extend=True)

        available_months = list_available_months(AssetType.ETFs)

        start_idx = len(available_months) // 4
        end_idx = 3 * len(available_months) // 4
        month_range = (available_months[start_idx], available_months[end_idx])

        df_restricted = load_daily(
            asset_type=AssetType.ETFs,
            symbols=symbols,
            month_range=month_range,
            extend=True,
        )

        if "date" in df_full.columns:
            df_full["date"] = pd.to_datetime(df_full["date"])

        if "date" in df_restricted.columns:
            df_restricted["date"] = pd.to_datetime(df_restricted["date"])

        self.assertLessEqual(
            df_restricted["date"].min(),
            df_full["date"].max(),
            "Restricted dataset's start date should be within full dataset's range",
        )

        self.assertGreaterEqual(
            df_restricted["date"].max(),
            df_full["date"].min(),
            "Restricted dataset's end date should be within full dataset's range",
        )

        for symbol in symbols:
            full_symbol_data = df_full[df_full["symbol"] == symbol].copy()
            restricted_symbol_data = df_restricted[
                df_restricted["symbol"] == symbol
            ].copy()

            full_symbol_data.set_index("date", inplace=True)
            restricted_symbol_data.set_index("date", inplace=True)

            common_dates = full_symbol_data.index.intersection(
                restricted_symbol_data.index
            )

            self.assertGreater(
                len(common_dates),
                0,
                f"No common dates for {symbol} between full and restricted datasets",
            )

            for date in common_dates:
                full_row = full_symbol_data.loc[date]
                restricted_row = restricted_symbol_data.loc[date]

                for col in ["open", "high", "low", "close"]:
                    full_val = full_row[col]
                    restricted_val = restricted_row[col]

                    if pd.isna(full_val) or pd.isna(restricted_val):
                        continue

                    self.assertEqual(
                        full_val,
                        restricted_val,
                        f"Value mismatch for {symbol} on {date} in column {col}",
                    )

    def test_comprehensive_etf_comparison(self):
        """A comprehensive test that simulates the analysis script provided"""
        if not PWB_AVAILABLE:
            self.skipTest("pwb_toolbox not installed")

        symbols = ["SPY", "IEF", "GLD"]

        df_pwb = pwb_ds.load_dataset("ETFs-Daily-Price", symbols, extend=True)
        df_alpha = load_daily(asset_type=AssetType.ETFs, symbols=symbols, extend=True)

        if "date" in df_pwb.columns and not isinstance(df_pwb.index, pd.DatetimeIndex):
            df_pwb["date"] = pd.to_datetime(df_pwb["date"])
            df_pwb = df_pwb.set_index("date")

        if "date" in df_alpha.columns and not isinstance(
            df_alpha.index, pd.DatetimeIndex
        ):
            df_alpha["date"] = pd.to_datetime(df_alpha["date"])
            df_alpha = df_alpha.set_index("date")

        common_cols = set(df_pwb.columns).intersection(set(df_alpha.columns))
        if "symbol" in common_cols:
            common_cols.remove("symbol")

        total_date_discrepancies = 0
        total_value_discrepancies = 0

        for symbol in symbols:
            pwb_symbol_data = df_pwb[df_pwb["symbol"] == symbol].copy()
            alpha_symbol_data = df_alpha[df_alpha["symbol"] == symbol].copy()

            pwb_dates = set(pwb_symbol_data.index)
            alpha_dates = set(alpha_symbol_data.index)

            missing_in_alpha = pwb_dates - alpha_dates
            total_date_discrepancies += len(missing_in_alpha)
            self.assertEqual(
                len(missing_in_alpha),
                0,
                f"Found {len(missing_in_alpha)} dates in PWB but not in Alpha for {symbol}",
            )

            missing_in_pwb = alpha_dates - pwb_dates
            total_date_discrepancies += len(missing_in_pwb)
            self.assertEqual(
                len(missing_in_pwb),
                0,
                f"Found {len(missing_in_pwb)} dates in Alpha but not in PWB for {symbol}",
            )

            common_dates = pwb_dates.intersection(alpha_dates)

            for date in sorted(common_dates):
                pwb_row = pwb_symbol_data.loc[date]
                alpha_row = alpha_symbol_data.loc[date]

                for col in common_cols:
                    pwb_val = pwb_row[col]
                    alpha_val = alpha_row[col]

                    if pd.isna(pwb_val) or pd.isna(alpha_val):
                        continue

                    if not np.isclose(pwb_val, alpha_val, rtol=1e-5, atol=1e-8):
                        total_value_discrepancies += 1
                        self.fail(
                            f"Value mismatch for {symbol} on {date} in column {col}: "
                            f"PWB={pwb_val}, Alpha={alpha_val}"
                        )

        self.assertEqual(
            total_date_discrepancies,
            0,
            f"Found {total_date_discrepancies} date discrepancies",
        )
        self.assertEqual(
            total_value_discrepancies,
            0,
            f"Found {total_value_discrepancies} value discrepancies",
        )


if __name__ == "__main__":
    unittest.main()
