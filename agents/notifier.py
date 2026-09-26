import subprocess
import os

class NotificationAgent:
    """
    Agent Thông báo: Gửi thông báo trực tiếp lên màn hình macOS (Notification Banner + Âm thanh)
    kèm mở nhanh file video để người dùng duyệt.
    """
    def notify_user_for_review(self, video_title, video_path):
        sound_name = "Glass" # Âm thanh thông báo sang trọng của Mac
        app_name = "Lido AI Lab Production"
        msg = f"Đã có video mới: '{video_title[:45]}...' - Bấm để xem và duyệt đăng!"
        
        # AppleScript gửi native notification trên macOS
        applescript = f'''
        display notification "{msg}" with title "{app_name}" sound name "{sound_name}"
        '''
        subprocess.run(["osascript", "-e", applescript], check=False)
        print(f"\n🔔 [NotificationAgent] ĐÃ GỬI THÔNG BÁO MACOS ĐẾN BẠN!")
        print(f"👉 Mở xem nhanh video tại: file://{video_path}")

if __name__ == "__main__":
    notifier = NotificationAgent()
    notifier.notify_user_for_review("AI Gemini hack 3 công ty", "/dummy/path.mp4")
