"""Logika sesi fokus murni (tanpa flet, tanpa baca/tulis file)."""

from datetime import datetime

REST_THRESHOLD_MINUTES = 50


def _elapsed_seconds(data, now):
    """Hitung durasi sesi yang sedang berjalan dalam detik (tidak negatif)."""
    focus = data["focus"]
    if not focus.get("is_running") or focus.get("started_at") is None:
        return 0
    started_at = datetime.fromisoformat(focus["started_at"])
    return max(0, int((now - started_at).total_seconds()))


def start_focus(data, now):
    """Mulai sesi fokus; bila sesi sudah berjalan, started_at tidak direset."""
    focus = data["focus"]
    if not focus.get("is_running"):
        focus["is_running"] = True
        focus["started_at"] = now.isoformat()
    return data


def end_focus(data, now):
    """Akhiri sesi fokus, tambahkan durasinya ke accumulated_seconds."""
    focus = data["focus"]
    if focus.get("is_running"):
        focus["accumulated_seconds"] += _elapsed_seconds(data, now)
        focus["is_running"] = False
        focus["started_at"] = None
    return data


def get_focus_seconds(data, now):
    """Kembalikan total detik fokus (tersimpan + sesi berjalan), int dan tidak negatif."""
    focus = data["focus"]
    total = focus.get("accumulated_seconds", 0) + _elapsed_seconds(data, now)
    return max(0, int(total))


def is_rest_required(data, now, threshold_minutes):
    """True bila total detik fokus sudah mencapai ambang istirahat."""
    return get_focus_seconds(data, now) >= threshold_minutes * 60


def record_break(data, now):
    """Catat istirahat: reset accumulated_seconds dan restart sesi berjalan dari now."""
    focus = data["focus"]
    focus["accumulated_seconds"] = 0
    if focus.get("is_running"):
        focus["started_at"] = now.isoformat()
    return data
