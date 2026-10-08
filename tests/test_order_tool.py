"""Tests for get_order_status. They never call Gemini."""
from tools import get_order_status


def test_known_order():
    result = get_order_status("KE1002")
    assert "Shipped" in result
    assert "Prestige pressure cooker" in result
    assert "2026-10-07" in result
    assert "Credit card" in result


def test_lowercase_order_id():
    result = get_order_status("ke1005")
    assert "Processing" in result
    assert "2026-10-08" in result


def test_unknown_order_id():
    result = get_order_status("KE9999")
    assert "No order found" in result
    assert "KE9999" in result


def test_order_id_with_spaces():
    assert "Delivered" in get_order_status("  KE1001  ")


def test_cancelled_order_has_no_date():
    result = get_order_status("KE1007")
    assert "Cancelled" in result
    assert "not applicable" in result
