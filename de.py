from simple_term_menu import TerminalMenu

# Définir les options
options = ["Option 1", "Option 2", "Option 3", "Quit"]

# Fonction de prévisualisation (callback)
def preview_message(option):
    messages = {
        "Option 1": "You are hovering over Option 1!",
        "Option 2": "You are hovering over Option 2!",
        "Option 3": "You are hovering over Option 3!",
        "Quit": "You are hovering over Quit!"
    }
    return messages.get(option, "No message available.")

# Créer le menu avec la prévisualisation
terminal_menu = TerminalMenu(
    options,
    preview_command=lambda selected_option: preview_message(selected_option),
    preview_size=1
)

# Afficher le menu
selected_index = terminal_menu.show()

# Vérifier la sélection finale
if selected_index is not None:
    print(f"You selected: {options[selected_index]}")
else:
    print("No option selected.")
