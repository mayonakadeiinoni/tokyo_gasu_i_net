from PIL import Image
import os

# === 設定項目 ===
# 対象ディレクトリを指定（例: "C:/Users/yuki/images"）
TARGET_DIR = "/home/ytmr0/demo/tokyo_gasu_i_net"

# 解像度を下げる倍率（例: 0.5で半分、0.25で1/4）
SCALE = 0.5

# 出力フォルダ（元と同じに上書きしたいなら同じにしてもOK）
OUTPUT_DIR = os.path.join(TARGET_DIR)

# === 実行 ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(TARGET_DIR):
    if file.lower().endswith(".png"):
        
        img_path = os.path.join(TARGET_DIR, file)
        img = Image.open(img_path)
        
        # 現在のサイズ取得
        w, h = img.size
        new_size = (int(w * SCALE), int(h * SCALE))
        
        # リサイズして保存（品質を落とす）
        img_resized = img.resize(new_size, Image.LANCZOS)
        output_path = os.path.join(OUTPUT_DIR, file)
        img_resized.save(output_path, optimize=True)

        print(f"✅ {file}: {w}x{h} → {new_size[0]}x{new_size[1]}")

print("🎉 全てのPNGの解像度を下げました！")
