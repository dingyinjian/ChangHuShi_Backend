from typing import List
from pathlib import Path
import shutil
import uuid
import cv2
from openai import OpenAI
import base64
from django.conf import settings

# 从 Django settings 读取（settings 已从 .env.development/.env.production 加载）
VLM_API_BASE = settings.VLM_API_BASE
VLM_API_KEY = settings.VLM_API_KEY
MODEL_NAME = settings.VLM_MODEL_NAME
VLM_TIMEOUT_SECONDS = settings.VLM_TIMEOUT_SECONDS

client = OpenAI(base_url=VLM_API_BASE, api_key=VLM_API_KEY, timeout=VLM_TIMEOUT_SECONDS)
def app_base_dir() -> Path:
    return Path(__file__).resolve().parent

def extract_frames(video_path, output_dir, interval_sec=5):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频: {video_path}")
    # 获取视频的帧率，帧率:视频每秒包含的画面数量
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 获取视频的总帧数，总帧数:整个视频包含的所有画面的总数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # 计算视频的时长
    duration = total_frames / fps if fps > 0 else 0
    print(f"📹 处理视频: {Path(video_path).name} | 时长: {duration:.1f}s")
    current_time = 0.0
    frame_id = 0
    frames_info = []

    while current_time <= duration:
        # 将时间（秒）转换为帧编号（第几帧）
        frame_num = int(current_time * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        # ret 布尔值，表示是否成功读取到帧
        # frame  读取到的图像数据(numpy数组)
        ret, frame = cap.read()
        if not ret:
            break
        # frame_id:03d 占三位，不足补0(如001,002,...)
        filename = f"frame_{frame_id:03d}_{int(current_time):04d}s.jpg"
        filepath = str(Path(output_dir) / filename)
        # 将图像保存为文件
        cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

        frames_info.append({
            "time_sec": current_time,
            "filepath": filepath
        })

        current_time += interval_sec
        frame_id += 1

    cap.release()
    return frames_info
def clear_folder(folder_path: str):
    path = Path(folder_path)
    if not path.exists():
        return
    shutil.rmtree(path, ignore_errors=True)


def analyze_video(video_path: str) -> List[str]:
    if not video_path:
        raise ValueError("视频路径为空")

    frames_interval = 5
    # 每次分析使用独立临时目录，避免并发任务互相覆盖
    output_dir = app_base_dir() / "frames_tmp" / uuid.uuid4().hex
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        frames = extract_frames(video_path, str(output_dir), frames_interval)
        teach_prompt = (
            "你是一名资深护理专家。请根据此画面，列出当前必须遵守的1-3条核心操作规范"
            "聚焦手部位置、器械使用、操作顺序、服务态度等。每条以'-'开头，不要解释。"
        )
        all_rules = set()
        for i, frame_info in enumerate(frames):
            print(f"  分析帧 {i + 1}/{len(frames)} (t={frame_info['time_sec']:.1f}s)...")
            try:
                result = qwen_vl_analyze(frame_info["filepath"], teach_prompt)
                print(f"大模型识别结果{result}")
                for line in result.split('\n'):
                    line = line.strip()
                    if line.startswith('-'):
                        all_rules.add(line)
            except Exception as e:
                print(f"    ⚠️ 跳过帧: {e}")

        standards = sorted(all_rules)
        return optimize_standards(standards)
    finally:
        clear_folder(str(output_dir))

def qwen_vl_analyze(image_path: str, prompt: str) -> str:
    """调用你部署的 Qwen3-VL 模型"""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                    }
                ]
            }
        ],
        max_tokens=512,
        temperature=0.0  # 减少随机性
    )
    return response.choices[0].message.content.strip()

def optimize_standards(standards: List[str]) -> List[str]:
    """将标准列表去重、优化，并返回 List[str]"""
    if not standards:
        return []
    prompt_text = (
        "请将以下护理操作规范进行去重和精简，仅保留核心条目，每条以 '-' 开头，不要解释，不要编号，不要多余文字。\n"
        "输出格式必须是纯文本，每条占一行，以 '-' 开头。\n\n"
        + "\n".join(standards)
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt_text}]}],
        max_tokens=512,
        temperature=0.0
    )
    text = response.choices[0].message.content.strip()

    # 解析为列表
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('-'):
            # 去掉开头的 '-' 和空格，再加回来保证统一（可选）
            content = line.lstrip('- ').strip()
            if content:
                lines.append(f"- {content}")
    return lines  # 返回 List[str]
