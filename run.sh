#!/usr/bin/env bash
# ==============================================================================
# LIDO AI LAB - BỘ ĐIỀU KHIỂN & BÁO CÁO 2 BIỆT ĐỘI AI (@LidoAILab)
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHON="$DIR/venv/bin/python3"
PID_VN="$DIR/.squad_vn.pid"
PID_GLOBAL="$DIR/.squad_global.pid"
LOG_VN="$DIR/squad_vn.log"
LOG_GLOBAL="$DIR/squad_global.log"

case "$1" in
  start)
    echo "🚀 [LIDO AI LAB] Đang khởi chạy 2 biệt đội chạy ngầm..."
    
    # 1. Chạy Squad VN
    if [ -f "$PID_VN" ] && kill -0 $(cat "$PID_VN") 2>/dev/null; then
      echo "ℹ️  Biệt đội VN đang chạy (PID: $(cat "$PID_VN"))"
    else
      nohup "$PYTHON" "$DIR/squad_vn_scheduler.py" > "$LOG_VN" 2>&1 &
      echo $! > "$PID_VN"
      echo "✅ Đã bật Biệt Đội Tiếng Việt (PID: $(cat "$PID_VN") | Log: squad_vn.log)"
    fi

    # 2. Chạy Squad Global
    if [ -f "$PID_GLOBAL" ] && kill -0 $(cat "$PID_GLOBAL") 2>/dev/null; then
      echo "ℹ️  Biệt đội Toàn cầu đang chạy (PID: $(cat "$PID_GLOBAL"))"
    else
      nohup "$PYTHON" "$DIR/squad_global_scheduler.py" > "$LOG_GLOBAL" 2>&1 &
      echo $! > "$PID_GLOBAL"
      echo "✅ Đã bật Biệt Đội Toàn Cầu (PID: $(cat "$PID_GLOBAL") | Log: squad_global.log)"
    fi
    echo ""
    echo "💡 Dùng './run.sh status' để kiểm tra trạng thái."
    echo "💡 Dùng './run.sh report' để xem báo cáo các video đã đăng."
    ;;

  stop)
    echo "🛑 [LIDO AI LAB] Đang dừng 2 biệt đội..."
    if [ -f "$PID_VN" ]; then
      kill $(cat "$PID_VN") 2>/dev/null && rm -f "$PID_VN"
      echo "⏹️ Đã dừng Biệt Đội Tiếng Việt."
    fi
    if [ -f "$PID_GLOBAL" ]; then
      kill $(cat "$PID_GLOBAL") 2>/dev/null && rm -f "$PID_GLOBAL"
      echo "⏹️ Đã dừng Biệt Đội Toàn Cầu."
    fi
    # Dọn dẹp tiến trình phụ nếu có
    pkill -f "squad_vn_scheduler.py" 2>/dev/null
    pkill -f "squad_global_scheduler.py" 2>/dev/null
    echo "✅ Toàn bộ hệ thống đã dừng."
    ;;

  status)
    echo "======================================================================"
    echo "📊 TRẠNG THÁI TIẾN TRÌNH CỦA 2 BIỆT ĐỘI"
    echo "======================================================================"
    P_VN=$(pgrep -f "squad_vn_scheduler.py")
    P_GB=$(pgrep -f "squad_global_scheduler.py")

    if [ -n "$P_VN" ]; then
      echo "🟢 Biệt Đội Tiếng Việt (Squad VN): ĐANG CHẠY (PID: $P_VN)"
    else
      echo "🔴 Biệt Đội Tiếng Việt (Squad VN): ĐANG TẮT"
    fi

    if [ -n "$P_GB" ]; then
      echo "🟢 Biệt Đội Toàn Cầu (Squad Global): ĐANG CHẠY (PID: $P_GB)"
    else
      echo "🔴 Biệt Đội Toàn Cầu (Squad Global): ĐANG TẮT"
    fi
    echo "======================================================================"
    ;;

  log-vn)
    tail -n 40 -f "$LOG_VN"
    ;;

  log-global)
    tail -n 40 -f "$LOG_GLOBAL"
    ;;

  report)
    "$PYTHON" "$DIR/report.py"
    ;;

  run-vn-now)
    echo "⚡ Chạy ngay 1 vòng quét cho Biệt Đội Tiếng Việt (Xem trực tiếp)..."
    "$PYTHON" -c "
import asyncio
from squad_vn_scheduler import SquadVNScheduler
asyncio.run(SquadVNScheduler().run_cycle())
"
    ;;

  run-global-now)
    echo "⚡ Chạy ngay 1 vòng quét cho Biệt Đội Toàn Cầu (Xem trực tiếp)..."
    "$PYTHON" -c "
import asyncio
from squad_global_scheduler import SquadGlobalScheduler
asyncio.run(SquadGlobalScheduler().run_cycle())
"
    ;;

  *)
    echo "Cách sử dụng: ./run.sh [lệnh]"
    echo ""
    echo "Các lệnh hỗ trợ:"
    echo "  ./run.sh start           - Khởi chạy cả 2 biệt đội chạy ngầm (mỗi 2 tiếng)"
    echo "  ./run.sh stop            - Dừng cả 2 biệt đội"
    echo "  ./run.sh status          - Kiểm tra xem 2 biệt đội có đang chạy không"
    echo "  ./run.sh report          - Xem báo cáo video đã đăng và link YouTube"
    echo "  ./run.sh run-vn-now      - Ép Biệt Đội VN quét và đăng video ngay lập tức"
    echo "  ./run.sh run-global-now  - Ép Biệt Đội Global quét và đăng video ngay lập tức"
    echo "  ./run.sh log-vn          - Xem log trực tiếp của Biệt Đội VN"
    echo "  ./run.sh log-global      - Xem log trực tiếp của Biệt Đội Toàn Cầu"
    echo ""
    ;;
esac
