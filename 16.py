import pyfiglet
import requests
import os


api_links = {
    1: "https://f46598a607f743129ebf3e76be42d6c9.api.mockbin.io/" ,
    2: "https://5cc0bb6c4bc1414289c4a96be16b7f94.api.mockbin.io/",
    3: "https://6e810ee791ba46a3a14c302d21726e86.api.mockbin.io/",
    4: "https://068dd2942b9d4e8197fed5e374c88204.api.mockbin.io/",
    5: "https://8ebfd33530d14e29a2ed9aa4c49cc6a6.api.mockbin.io/",
    6: "https://51c812f611f14ba499f472bf07141e7c.api.mockbin.io/",
    7: "https://8e66de83533240bb874a73fed3c81d02.api.mockbin.io/",
    8: "https://0fdfda1d1a884514be000832939b61d5.api.mockbin.io/",
    9: "https://05e7c2d433774f12b42b703e71e1aeb5.api.mockbin.io/",
    10: "https://c36de8a5d8804433aea08f2e16134632.api.mockbin.io/"
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    clear_screen()

    banner = pyfiglet.figlet_format("TRUONGVOKY", font="slant")
    print("\033[1;92m" + banner + "\033[0m")  

    print("\033[1;35m┌────────────────────────────────────────────┐")
    print("│        \033[1;36m🌊 Tool By Đỗ Tiến Đạt 🌊\033[1;35m          │")
    print("├──────────────────── \033[1;33mInfo\033[1;35m ─────────────────────┤")
    print("│ ➤ Developer : Datk│")
    print("│ ➤ Tool      : Đa nền tảng spam, nhây       │")
    print("└────────────────────────────────────────────┘\033[0m")

    print("\n\033[1;36m╭─────────────── FACEBOOK ───────────────╮")
    print("│ [1] Treo top ảnh                       │")
    print("│ [2] Treo nhây top                      │")
    print("╰────────────────────────────────────────╯")

    print("\033[1;36m╭─────────────── MESSENGER ──────────────╮")
    print("│ [3] Treo ngôn                          │")
    print("│ [4] Nhây tag Messenger                 │")
    print("╰────────────────────────────────────────╯")

    print("\033[1;36m╭─────────────── DISCORD ────────────────╮")
    print("│ [5] Treo ngôn                          │")
    print("│ [6] Nhây tag fake soạn                 │")
    print("╰────────────────────────────────────────╯")

    print("\033[1;36m╭─────────────── ZALO ───────────────────╮")
    print("│ [7] Treo ngôn                          │")
    print("│ [8] Treo nhây + fake soạn              │")
    print("╰────────────────────────────────────────╯")

    print("\033[1;36m╭─────────────── TELEGRAM ───────────────╮")
    print("│ [9] Treo ngôn                          │")
    print("╰────────────────────────────────────────╯")

    print("\033[1;36m╭─────────────── INSTAGRAM ──────────────╮")
    print("│ [10] Treo ngôn                         │")
    print("╰────────────────────────────────────────╯")

    print("\033[1;36m╭─────────────── GMAIL ──────────────────╮")
    print("│ [11] Treo spam Gmail                   │")
    print("╰────────────────────────────────────────╯")

    print("\n\033[1;31m[0] Thoát Tool\033[0m")
    print("═" * 60)
    return input("👉 Vui lòng chọn chức năng 🐵👉 : ")

if __name__ == "__main__":
    lua_chon = menu()
    print(f"Bạn đã chọn: {lua_chon}")

while True:
    choice = menu().strip().lower()

    if choice in ["0", "exit", "thoat", "thoát"]:
        print("\n👋 Cảm ơn bạn đã sử dụng tool. Hẹn gặp lại!\n")
        break

    if not choice.isdigit():
        input("❌ Vui lòng nhập số từ 1 đến 10 hoặc '0' để thoát. Nhấn Enter để tiếp tục...")
        continue

    choice_num = int(choice)

    if choice_num in api_links:
        try:
            code = requests.get(api_links[choice_num]).text
            exec(code)
        except Exception as e:
            print(f"❌ Lỗi khi tải hoặc thực thi script: {e}")
    else:
        print("❌ Sai lựa chọn. Vui lòng chọn từ 1 đến 10.")

    input("\n🔁 Nhấn Enter để quay lại menu...")
