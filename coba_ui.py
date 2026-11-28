import asyncio
import os
from datetime import datetime

import flet as ft

import focus
import pet

# ===== warna (nanti dipindah ke theme.py) =====
BG = "#151A1A"
SURFACE = "#1F2626"
BORDER = "#2C3636"
SAGE = "#8FB59B"
SAGE_DARK = "#3C5046"
LIME = "#C9E265"
TEXT = "#F4F1EA"
MUTED = "#8E9A98"

PET_SIZE = 432  # sama dengan ukuran GIF, supaya piksel tetap tajam

STATE_LABELS = {"idle": "Idle", "listening": "Listening", "happy": "Happy", "rest": "Rest"}
STATE_MESSAGES = {
    "idle": "Tugas DDP jatuh tempo besok.",  # contoh, nanti dari data tugas
    "listening": "Aku dengerin. Tulis pelan-pelan saja.",
    "happy": "Satu tugas selesai. Pelan tapi pasti.",
    "rest": "Sudah cukup lama fokus. Mau jeda sebentar? "
            "Minum air, istirahatkan mata, atau regangkan badan.",
}


def image_for_state(state):
    """Nama file GIF untuk state. Sementara: kalau file-nya belum ada, pakai idle."""
    name = pet.get_pet_image(state)
    if os.path.exists(os.path.join("assets", name)):
        return name
    return pet.get_pet_image("idle")


def main(page: ft.Page):
    page.title = "PetChill"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO

    data = focus.reset_focus_on_launch({})  # sesi lama dianggap selesai
    ui_state = {"is_journaling": False, "task_completed_at": None}

    # ---------- komponen ----------
    bubble_text = ft.Text(STATE_MESSAGES["idle"], size=14, color=BG,
                          text_align=ft.TextAlign.CENTER)
    bubble = ft.Container(
        content=bubble_text, bgcolor=TEXT, border_radius=20, width=420,
        padding=ft.Padding.only(left=20, right=20, top=12, bottom=12),
    )

    glow = ft.Container(
        width=300, height=300, border_radius=150, left=66, top=60,
        bgcolor=ft.Colors.with_opacity(0.12, SAGE),
        shadow=ft.BoxShadow(blur_radius=90, spread_radius=10,
                            color=ft.Colors.with_opacity(0.35, SAGE)),
    )
    platform = ft.Container(
        width=300, height=44, border_radius=22, bgcolor=SAGE_DARK,
        left=66, top=PET_SIZE - 100,
    )
    pet_image = ft.Image(src=image_for_state("idle"), width=PET_SIZE,
                         height=PET_SIZE, fit=ft.BoxFit.CONTAIN)
    pet_click = ft.Container(content=pet_image, left=0, top=0)
    pet_stage = ft.Stack(width=PET_SIZE, height=PET_SIZE,
                         controls=[glow, platform, pet_click])

    chip_text = ft.Text("Idle", size=12, color=TEXT)
    chip = ft.Container(
        content=chip_text, bgcolor=SURFACE, border_radius=14,
        border=ft.Border.all(1, BORDER),
        padding=ft.Padding.only(left=14, right=14, top=4, bottom=4),
    )
    hint = ft.Text("Ketuk pet untuk membuka menu", size=12, color=MUTED)

    timer_text = ft.Text("00:00", size=28, weight=ft.FontWeight.BOLD, color=TEXT)
    start_btn = ft.Button("Mulai fokus", style=ft.ButtonStyle(bgcolor=LIME, color=BG))
    end_btn = ft.OutlinedButton("Akhiri fokus", style=ft.ButtonStyle(color=TEXT))
    break_btn = ft.Button("Saya sudah istirahat", visible=False,
                          style=ft.ButtonStyle(bgcolor=SAGE, color=BG))
    focus_pill = ft.Container(
        bgcolor=SURFACE, border_radius=32, border=ft.Border.all(1, BORDER),
        padding=ft.Padding.only(left=24, right=16, top=10, bottom=10),
        content=ft.Row(
            [ft.Column([ft.Text("Waktu fokus", size=11, color=MUTED), timer_text],
                       spacing=0), start_btn, end_btn],
            spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    def dock_item(icon, label, on_click):
        return ft.Column(
            [ft.Container(content=ft.Icon(icon, color=BG, size=26), width=56,
                          height=56, border_radius=28, bgcolor=LIME,
                          alignment=ft.Alignment.CENTER, on_click=on_click),
             ft.Text(label, size=12, color=MUTED)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6)

    # ---------- logika tampilan ----------
    def refresh():
        now = datetime.now()
        seconds = focus.get_focus_seconds(data, now)
        timer_text.value = "%02d:%02d" % (seconds // 60, seconds % 60)
        state = pet.resolve_pet_state(data, ui_state, now)
        pet_image.src = image_for_state(state)
        chip_text.value = STATE_LABELS[state]
        bubble_text.value = STATE_MESSAGES[state]
        break_btn.visible = state == "rest"
        page.update()

    def on_start(e):
        focus.start_focus(data, datetime.now())
        refresh()

    def on_end(e):
        focus.end_focus(data, datetime.now())
        refresh()

    def on_break(e):
        focus.record_break(data, datetime.now())
        refresh()

    def toggle_dock(e):
        dock.visible = not dock.visible
        page.update()

    def on_tasks(e):  # tombol UJI: anggap tugas baru selesai -> pet happy 4 detik
        ui_state["task_completed_at"] = datetime.now()
        refresh()

    def on_mood(e):
        hint.value = "Panel Mood belum dibuat"
        page.update()

    def on_journal(e):  # tombol UJI: aktifkan/matikan listening
        ui_state["is_journaling"] = not ui_state["is_journaling"]
        refresh()

    start_btn.on_click = on_start
    end_btn.on_click = on_end
    break_btn.on_click = on_break
    pet_click.on_click = toggle_dock

    dock = ft.Row(
        [dock_item(ft.Icons.CHECKLIST, "Tugas", on_tasks),
         dock_item(ft.Icons.MOOD, "Mood", on_mood),
         dock_item(ft.Icons.EDIT_NOTE, "Jurnal", on_journal)],
        alignment=ft.MainAxisAlignment.CENTER, spacing=28, visible=False)

    # ---------- susunan halaman ----------
    page.add(
        ft.Container(
            alignment=ft.Alignment.CENTER_LEFT,
            content=ft.Column([
                ft.Text("Pelan-pelan saja.", size=32,
                        weight=ft.FontWeight.BOLD, color=TEXT),
                ft.Text("Istirahat juga bagian dari rencana.", size=14, color=MUTED),
            ], spacing=2)),
        ft.Container(
            alignment=ft.Alignment.TOP_CENTER,
            content=ft.Column(
                [bubble, pet_stage, chip, hint, focus_pill, break_btn, dock],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14)),
    )
    refresh()
    page.run_task(tick_factory(refresh))


def tick_factory(refresh):
    async def tick():
        while True:
            await asyncio.sleep(1)
            refresh()
    return tick


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")