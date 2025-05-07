import shutil
import sys

def check_system_dependencies():
    """
    poppler-utils（pdftoppm）や ghostscript（gs）がインストールされているか確認します。
    足りない場合はエラーメッセージを表示して終了します。
    """
    missing = []

    # チェック対象の外部コマンド（コマンド名: 説明）
    commands = {
        'pdftoppm': 'poppler-utils（PDF → 画像変換）',
        'gs': 'ghostscript（PDF 処理）'
    }

    for cmd, description in commands.items():
        if shutil.which(cmd) is None:
            missing.append(f"{cmd}：{description}")

    if missing:
        print("⚠️ システムに必要な外部コマンドが見つかりません。以下を確認してください：\n")
        for item in missing:
            print(f"  - {item}")

        print("\n🛠 Ubuntu / Google Colab の場合は次のコマンドでインストールできます：")
        print("  sudo apt install poppler-utils ghostscript fonts-ipafont\n")
        print("処理を中断します。依存パッケージをインストールしてから再実行してください。")
        sys.exit(1)
