from datetime import datetime

REST_THRESHOLD_MINUTES = 50  # untuk video demo nanti diubah sementara jadi 1 dulu
MAX_SESSION_HOURS = 4  # batas satu sesi jika user lupa istirahat, lewat dari ini sesi berhenti otomatis
MAX_SESSION_SECONDS = MAX_SESSION_HOURS * 3600

DEFAULT_FOCUS = {"accumulated_seconds": 0, "is_running": False, "started_at": None}


def _focus(data):
    """Mengambil bagian fokus dari data, dan melengkapi kunci yang hilang."""
    focus = data.setdefault("focus", {})
    for key, value in DEFAULT_FOCUS.items():
        focus.setdefault(key, value)
    return focus


def _elapsed_seconds(data, now):
    """Durasi sesi yang sedang berjalan (detik, tidak negatif). Rusak -> 0."""
    focus = _focus(data)
    if not focus["is_running"] or focus["started_at"] is None:
        return 0
    try:
        started_at = datetime.fromisoformat(focus["started_at"])
        elapsed = max (0, int((now - started_at).total_seconds()))
        return min(elapsed, MAX_SESSION_SECONDS)
    except (ValueError, TypeError):
        return 0


def start_focus(data, now):
    """Memulai sesi fokus. Jika sudah berjalan, started_at tidak direset."""
    focus = _focus(data)
    if not focus["is_running"]:
        focus["is_running"] = True
        focus["started_at"] = now.isoformat()
    return data


def end_focus(data, now):
    """Mengakhiri sesi dan menambahkan durasinya ke accumulated_seconds."""
    focus = _focus(data)
    if focus["is_running"]:
        focus["accumulated_seconds"] += _elapsed_seconds(data, now)
        focus["is_running"] = False
        focus["started_at"] = None
    return data

def end_if_too_long(data, now):
    """Mengakhiri sesi otomatis jika sudah mencapai batas maksimum.
    Mengembalikan True jika sesi baru saja dihentikan."""
    focus = _focus(data)
    if focus["is_running"] and _elapsed_seconds(data, now) >= MAX_SESSION_SECONDS:
        end_focus(data, now)
        return True
    return False


def get_focus_seconds(data, now):
    """Total detik fokus sejak istirahat terakhir (tersimpan + sesi berjalan)."""
    focus = _focus(data)
    return max(0, int(focus["accumulated_seconds"] + _elapsed_seconds(data, now)))


def is_rest_required(data, now, threshold_minutes=REST_THRESHOLD_MINUTES):
    """True jika total fokus sudah mencapai ambang istirahat."""
    return get_focus_seconds(data, now) >= threshold_minutes * 60


def record_break(data, now):
    """Mencatat istirahat: akumulasi jadi 0; sesi yang berjalan dimulai ulang dari now."""
    focus = _focus(data)
    focus["accumulated_seconds"] = 0
    if focus["is_running"]:
        focus["started_at"] = now.isoformat()
    return data


def reset_focus_on_launch(data):
    """Dipanggil saat aplikasi dibuka: sesi sebelumnya dianggap selesai."""
    data["focus"] = dict(DEFAULT_FOCUS)
    return data