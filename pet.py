import focus

HAPPY_DURATION_SECONDS = 4  # lama pet senang setelah tugas selesai

PET_IMAGES = { #nama file nanti diganti
    "idle": "pet_idle.gif",
    "listening": "pet_listening.gif",
    "happy": "pet_happy.gif",
    "rest": "pet_rest.gif",
}


def get_pet_state(rest_required, is_journaling, task_just_completed):
    """FSM pet: satu state pada satu waktu. Prioritas: rest > listening > happy > idle."""
    if rest_required:
        return "rest"
    if is_journaling:
        return "listening"
    if task_just_completed:
        return "happy"
    return "idle"


def is_happy_active(completed_at, now, duration_seconds=HAPPY_DURATION_SECONDS):
    """True jika tugas baru saja selesai (kurang dari duration_seconds yang lalu)."""
    if completed_at is None:
        return False
    elapsed = (now - completed_at).total_seconds()
    return 0 <= elapsed < duration_seconds


def resolve_pet_state(data, ui_state, now):
    """Menentukan state pet dari data fokus dan sinyal UI sementara."""
    rest_required = focus.is_rest_required(data, now)
    is_journaling = bool(ui_state.get("is_journaling", False))
    task_just_completed = is_happy_active(ui_state.get("task_completed_at"), now)
    return get_pet_state(rest_required, is_journaling, task_just_completed)


def get_pet_image(state):
    """Nama file gambar untuk state tertentu. State tak dikenal -> idle."""
    return PET_IMAGES.get(state, PET_IMAGES["idle"])