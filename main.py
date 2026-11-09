import flet as ft


def main(page: ft.Page):
    page.title = "PetChill"
    page.add(
        ft.Text("Hello! Welcome to PetChill.", size=24),
        ft.Text("Your study buddy is ready."),
        ft.Text("Tamagotchi Pacil Version")
    )


if __name__ == "__main__":
    ft.run(main)