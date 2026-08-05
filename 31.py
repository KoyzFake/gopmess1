import yt_dlp
import time
import os
import re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live

# ==========================================
# SYSTEM CORE SETUP
# ==========================================
console = Console()

class CyberInterface:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def matrix_effect():
        """Hiệu ứng ma trận khởi động siêu tối tân"""
        CyberInterface.clear()
        matrix_text = "0101101001011010010101010110101010"
        with Live(console=console, screen=False) as live:
            for i in range(15):
                color = "green" if i % 2 == 0 else "bright_green"
                live.update(Text(f"INITIALIZING SYSTEM... {matrix_text[:i*2]}", style=color))
                time.sleep(0.08)
        time.sleep(0.5)

    @staticmethod
    def header():
        CyberInterface.clear()
        header_text = Text()
        header_text.append("⚡ TIENDAT SECURITY OPERATING SYSTEM 2026 ⚡\n", style="bold cyan")
        header_text.append(" [ STATUS: MILITARY GRADE SHIELD ON ] ", style="bold red blink")
        
        console.print(Panel(
            header_text, 
            border_style="bright_blue", 
            subtitle="[ v3.1.0-ULTIMATE ]",
            subtitle_align="right",
            padding=(1, 5)
        ))

    @staticmethod
    def menu():
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_row("[bold yellow][1][/bold yellow]", "📡 [bold cyan]DEEP SCAN[/bold cyan] (Quét sâu dữ liệu)")
        menu_table.add_row("[bold yellow][2][/bold yellow]", "🚀 [bold green]BUFF VIEW[/bold green] (Coming Soon)")
        menu_table.add_row("[bold yellow][3][/bold yellow]", "❤️  [bold magenta]BUFF LIKE[/bold magenta] (Coming Soon)")
        menu_table.add_row("[bold yellow][0][/bold yellow]", "❌ [bold red]SHUTDOWN[/bold red] (Ngắt kết nối)")
        
        console.print(Panel(menu_table, title="[bold white]🚀 COMMAND CENTER[/bold white]", border_style="bright_yellow"))

    @staticmethod
    def loading_effect(task_name):
        # Đã FIX: Bỏ tham số gradient gây lỗi
        with Progress(
            SpinnerColumn(spinner_name="aesthetic"),
            TextColumn("[bold yellow]{task.description}"),
            BarColumn(bar_width=35, complete_style="cyan", finished_style="bright_green"),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"{task_name}...", total=100)
            while not progress.finished:
                time.sleep(0.015)
                progress.update(task, advance=2.5)

class CoreProcessor:
    @staticmethod
    def scan_video(url):
        ydl_opts = {'quiet': True, 'no_warnings': True, 'nocheckcertificate': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'N/A'),
                    'views': info.get('view_count', 0),
                    'likes': info.get('like_count', 0),
                    'duration': time.strftime('%H:%M:%S', time.gmtime(info.get('duration', 0))),
                    'channel': info.get('uploader', 'N/A'),
                    'subs': info.get('channel_follower_count', 0),
                }
        except: return None

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    CyberInterface.matrix_effect()
    while True:
        CyberInterface.header()
        CyberInterface.menu()
        
        choice = console.input("[bold white]❯ Nhập mã lệnh (0-3): [/bold white]")

        if choice == "1":
            url = console.input("\n[bold cyan]🔗 Dán liên kết mục tiêu: [/bold cyan]")
            CyberInterface.loading_effect("ĐANG THÂM NHẬP GIAO THỨC YOUTUBE")
            
            data = CoreProcessor.scan_video(url)
            if data:
                res_table = Table(show_header=True, header_style="bold white", border_style="bright_green")
                res_table.add_column("PHÂN LỚP DỮ LIỆU", style="cyan", width=20)
                res_table.add_column("GIÁ TRỊ GIẢI MÃ", style="bold white")
                
                res_table.add_row("Tiêu đề", data['title'])
                res_table.add_row("Lượt xem", f"[bold yellow]{data['views']:,}[/bold yellow]")
                res_table.add_row("Lượt thích", f"[bold magenta]{data['likes']:,}[/bold magenta]")
                res_table.add_row("Thời lượng", data['duration'])
                res_table.add_row("Chủ kênh", data['channel'])
                res_table.add_row("Subscriber", f"{data['subs']:,}")
                res_table.add_row("Trạng thái", "[bold green]DỮ LIỆU SẠCH[/bold green]")
                
                console.print("\n", res_table)
            else:
                console.print(Panel("[bold red]❌ LỖI TRUY CẬP: Mục tiêu không tồn tại hoặc đã bị ẩn![/bold red]", border_style="red"))
            
            console.input("\n[italic dim]Nhấn Enter để quay lại trung tâm điều khiển...[/italic dim]")

        elif choice in ["2", "3"]:
            CyberInterface.loading_effect("ĐANG KẾT NỐI SERVER PROXY QUÂN SỰ")
            console.print(Panel("[bold red]ACCESS DENIED![/bold red]\n[white]Tính năng đang được mã hóa. Vui lòng đợi bản cập nhật v4.0.[/white]", border_style="bright_magenta"))
            time.sleep(2.5)

        elif choice == "0":
            console.print("[bold red]Đang hủy lệnh... Xóa nhật ký truy cập... Tạm biệt.[/bold red]")
            time.sleep(1)
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[bold red]HỆ THỐNG CRASH: {e}[/bold red]")
